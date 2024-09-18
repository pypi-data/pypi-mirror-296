"""Create the CLI interface with correct arguments, and load the inputs in correct formats"""
import argparse
import logging
import sys

import yaml

logger = logging.getLogger(__name__)


class ParserBuilder:
    """
    Create the CLI parser with all the options for oligopipe as ArgumentParser object
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="oligopipe",
                                              description="CLI for oligopipe - oligogenic variant analysis pipelines")

        self.subparsers = self.parser.add_subparsers(title="Commands", dest="subparser",
                                                     description="Run oligopipe {command} -h to get detailed help")

        self.predparser = self.create_predict_subparser()
        self.priorparser = self.create_prioritize_subparser()
        self.configparser = self.create_config_subparser()

    def create_config_subparser(self):
        """
        Sets up the subparser for showing the config file
        """
        parser_config = self.subparsers.add_parser("config", help="Show the template config file", add_help=False)
        return parser_config

    def create_predict_subparser(self):
        """
        Sets up the subparser for prediction, using grouped arguments
        We don't use defaults or required arguments; those are handled in the loading of the arguments and config
        so that options can also be retrieved from input config but are overriden by CLI arguments
        """
        description = "Run a VarCoPP prediction analysis\n\n" \
                      "All options can be passed as CLI arguments or in a global input config file (YAML). " \
                      "CLI arguments override the values in the config file if both are given.\n" \
                      "** Required arguments: database credentials, variants (either in VCF or TSV), " \
                      "and the genome build. **"
        parser_pred = self.subparsers.add_parser("predict", help="Run a VarCoPP prediction", description=description,
                                                 formatter_class=argparse.RawTextHelpFormatter)
        self.add_config_arg(parser_pred)
        self.add_variants_args_group(parser_pred)
        self.add_db_args_group(parser_pred)
        self.add_filters_args_group(parser_pred)

        # parser_pred.add_argument("-de", "--digenic-effect", action="store_true",
        #                     help="Also predict the Digenic Effect for all variant combinations predicted "
        #                          "as pathogenic by VarCoPP.")
        # parser_pred.add_argument("-contrib", "--calc-contrib", action="store_true",
        #                     help="Also calculate the feature contributions for the VarCoPP predictions "
        #                          "(this takes quite some time)")

        self.add_output_args_group(parser_pred)

        return parser_pred

    def create_prioritize_subparser(self):
        """
        Sets up the subparser for prioritization, using grouped arguments
        We don't use defaults or required arguments; those are handled in the loading of the arguments and config
        so that options can also be retrieved from input config but are overriden by CLI arguments
        """
        description = "Run a prioritization analysis with Hop \n\n" \
                      # "All options can be passed as CLI arguments or in a global input config file (YAML). " \
                      # "CLI arguments override the values in the config file if both are given.\n" \
                      # "** Required arguments: database credentials, variants (either in VCF or TSV), " \
                      # "genome build, and at least one type of disease-related info (HPO terms or gene panel). **"
        parser_prior = self.subparsers.add_parser("prioritize", formatter_class=argparse.RawTextHelpFormatter,
                                                description=description, help="Run a prioritization analysis with Hop")
        self.add_config_arg(parser_prior)
        parser_prior.add_argument("-N", "--nb-top-ranked", type=int,
                                  help="The number of top-ranked combinations to retain (default = 100).")
        self.add_variants_args_group(parser_prior)
        self.add_db_args_group(parser_prior)
        self.add_seeds_args_group(parser_prior)
        self.add_filters_args_group(parser_prior)
        self.add_output_args_group(parser_prior)
        return parser_prior

    def add_db_args_group(self, subparser=None):
        if subparser:
            db = subparser.add_argument_group("Annotation database credentials")
        else:
            db = self.parser.add_argument_group("Annotation database credentials")
        db.add_argument("-host", "--db-host", help="Hostname of annotation database server.")
        db.add_argument("-u", "--db-user", help="User for annotation database.")
        db.add_argument("-pw", "--db-password", help="Password for annotation database.")
        db.add_argument("-p", "--db-port", help="Port for annotation database.")

    def add_variants_args_group(self, subparser=None):
        if subparser:
            variants = subparser.add_argument_group("Variant input")
        else:
            variants = self.parser.add_argument_group("Variant input")
        variants.add_argument("-vcf", "--variants-vcf", action="store",
                              help="The patient's VCF file, can be compressed.")
        variants.add_argument("-tsv", "--variants-tsv", action="store",
                              help="Tab-delimited text file containing the patient's variants to analyse "
                                   "(chrom/pos/ref/alt/zygosity).")
        variants.add_argument("-hg", "--genome-build", choices=["hg19", "hg38"], action="store",
                              help="The genome assembly to which the positions of your variants correspond.")
        variants.add_argument("-s", "--patient-sex", metavar="patient_sex", choices=["M", "F", "U"], action="store",
                              help="The sex of the patient (defaults to U = undetermined).")

    def add_output_args_group(self, subparser=None):
        if subparser:
            out = subparser.add_argument_group("Output")
        else:
            out = self.parser.add_argument_group("Output")
        out.add_argument("-dir", "--outdir", metavar="output_path",
                         help="Output directory (defaults to working directory).")
        out.add_argument("-pre", "--prefix", metavar="prefix", type=str,
                        help="Optional prefix for the output files, use for example the patient ID.")
        out.add_argument("-f", "--force", help="Force re-using an output directory, which may overwrite files.",
                         action="store_true")
        out.add_argument("-v", "--verbose", help="Show debug logs", action="store_true")

    def add_config_arg(self, subparser=None):
        help_string = "Configuration file in YAML format; run 'oligopipe config' to show the template"
        if subparser:
            subparser.add_argument("-c", "--config", action="store", metavar="config_file", help=help_string)
        else:
            self.parser.add_argument("-c", "--config", action="store", metavar="config_file", help=help_string)

    def add_filters_args_group(self, subparser=None):
        if subparser:
            filters = subparser.add_argument_group("Filtering options")
            # Gene panel is put in filters for prediction, but as a seed for prioritization
            if subparser.prog == "oligopipe predict":
                filters.add_argument("-gp", "--panel", action="store", metavar="gene_panel",
                                     help="Gene panel file, containing a list of gene names or ENSGs"
                                          " to restrict the analysis.")
        else:
            filters = self.parser.add_argument_group("Filtering options")
        filters.add_argument("-m", "--max-maf", action="store", type=float,
                            help="The MAF to filter variants (default: 0.035).")
        filters.add_argument("--keep-intron-syn", action="store_true",
                            help="Don't remove intronic and synonymous variants (not recommended).")
        filters.add_argument("--keep-intergenic", action="store_true",
                            help="Don't remove intergenic variants (not recommended).")

    def add_seeds_args_group(self, subparser=None):
        if subparser:
            seeds = subparser.add_argument_group("Disease-related information", description="Submit at least one")
        else:
            seeds = self.parser.add_argument_group("Annotation database credentials")
        seeds.add_argument("-hpo", "--hpo-terms", metavar="hpo_file",
                           help="File containing a list of HPO IDs (e.g. HP:0001166).")
        seeds.add_argument("-gp", "--panel", action="store", metavar="gene_panel",
                           help="Gene panel file, containing a list of gene names or ENSGs.")

    def parse_args(self):
        return self.parser.parse_args()


class ArgumentsLoader:
    """
    Loads the arguments given as command line options and/or passed in the config file,
    assigning default values where needed and always letting command line supersede config
    For required parameters (DB credentials, genome build, variant input (seeds)) a sys.exit() is triggered if not given
    """
    def __init__(self, args):
        """
        :param args: Namespace object from the argument parser,
                    contains data passed to execution (incl path to config file)
        """
        self.args = args
        self.config = {}
        self.options = {"force": True if args.force else False, "verbose": True if args.verbose else False}

        # digenic effect and contribution analysis (currently not included)
        # self.options["digenic_effect"] = True if args.digenic_effect else False
        # self.options["calc_contrib"] = True if args.calc_contrib else False

    def load_predict_options(self):
        """
        :return: dictionary of loaded arguments for prediction ("options")
        """
        options = self.options
        args = self.args
        config = self.config

        if args.config:
            with open(args.config, "r") as f:
                config = yaml.safe_load(f)

        # Arguments common to both analyses
        self.load_db_args(args, config, options)
        self.load_variant_args(args, config, options)
        self.load_filter_args(args, config, options)
        self.load_output_args(args, config, options)

        # Specific prediction arguments
        if args.panel:
            options["panel_file"] = args.panel
        elif "gene_panel_file" in config:
            options["panel_file"] = config["gene_panel_file"]
        else:
            options["panel_file"] = None

        return options

    def load_prioritize_options(self):
        """
        :return: dictionary of loaded arguments for prioritization ("options")
        """
        options = self.options
        args = self.args
        config = self.config

        if args.config:
            with open(args.config, "r") as f:
                config = yaml.safe_load(f)

        # Arguments common to both analyses
        self.load_db_args(args, config, options)
        self.load_variant_args(args, config, options)
        self.load_filter_args(args, config, options)
        self.load_output_args(args, config, options)

        # Specific prioritization arguments
        self.load_seeds_args(args, config, options)
        if args.nb_top_ranked:
            options["N"] = args.nb_top_ranked
        elif "top_N" in config and config["top_N"]:
            options["N"] = config["top_N"]
        else:
            options["N"] = 100

        return options

    # TODO check if all methods below can be implemented more concisely
    @staticmethod
    def load_db_args(args, config, options):
        if args.db_host:
            options["db_host"] = args.db_host
        elif "annotation_database" in config and "host" in config["annotation_database"] \
                and config["annotation_database"]["host"]:
            options["db_host"] = config["annotation_database"]["host"]
        else:
            logger.error("Missing annotation DB host parameter in command line or config file")
            sys.exit()

        if args.db_user:
            options["db_user"] = args.db_user
        elif "annotation_database" in config and "user" in config["annotation_database"] \
                and config["annotation_database"]["user"]:
            options["db_user"] = config["annotation_database"]["user"]
        else:
            logger.error("Missing annotation DB user parameter in command line or config file")
            sys.exit()

        if args.db_password:
            options["db_password"] = args.db_password
        elif "annotation_database" in config and "password" in config["annotation_database"] \
                and config["annotation_database"]["password"]:
            options["db_password"] = config["annotation_database"]["password"]
        else:
            logger.error("Missing annotation DB password parameter in command line or config file")
            sys.exit()

        if args.db_port:
            options["db_port"] = args.db_port
        elif "annotation_database" in config and "port" in config["annotation_database"] \
                and config["annotation_database"]["port"]:
            options["db_port"] = config["annotation_database"]["port"]
        else:
            logger.error("Missing annotation DB port parameter in command line or config file")
            sys.exit()

    @staticmethod
    def load_variant_args(args, config, options):
        if args.genome_build:
            options["genome_build"] = args.genome_build
        elif "variant_input" in config and "genome_build" in config["variant_input"] \
                and config["variant_input"]["genome_build"]:
            options["genome_build"] = config["variant_input"]["genome_build"]
        else:
            logger.error("Missing genome build parameter in command line or config file")
            sys.exit()

        if args.variants_vcf:
            options["variants_vcf"] = args.variants_vcf
        elif "variant_input" in config and "vcf_file" in config["variant_input"] \
                and config["variant_input"]["vcf_file"]:
            options["variants_vcf"] = config["variant_input"]["vcf_file"]
        elif args.variants_tsv:
            options["variants_tsv"] = args.variants_tsv
        elif "variant_input" in config and "tsv_file" in config["variant_input"] \
                and config["variant_input"]["tsv_file"]:
            options["variants_tsv"] = config["variant_input"]["tsv_file"]
        else:
            logger.error("Missing variant file (.tsv or .vcf) in command line or config file")
            sys.exit()

        # Patient sex: defaults to Undetermined if not given
        if args.patient_sex:
            options["sex"] = args.patient_sex
        elif "patient_info" in config and "sex" in config["patient_info"] and config["patient_info"]["sex"]:
            options["sex"] = config["patient_info"]["sex"]
        else:
            options["sex"] = "U"

    @staticmethod
    def load_filter_args(args, config, options):
        if args.max_maf:
            options["max_maf"] = args.max_maf
        elif "variant_filters" in config and "max_maf" in config["variant_filters"]\
                and config["variant_filters"]["max_maf"]:
            options["max_maf"] = config["variant_filters"]["max_maf"]
        else:
            options["max_maf"] = 0.035

        if args.keep_intron_syn:
            options["remove_intronic_synonymous"] = False
        elif "variant_filters" in config and "remove_intronic_synonymous" in config["variant_filters"]\
                and config["variant_filters"]["remove_intronic_synonymous"]:
            options["remove_intronic_synonymous"] = config["variant_filters"]["remove_intronic_synonymous"]
        else:
            options["remove_intronic_synonymous"] = True

        if args.keep_intron_syn:
            options["remove_intron_and_all_synonymous"] = False
        elif "variant_filters" in config and "remove_intron_and_all_synonymous" in config["variant_filters"]:
            options["remove_intron_and_all_synonymous"] = config["variant_filters"]["remove_intron_and_all_synonymous"]
        else:
            options["remove_intron_and_all_synonymous"] = False

        if args.keep_intergenic:
            options["remove_intergenic"] = False
        elif "variant_filters" in config and "remove_intergenic" in config["variant_filters"]\
                and config["variant_filters"]["remove_intergenic"]:
            options["remove_intergenic"] = config["variant_filters"]["remove_intergenic"]
        else:
            options["remove_intergenic"] = True

    @staticmethod
    def load_output_args(args, config, options):
        if args.outdir:
            options["outdir"] = args.outdir
        elif "output" in config and "dir" in config["output"]:
            options["outdir"] = config["output"]["dir"]
        else:
            options["outdir"] = None

        if args.prefix:
            options["prefix"] = args.prefix
        elif "output" in config and "prefix" in config["output"]:
            options["prefix"] = config["output"]["prefix"]
        else:
            options["prefix"] = None

    @staticmethod
    def load_seeds_args(args, config, options):
        if args.panel:
            options["panel_file"] = args.panel
        elif "gene_panel_file" in config:
            options["panel_file"] = config["gene_panel_file"]
        else:
            options["panel_file"] = None

        if args.hpo_terms:
            options["hpo_terms_file"] = args.hpo_terms
        elif "hpo_terms_file" in config:
            options["hpo_terms_file"] = config["hpo_terms_file"]
        else:
            options["hpo_terms_file"] = None

        if not options["panel_file"] and not options["hpo_terms_file"]:
            logger.error("Missing at least one type of disease-related information (HPO terms or gene panel)")
            sys.exit()
