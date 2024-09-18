import itertools
import logging
import re
from abc import abstractmethod

from oligopipe.preprocess.annotation import VariantAnnotator, GenePairAnnotator
from oligopipe.entities import VarCoPPInputData, Variant, VariantParsingError, HOPInputData

logger = logging.getLogger(__name__)


class PreprocessPipeline:

    def __init__(self, variants, filters=None, gene_panel=None):
        self.variants = variants    # list of Variant objects
        self.filters = filters      # list with filters e.g. [('MAX_MAF', 0.035), 'REMOVE_INTERGENIC', 'REMOVE_INTRONS']
        self.gene_panel = gene_panel    # list of genes or None; remains None for HOP preprocessing,
                                        # but is needed for annotate() in execute()
        self.variants_compkeys_to_original = {}     # allow to retrieve discarded variants how they were originally
                                                    # submitted (especially important for indels)
        self.variants_compkeys_to_zygosity = {}
        self.invalid_zygosity = []

    def preprocess_vars(self, patient_information, genome_build, db_credentials):
        """
        First part of the preprocessing: annotate and handle variants
        (including getting the discarded variants
        and calculating the number of gene pairs that will be created)
        :param patient_information: patient data dictionary containing "sex" key
        :param genome_build: 'hg19' or 'hg38'
        :param db_credentials: dictionary containing connection parameters for the database
        :return: db_schema: 'old' or 'new',
                 nb_gene_pairs: int,
                 discarded_vars_original: dict for the 3 types of discarded vars
                                        ("missing" / "filtered" / "invalid_zygosity") -
                                        values are a list of variants in their original input,
                 annotated_variants: list of AnnotationData objects
        """
        logger.info("Start preprocessing...")
        logger.debug("De-duplicating variants with 2 alt alleles and determining the zygosity of each variant...")
        self.update_var_list(patient_information)

        logger.info("Annotating the variants...")
        # prepare by creating necessary dicts
        self.set_variants_dict()
        self.set_zygosity_dict()
        vars_for_annotation = [compkey for compkey in self.variants_compkeys_to_original.keys()
                               if compkey not in self.invalid_zygosity]

        var_annotator = VariantAnnotator(db_credentials, genome_build)
        annotated_variants, discarded_vars = list(var_annotator.annotate(vars_for_annotation,
                                                                         self.variants_compkeys_to_zygosity,
                                                                         self.filters, self.gene_panel))

        # get the discarded variants but in the chr:pos:ref:alt representation of how they were initially submitted
        discarded_vars_original = {"invalid_zygosity": self.get_original_vars(self.invalid_zygosity)}
        for key, var_compkey_list in discarded_vars.items():
            discarded_vars_original[key] = self.get_original_vars(var_compkey_list)

        db_schema = var_annotator.db_schema
        nb_gene_pairs = len(list(itertools.combinations(var_annotator.unique_genes, 2)))

        return db_schema, nb_gene_pairs, discarded_vars_original, annotated_variants

    def preprocess_gp(self, annotated_variants, patient_information, genome_build, db_credentials):
        """
        Second part of the preprocessing: annotate gene pairs and create the input
        :param annotated_variants: list of AnnotationData objects
        :param patient_information: patient data dictionary containing "sex" key
        :param genome_build: 'hg19' or 'hg38'
        :param db_credentials: dictionary containing connection parameters for the database
        :return: input_data: VarCoPPInputData or HOPInputData object
        """
        logger.info("Annotating the gene pairs...")
        gene_pairs = GenePairAnnotator(db_credentials, genome_build).annotate(annotated_variants)
        # dict of format: {('ensgA', 'ensgB'): {"biol_dist": x, "BP_similarity": y, "KG_dist": z}}
        # (or gene names instead of ENSGs for the old DB schema)
        input_data = self.create_input_data(patient_information, annotated_variants, gene_pairs)
        logger.info("VarCoPP preprocessing completed!")
        return input_data

    def get_original_vars(self, var_list):
        return [self.variants_compkeys_to_original[compkey] for compkey in var_list]

    def set_variants_dict(self):
        """
        Iterates over the variant objects to create a dictionary {composite_key: original_repr}
        where original_repr is chr:pos:ref:alt of the variant as provided in the input
        (after annotation, the AnnotationData objects have the chr:pos:ref:alt as present in the DB,
        which can be different)
        """
        for var in self.variants:
            self.variants_compkeys_to_original[var.composite_key] = str(var)

    def set_zygosity_dict(self):
        """
        Iterates over the variant objects to create a dictionary {composite_key: zygosity}
        It also collects a list of variants (composite_keys) with invalid zygosity
        """
        for var in self.variants:
            zygosity = var.zygosity
            if zygosity is None:
                self.invalid_zygosity.append(var.composite_key)
            self.variants_compkeys_to_zygosity[var.composite_key] = zygosity

    def update_var_list(self, patient_information):
        """
        Updates the list of variants parsed from input. If there are special cases with 2 alternative alleles,
        those are recreated as 2 separate heterozygous variants. For the others, the alt allele and zygosity
        are set based on the raw input.
        :param patient_information: patient data dictionary containing "sex" key
        """
        for var in list(self.variants):  # iterate over copy of variants list because we will add/remove some
            alts = var.alt_list
            zyg_splitted = re.split("[|/]", var.raw_zygosity)

            # create separate heterozygous variants for cases with GT = "1/2" etc.
            # (extra checks to exclude cases with e.g. GT = "1", GT = "0/1", GT = "1/1" or GT = "./1")
            if len(alts) > 1 and len(zyg_splitted) > 1 and "0" not in zyg_splitted and "." not in zyg_splitted \
                    and zyg_splitted[0] != zyg_splitted[1]:
                alt_indices = [int(a)-1 for a in zyg_splitted]
                if len(alt_indices) > 2:
                    raise VariantParsingError("There was a problem determining the alternative allele for variant "
                                          "chr{c}:{pos}. Please review the GT info.".format(c=var.chr, pos=var.pos))
                var1 = Variant(var.chr, var.pos, var.ref, alt=alts[alt_indices[0]].strip(),
                               zygosity="Heterozygous", id=var.id)
                var1.set_composite_key()
                var2 = Variant(var.chr, var.pos, var.ref, alt=alts[alt_indices[1]].strip(),
                               zygosity="Heterozygous", id=var.id)
                var2.set_composite_key()
                self.variants.remove(var)
                self.variants += [var1, var2]

            else:
                var.alt = var.get_alt_from_list()
                var.set_composite_key()
                var.set_zygosity(patient_information.sex)

    @abstractmethod
    def create_input_data(self, patient_information, annotated_variants, gene_pairs):
        pass


class VarcoppPreprocessPipeline(PreprocessPipeline):

    def __init__(self, variants, filters=None, gene_panel=None):
        super().__init__(variants, filters)
        self.gene_panel = gene_panel

    def create_input_data(self, patient_information, annotated_variants, gene_pairs):
        varcopp_input_data = VarCoPPInputData(patient_information, annotated_variants, gene_pairs)
        return varcopp_input_data

class HOPPreprocessPipeline(PreprocessPipeline):

    def __init__(self, variants, seeds, filters=None, nb_tops=100):
        super().__init__(variants, filters)
        self.seeds = seeds
        self.nb_tops = nb_tops

    def create_input_data(self, patient_information, annotated_variants, gene_pairs):
        hop_input_data = HOPInputData(patient_information, annotated_variants, gene_pairs, self.seeds, self.nb_tops)
        logger.info("HOP preprocessing completed!")
        return hop_input_data
