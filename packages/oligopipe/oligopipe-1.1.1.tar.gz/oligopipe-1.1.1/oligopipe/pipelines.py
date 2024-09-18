"""
Given a list of Variant objects and other parsed inputs in an "options" dictionary,
run a VarCoPP prediction or prioritization pipeline.
This code should work regardless of the running environment (CLI, app ...)
"""
import logging
from abc import abstractmethod

import magic

from oligopipe.entities import PatientInformation
from oligopipe.network import OligoNetwork
from oligopipe.preprocess.input_parsers import DefaultVariantFormatParser, GenePanelParser, VCFParser, HPOParser
from oligopipe.preprocess.preprocessing import VarcoppPreprocessPipeline, HOPPreprocessPipeline
from oligopipe.utils import get_model
from oligopipe.predictors import VarcoppPredictor, HOPPredictor

logger = logging.getLogger(__name__)


class Pipeline:
    # name of the annotation database per genome build
    ANNOT_DB_NAME = {"hg19": "annotation", "hg38": "annot_hg38"}

    def __init__(self, options):
        """
        :param options: dictionary of loaded arguments from inputs
        """
        self.options = options
        self.metadata = {}
        self.results = {}
        if options["verbose"]:
            logging.getLogger().setLevel(logging.DEBUG)

    @abstractmethod
    def execute(self):
        """Executes the pipeline and returns a dictionary of results"""
        pass

    def get_inputs_from_options(self):
        """
        Parses the options to get the prediction pipeline inputs.
        (parent class method which is extended for the prioritization subclass)
        :return: variants: list of Variant objects
                 metadata: dictionary with metadata about the current pipeline run (keys: "variants_input",
                 "nb_variants_input", "genome_build", "patient_info", "filters", "gene_panel", "database")
        """
        options = self.options

        # database dictionary
        annot_db = {
            "HOST": options["db_host"],
            "PORT": options["db_port"],
            "DB": self.ANNOT_DB_NAME[options["genome_build"]],
            "USER": options["db_user"],
            "PASSWORD": options["db_password"]
        }

        # parse variants
        variants = []
        variant_file = None
        if "variants_vcf" in options:
            variant_file = options["variants_vcf"]
            content_type = magic.from_file(options["variants_vcf"], mime=True)
            with open(options["variants_vcf"], "rb") as f:
                variants = list(VCFParser().parse(f, content_type))
        elif "variants_tsv" in options:
            variant_file = options["variants_tsv"]
            with open(options["variants_tsv"], "r") as f:
                var_input = f.read()
            variants = list(DefaultVariantFormatParser().parse(var_input))

        # create PatientInformation object
        patient_info = PatientInformation(id="", sex=options["sex"])

        # create filters correctly formatted (TODO see if class can be adopted to make better use of it here)
        filters = [('MAX_MAF', options["max_maf"])]
        if options["remove_intergenic"]:
            filters.append("REMOVE_INTERGENIC")
        if options["remove_intronic_synonymous"]:
            filters.append("REMOVE_INTRONS")
        elif options["remove_intron_and_all_synonymous"]:
            filters.append("REMOVE_INTRONS_AND_SYNONYMOUS")

        # create gene panel list
        gene_panel = []
        if options["panel_file"]:
            with open(options["panel_file"], "rb") as f:
                gene_panel = GenePanelParser().parse_file(f, annot_db)

        metadata = {"variants_input": variant_file, "nb_variants_input": len(variants),
                    "genome_build": options["genome_build"],
                    "patient_info": patient_info,
                    "filters": filters, "gene_panel": gene_panel,
                    "database": annot_db}
        logger.debug("Parsed input:\n" + str(metadata))

        return variants, metadata

    @abstractmethod
    def run(self, input):
        pass

    def get_varcopp_model(self):
        """
        :return: unpickled model
        """
        logger.debug("Loading the VarCoPP model...")
        if self.metadata["genome_build"] == "hg19":
            return get_model("varcopp_19")
        else:
            return get_model("varcopp_38")

    # def run_de(self, result_json):
    #     """
    #     Uses the results from VarCoPP to run the DE predictor on pathogenic combinations,
    #     updating the result_json with its results
    #     :param result_json: VarCoPPResults instance as JSON
    #     """
    #     logger.info("Running the Digenic Effect predictions...")
    #     logger.debug("Loading the DE model...")
    #     if self.metadata["genome_build"] == "hg19":
    #         de_model = get_model("digenic_effect_19")
    #     else:
    #         de_model = get_model("digenic_effect_38")
    #     logger.debug("Predicting...")
    #     for comb_id, comb in result_json["combinations"].items():
    #         if comb["prediction"] == "Disease-causing":
    #             comb["de_prediction"] = DigenicEffectPredictor(de_model).predict(comb["vectorcomb"])
    #         else:
    #             comb["de_prediction"] = None
    #
    # def run_contrib(self, result_json):
    #     """
    #     Uses the results from VarCoPP to calculate feature contributions of each combination,
    #     updating the result_json with its results
    #     :param result_json: VarCoPPResults instance as JSON
    #     """
    #     logger.debug("Calculating feature contributions...")
    #     varcopp_model = self.get_varcopp_model()
    #     for comb_id, comb in result_json["combinations"].items():
    #         comb["feature_contributions"] = VarcoppContributionAnalyzer(varcopp_model).execute(comb["vectorcomb"])

    @staticmethod
    def create_gene_network(result_json):
        """
        Calculates the gene network from the VarCoPP results
        :param result_json: VarCoPPResults/HOPResults instance as JSON
        :return network: dictionary representing an OligoNetwork object (from get_graph())
        """
        logger.info("Creating the gene network...")
        network = OligoNetwork(result_json).get_augmented_graph()
        logger.info("Finished gene network generation.")
        return network


