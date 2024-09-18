"""CLI interface for oligopipe pipelines."""
import logging
import sys

from oligopipe.cli_output import ResultsPrinter
from oligopipe.entities import VariantParsingError
from oligopipe.preprocess.input_parsers import ParsingError

try:
    import magic
except ImportError:
    logging.error("There is a problem with the dependency 'python-magic' which is probably related to using a "
                  "M1 Macbook. Please try to pip install 'python-magic-bin' to resolve the issue.")
    sys.exit()
try:
    import psycopg2
except ImportError:
    logging.error("There is a problem with the dependency 'psycopg2' which is probably related to using a M1 Macbook. "
          "Please try to pip uninstall 'psycopg2' and re-install 'psycopg2-binary' to resolve the issue.")
    sys.exit()

from oligopipe.cli_parser import ParserBuilder, ArgumentsLoader
from oligopipe.pipelines import PredictionPipeline, PrioritizationPipeline
from oligopipe.cli_utils import show_config

logger = logging.getLogger(__name__)


def main():
    """
    The main function for oligopipe CLI, executes on commands:
    `python -m oligopipe` and `$ oligopipe `.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%d/%m %H:%M:%S'
    )
    parser = ParserBuilder()
    args = parser.parse_args()
    if args.subparser == "config":
        show_config()
    elif args.subparser == "prioritize":
        options = ArgumentsLoader(args).load_prioritize_options()
        pipeline = PrioritizationPipeline(options)
        results = safe_run_pipeline(pipeline)
        ResultsPrinter(options).execute(results, True)
        logging.info("Prioritization pipeline has finished.")
        # logging.error("Prioritization is not available yet")
    elif args.subparser == "predict":
        options = ArgumentsLoader(args).load_predict_options()
        pipeline = PredictionPipeline(options)
        results = safe_run_pipeline(pipeline)
        ResultsPrinter(options).execute(results)
        logging.info("Prediction pipeline has finished.")
    else:
        parser.parser.print_help()


def safe_run_pipeline(pipeline):
    """
    Executes the selected pipeline and handles possible errors
    :param pipeline: initialized Pipeline object
    :return: results dictionary
    """
    try:
        results = pipeline.execute()
    except ParsingError as e:
        logging.error(e)
        sys.exit()
    except VariantParsingError as e:
        logging.error(e)
        sys.exit()
    except psycopg2.OperationalError as e:
        logger.error("Error connecting to the annotation database:")
        logger.error(e)
        logger.error("Please review the database credentials you provided. Exiting oligopipe")
        sys.exit()
    return results
