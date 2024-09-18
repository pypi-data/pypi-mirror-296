import csv
import importlib.resources
import json
import logging
import os
import sys

from oligopipe.network import OligoNetwork

logger = logging.getLogger(__name__)


def show_config():
    with importlib.resources.open_text("test_data", "input_config.yaml") as f:
        print(f.read())


def set_outdir(outdir_arg, force):
    """
    Set up the output directory. If none given, take the current working directory.
    If the given dir exists, check if "force" and else exit
    :param outdir_arg: None or string
    :param force: boolean
    :return: path of the output directory as String
    """
    if outdir_arg:
        outdir = outdir_arg
        if os.path.exists(outdir):
            if not force:
                logging.error(
                    "Output folder already exists. Use -f/--force to use it anyway, which may overwrite files")
                logging.error("oligopipe CLI will now exit")
                sys.exit()
        else:
            os.makedirs(outdir)
    else:
        outdir = os.path.curdir
    return outdir


def create_out_filename(name, prefix):
    """
    Creates filename for an output file
    :param name: name of the output including file format suffix
    :param prefix: None or a String
    :return: filename including prefix if provided
    """
    if prefix:
        return f"{prefix}_{name}"
    else:
        return name


def write_json(json_dict, filename):
    """
    Writes a dictionary to a JSON file
    :param json_dict
    :param filename
    """
    with open(filename, "w") as out:
        json.dump(json_dict, out)


def write_txt(output_list, filename):
    """
    Writes a list to a .txt file, one element per line
    :param output_list: list of Strings
    :param filename
    """
    with open(filename, "w") as out:
        out.write("\n".join(output_list))


def write_graphml(network_dict, filename):
    """
    Writes a network to a GraphML file, adding also a header and comment
    :param network_dict: dictionary representing an OligoNetwork object (from get_graph())
    :param filename
    """
    xml_header = '<?xml version="1.0" encoding="UTF-8"?>'
    xml_comment = '<!-- This file can be imported in Cytoscape (File > Import > Network from file) or Gephi ' \
                  '(File > Open) for further network analyses.\n' \
                  'It can also be opened by graphical vectorial tools such as yED to export ' \
                  'high-resolution plots. -->'
    network_data = OligoNetwork.export_to_graphml(network_dict)
    network_data = xml_header + "\n" + xml_comment + "\n" + network_data
    with open(filename, "w") as out:
        out.write(network_data)


def write_tsv(list_of_dicts, filename, column_names):
    """
    Writes a list of dictionaries to a TSV file with header
    :param list_of_dicts: list of dicts having a fixed set of keys
    :param filename
    :param column_names: list of dict keys to use, can be subset of all the keys
    """
    with open(filename, "w") as out:
        dict_writer = csv.DictWriter(out, column_names, delimiter="\t", extrasaction="ignore")
        dict_writer.writeheader()
        dict_writer.writerows(list_of_dicts)