class PredictionPipeline(Pipeline):
    def execute(self):
        """
        Runs the pipeline: loading and preprocessing input, prediction, (network creation)
        :return results: dictionary containing the different outputs
        """
        variants, metadata = self.get_inputs_from_options()
        self.metadata = metadata
        varcopp_input, discarded_vars = self.preprocess_inputs(variants, gene_pair_limit=100000)
        self.results["discarded_vars"] = discarded_vars
        logger.info("-------------------------------")

        result_json = self.run(varcopp_input)
        # if self.options["digenic_effect"]:
        #     self.run_de(result_json)
        # if self.options["calc_contrib"]:
        #     self.run_contrib(result_json)
        self.results["result_json"] = result_json
        self.results["metadata"] = self.metadata
        logger.info("Finished prediction.")
        logger.info("-------------------------------")

        # network = self.create_gene_network(result_json)
        # self.results["network"] = network
        # logger.info("-------------------------------")
        return self.results

    def preprocess_inputs(self, variants, gene_pair_limit):
        """
        Connects to the annotation database to preprocess the variants (also updates self.metadata with the db_schema)
        :param variants: list of Variant objects
        :param gene_pair_limit: number of gene pairs that leads to a warning
        :return: varcopp_input: VarcoppInputData object
                 discarded_vars: dict for the 3 types of discarded vars ("missing" / "filtered" / "invalid_zygosity"),
                                values are a list of variants
        """
        preprocess = VarcoppPreprocessPipeline(variants, self.metadata["filters"], self.metadata["gene_panel"])
        db_schema, nb_gene_pairs, discarded_vars, annotated_variants = preprocess.preprocess_vars(
            self.metadata["patient_info"], self.metadata["genome_build"], self.metadata["database"])
        if nb_gene_pairs > gene_pair_limit:
            # Note: in ORVAL we stop the execution here
            logging.warning("There are a lot of gene pairs ({0}). (Their annotation can take a very long time)"
                            .format(nb_gene_pairs))
            logging.warning("Remember that VarCoPP is not intended for complete exomes! "
                            "Consider using a gene panel and/or stricter variant filtering settings.")
        varcopp_input = preprocess.preprocess_gp(annotated_variants, self.metadata["patient_info"],
                                              self.metadata["genome_build"], self.metadata["database"])
        self.metadata["db_schema"] = db_schema
        return varcopp_input, discarded_vars

    def run(self, varcopp_input):
        """
        Executes the VarCoPP prediction
        :param varcopp_input: VarCoPPInputData instance
        :return: VarCoPPResults instance as JSON
        """
        logger.info("Running the VarCoPP predictions...")
        varcopp_model = self.get_varcopp_model()
        logger.debug("Predicting...")
        return VarcoppPredictor(varcopp_model, self.metadata["genome_build"])\
            .execute(varcopp_input, self.metadata["db_schema"])

