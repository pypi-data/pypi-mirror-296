import gzip
import importlib.resources
import json
import logging
import pickle
import warnings
from itertools import islice, chain
from pathlib import Path

from oligopipe.predictors import Predictor

logger = logging.getLogger(__name__)


def todict(obj):
    if hasattr(obj, "__iter__"):
        return [todict(v) for v in obj]
    elif hasattr(obj, "__dict__"):
        return dict([(key, todict(value))
                     for key, value in obj.__dict__.iteritems()
                     if not callable(value) and not key.startswith('_')])
    else:
        return obj


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def iter_chunks(iterable, size):
    """ Implementation of previous "chunks" function, but take iterable as input and give iterables as outputs.
        Iterable at n step must be consumed before n+1 step can be generated.
    """
    iterator = iter(iterable)
    for first in iterator:
        yield chain([first], islice(iterator, size - 1))


def get_model(model):
    """
    Load, unpickle and return the specified model (where the pickle file is possibly gzipped)
    """
    # ignore sklearn warnings about version differences when loading model
    warnings.filterwarnings("ignore", category=UserWarning)

    model_path = get_model_path(model)
    logger.debug(f"Getting {model} model [path={model_path}]")

    try:
        with gzip.open(model_path, 'rb') as file:
            m = pickle.load(file, encoding='latin1')
            logger.debug(f"Successfully loaded {model} model!")
            return m
    except gzip.BadGzipFile:
        with open(model_path, 'rb') as f:
            m = pickle.load(f)
            logger.debug(f"Successfully loaded {model} model!")
            return m
    except IOError as e:
        logger.error(f"##### {model} model could not be loaded.", e)
        raise e


def get_model_path(model):
    """
    Load path for the specified model (DE or VarCoPP) from the JSON config
    """
    config_package = Predictor.CONFIG_PACKAGE_PATH
    config_filename = Predictor.CONFIG_FILENAME
    with importlib.resources.open_text(config_package, config_filename) as predictors_config_file:
        predictors_config = json.load(predictors_config_file)
        package_path = predictors_config[model]["package_path"]
        file_name = predictors_config[model]["file_name"]
        with importlib.resources.path(package_path, file_name) as model_path:
            return Path(model_path)

