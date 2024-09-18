"""Given parsed inputs in an "options" dictionary and results from VarCoPP prediction or prioritization pipeline,
Print the different outputs to a file."""
import logging
import os

import numpy as np

from oligopipe.cli_utils import set_outdir, create_out_filename, write_txt, write_tsv, write_json, write_graphml

logger = logging.getLogger(__name__)


class ResultsPrinter:
    """
    Writes the results to different output files:
    - Discarded variants (if applicable): filtered_variants.txt, invalid_zygosity_variants.txt,
                                          missing_variants.txt
    - gene_pairs.tsv
    - predicted_variant_combinations.tsv
    - predictions_with_annotations.json
    - (oligogenic_network.graphml - only for prediction)
    - metadata.json (includes some statistics)
    """
    def __init__(self, options):
        """
        :param options dictionary of loaded arguments from input
        """
        self.options = options
        self.outdir = set_outdir(options["outdir"], options["force"])
        self.prefix = options["prefix"]

    def execute(self, results, prioritize=False):
        """
        Checks which type of outputs are given (based on the specific pipeline that was run) and prints them accordingly
        :param results: dictionary with the different outputs from the pipeline
        """
        if "discarded_vars" in results:
            self.print_discarded_vars(results["discarded_vars"])
        if "metadata" in results and "result_json" in results and not prioritize:
            updated_metadata = self.print_results(results["result_json"], results["metadata"])
            self.print_metadata(updated_metadata)
        if "metadata" in results and "result_json" in results and prioritize:
            updated_metadata = self.print_results_hop(results["result_json"], results["metadata"])
            self.print_metadata(updated_metadata)
        if "network" in results:
            self.print_network(results["network"])
        logger.info(f"Created result files in directory '{self.outdir}'.")

    def print_discarded_vars(self, discarded_vars):
        """
        Prints (if applicable): filtered_variants.txt, invalid_zygosity_variants.txt, missing_variants.txt
        :param discarded_vars: dict for the 3 types of discarded vars ("missing" / "filtered" / "invalid_zygosity"),
                                values are a list of variants
        """
        if discarded_vars["missing"]:
            missing_file = os.path.join(self.outdir, create_out_filename("missing_variants.txt", self.prefix))
            write_txt(discarded_vars["missing"], missing_file)
        if discarded_vars["filtered"]:
            filtered_file = os.path.join(self.outdir, create_out_filename("filtered_variants.txt", self.prefix))
            write_txt(discarded_vars["filtered"], filtered_file)
        if discarded_vars["invalid_zygosity"]:
            invalid_zyg_file = os.path.join(self.outdir,
                                            create_out_filename("invalid_zygosity_variants.txt", self.prefix))
            write_txt(discarded_vars["invalid_zygosity"], invalid_zyg_file)

    def print_results(self, result_json, metadata):
        """
        Reformats the results into a gene pair and variant combination table, and prints
             predicted_variant_combinations.tsv, gene_pairs.tsv and predictions_with_annotations.json
        (Also updates the metadata with some statistics)
        :param result_json: VarCoPPResults/HOPResults instance as JSON
        :param metadata
        :return updated metadata
        """
        combs, gene_pairs = self.get_pairs_combinations(result_json)  # lists of dicts
        metadata["nb_variant_combinations"] = len(combs)
        metadata["nb_gene_pairs"] = len(gene_pairs)
        metadata["variants_analysed"] = result_json["stats"]["variant_count"]

        # combinations table
        if len(combs) > 0:
            combs_table_file = os.path.join(self.outdir,
                                            create_out_filename("predicted_variant_combinations.tsv", self.prefix))
            write_tsv(combs, combs_table_file, column_names=combs[0].keys())

        # gene pair table
        if len(gene_pairs) > 0:
            gene_pair_file = os.path.join(self.outdir, create_out_filename("predicted_gene_pairs.tsv", self.prefix))
            write_tsv(gene_pairs, gene_pair_file, column_names=["GeneA", "GeneB", "Nb_combs", "Nb_dis_causing",
                                                                "Pct_pathogenic_combs", "Median_pathogenicity_score"])

        # raw JSON including feature annotations
        result_path = os.path.join(self.outdir, create_out_filename("predictions_with_annotations.json", self.prefix))
        write_json(result_json, result_path)
        return metadata

    def print_results_hop(self, result_json, metadata):
        """
        Reformats the results into a gene pair and variant combination table, and prints
             predicted_variant_combinations.tsv, gene_pairs.tsv and predictions_with_annotations.json
        (Also updates the metadata with some statistics)
        :param result_json: VarCoPPResults/HOPResults instance as JSON
        :param metadata
        :return updated metadata
        """
        combs, gene_pairs = self.get_pairs_combinations(result_json, True)  # lists of dicts
        metadata["nb_variant_combinations"] = len(combs)
        metadata["nb_gene_pairs"] = len(gene_pairs)
        metadata["variants_analysed"] = result_json["stats"]["variant_count"]

        # combinations table
        if len(combs) > 0:
            combs_table_file = os.path.join(self.outdir,
                                            create_out_filename("predicted_variant_combinations.tsv", self.prefix))
            write_tsv(combs, combs_table_file, column_names=combs[0].keys())

        # raw JSON including feature annotations
        result_path = os.path.join(self.outdir, create_out_filename("predictions_with_annotations.json", self.prefix))
        write_json(result_json, result_path)
        return metadata

    def print_metadata(self, metadata):
        """
        Prints metadata.json which includes job input information and some statistics
        :param metadata
        """
        metadata["patient_info"] = metadata["patient_info"].to_dict()
        metadata_file = os.path.join(self.outdir, create_out_filename("metadata.json", self.prefix))
        write_json(metadata, metadata_file)

    def print_network(self, network):
        """
        Prints oligogenic_network.graphml
        :param network: dictionary representing an OligoNetwork object (from get_graph())
        """
        if len(network) > 0:
            network_file = os.path.join(self.outdir, create_out_filename("oligogenic_network.graphml", self.prefix))
            write_graphml(network, network_file)

    @staticmethod
    def get_pairs_combinations(result_json, prioritize=False):
        """
        Uses the JSON output to format a list of predicted gene pairs
        and variant combinations to print to output
        :param result_json: VarCoPPResults/HOPResults instance as JSON generated by Pipeline.execute()
        :return: two lists of dictionaries with
                 keys for gene pairs: GeneA, GeneB, Nb_combs, Nb_dis_causing, VarCoPP_scores,
                                      Pct_pathogenic_combs, Median_pathogenicity_score
                 keys for variant combinations: GeneA, GeneB, GeneA_alleles, GeneA_zygosities, GeneB_alleles,
                                                GeneB_zygosities, VarCoPP_score, Prediction, Confidence_zone,
                                                (DE_prediction), (Varcopp_feature_contributions)

        """
        combs = []
        gene_pairs = {}

        gene_map = {ensg: gene["gene_name"] for ensg, gene in result_json["genes"].items()}

        for comb in result_json["combinations"].values():
            ensgA = comb["varA"]["ensembl_gene"]
            ensgB = comb["varB"]["ensembl_gene"]
            nameA = gene_map[ensgA]
            nameB = gene_map[ensgB]

            if prioritize:
                comb_dict = {
                    "GeneA": ensgA + '-' + nameA,
                    "GeneB": ensgB + '-' + nameB,
                    "GeneA_alleles": ';'.join(comb["varA"]["variants"]),
                    "GeneA_zygosities": ';'.join(comb["varA"]["zygosities"]),
                    "GeneB_alleles": ';'.join(comb["varB"]["variants"]),
                    "GeneB_zygosities": ';'.join(comb["varB"]["zygosities"]),
                    "VarCoPP_score": comb["varcopp_score"],
                    "Prediction": comb["prediction"],
                    "Confidence_zone": comb["confidence_zone"],
                    "HOP_Disease_relevance_Score": comb['hop_disease_score'],
                    "Hop_Final_Score": comb['hop_final_score'],
                    "Hop_Rank":comb['hop_rank']
                }
            else:
                comb_dict = {
                    "GeneA": ensgA + '-' + nameA,
                    "GeneB": ensgB + '-' + nameB,
                    "GeneA_alleles": ';'.join(comb["varA"]["variants"]),
                    "GeneA_zygosities": ';'.join(comb["varA"]["zygosities"]),
                    "GeneB_alleles": ';'.join(comb["varB"]["variants"]),
                    "GeneB_zygosities": ';'.join(comb["varB"]["zygosities"]),
                    "VarCoPP_score": comb["varcopp_score"],
                    "Prediction": comb["prediction"],
                    "Confidence_zone": comb["confidence_zone"]
                }
            # if self.options["digenic_effect"]:
            #     comb_dict["DE_prediction"] = comb["de_prediction"]
            # if self.options["calc_contrib"]:
            #     comb_dict["Varcopp_feature_contributions"] = comb["feature_contributions"]
            combs.append(comb_dict)

            pair_key = ensgA + "_" + ensgB
            if pair_key not in gene_pairs:
                gene_pairs[pair_key] = {
                    "GeneA": ensgA + '-' + nameA,
                    "GeneB": ensgB + '-' + nameB,
                    "Nb_combs": 1,
                    "Nb_dis_causing": 1 if comb["prediction"] == "Disease-causing" else 0,
                    "VarCoPP_scores": [comb["varcopp_score"]]
                }
            else:
                gene_pairs[pair_key]["Nb_combs"] += 1
                gene_pairs[pair_key]["Nb_dis_causing"] += 1 if comb["prediction"] == "Disease-causing" else 0
                gene_pairs[pair_key]["VarCoPP_scores"].append(comb["varcopp_score"])

        for gene_pair in gene_pairs.values():
            gene_pair["Pct_pathogenic_combs"] = round(gene_pair["Nb_dis_causing"] * 100 / gene_pair["Nb_combs"], 2)
            gene_pair["Median_pathogenicity_score"] = round(np.median(gene_pair["VarCoPP_scores"]), 2)
        return combs, list(gene_pairs.values())