class PrioritizationPipeline(Pipeline):
    def execute(self):
        """
        Runs the prioritization pipeline: loading and preprocessing input, prioritization
        :return results: dictionary containing the different outputs
        """
        variants, metadata = self.get_inputs_from_options()
        self.metadata = metadata
        hop_input, discarded_vars = self.preprocess_inputs(variants)
        self.results["discarded_vars"] = discarded_vars
        logger.info("-------------------------------")

        result_json = self.run(hop_input)
        self.results["result_json"] = result_json
        self.results["metadata"] = self.metadata
        logger.info("Finished prioritization.")
        logger.info("-------------------------------")
        return self.results

    def get_inputs_from_options(self):
        """
        Parses the options to get the prioritization pipeline inputs.
        (Running the parent class method and adding the options that are specific to prioritization; HPOs and N)
        :return: variants: list of Variant objects
                 metadata: dictionary with metadata about the current pipeline run (keys: "variants_input",
                 "nb_variants_input", "genome_build", "patient_info", "filters", "gene_panel", "database",
                 "hpo_terms", "top_N")
        """
        variants, metadata = super().get_inputs_from_options()
        options = self.options

        # create HPO list
        hpo_terms = []
        if options["hpo_terms_file"]:
            with open(options["hpo_terms_file"], "rb") as f:
                hpo_terms = HPOParser().parse_file(f, metadata["database"])

        metadata["hpo_terms"] = hpo_terms
        metadata["top_N"] = options["N"]

        logger.debug("Full parsed input:\n" + str(metadata))
        return variants, metadata

    def preprocess_inputs(self, variants):
        """
        Connects to the annotation database to preprocess the variants (also updates self.metadata with the db_schema)
        :param variants: list of Variant objects
        :return: hop_input: HOPInputData object
                 discarded_vars: dict for the 3 types of discarded vars ("missing" / "filtered" / "invalid_zygosity"),
                                values are a list of variants
        """
        seeds = self.metadata["gene_panel"] + self.metadata["hpo_terms"]
        preprocessor = HOPPreprocessPipeline(variants, seeds, self.metadata["filters"], self.metadata["top_N"])
        db_schema, nb_gene_pairs, discarded_vars, annotated_variants = preprocessor.preprocess_vars(
            self.metadata["patient_info"], self.metadata["genome_build"], self.metadata["database"])
        hop_input = preprocessor.preprocess_gp(annotated_variants, self.metadata["patient_info"],
                                          self.metadata["genome_build"], self.metadata["database"])
        self.metadata["db_schema"] = db_schema
        return hop_input, discarded_vars

    def run(self, hop_input):
        """
        Executes the prioritization
        :param hop_input: HOPInputData instance
        :return: HOPResults instance as JSON
        """
        logger.info("Running the VarCoPP predictions...")
        varcopp_model = self.get_varcopp_model()
        logger.debug("Predicting...")
        return HOPPredictor(varcopp_model, self.metadata["genome_build"])\
            .execute(hop_input, self.metadata["db_schema"])
