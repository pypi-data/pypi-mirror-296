from collections import defaultdict
import traceback


def varcopp_post_filtering(varcopp_result, min_threshold):
    """
    (Only for web app) Filter the results based on a threshold
    :param varcopp_result: JSON representing VarCoPPResults instance
    :param min_threshold: threshold for the VarCoPP score to filter on
    :return: updated JSON
    """
    stat_dict = defaultdict(dict)
    stat_dict["var_combinations"] = defaultdict(int)
    stat_dict_tmp = {"gene_combinations": defaultdict(set), "genes": defaultdict(set)}
    filtered_result = {"genes": {}, "variants": {}, "combinations": {}, "stats": {},
                       "metadata": varcopp_result["metadata"]}
    try:
        if min_threshold:
            min_threshold = float(min_threshold)
            if min_threshold > 0:
                for comb_key, combination in varcopp_result["combinations"].items():
                    if (combination["confidence_zone"] is not None and float(
                            combination["confidence_zone"].split('%')[0]) >= min_threshold) or \
                            (min_threshold == 50 and combination["prediction"] == "Disease-causing"):
                        filtered_result["combinations"][comb_key] = combination
                        for var in ["varA", "varB"]:
                            for variant in combination[var]["variants"]:
                                filtered_result["variants"][variant] = varcopp_result["variants"][variant]
                            ensembl_gene = combination[var]["ensembl_gene"]
                            filtered_result["genes"][ensembl_gene] = varcopp_result["genes"][ensembl_gene]
                        comb_class = combination["prediction"] + (
                            "_" + combination["confidence_zone"] if combination["confidence_zone"] is not None else "")
                        stat_dict["var_combinations"][comb_class] += 1
                        stat_dict_tmp["gene_combinations"][comb_class].add(
                            combination["varA"]["ensembl_gene"] + combination["varB"]["ensembl_gene"])
                        stat_dict_tmp["genes"][comb_class].add(combination["varA"]["ensembl_gene"])
                        stat_dict_tmp["genes"][comb_class].add(combination["varB"]["ensembl_gene"])

                prev_class_stat = {}
                for stat_type in ["genes", "gene_combinations"]:
                    if stat_type not in prev_class_stat:
                        prev_class_stat[stat_type] = set()
                    for comb_class in ["Disease-causing_99.9%-zone", "Disease-causing_99%-zone", "Disease-causing",
                                       "Neutral"]:
                        stat_for_comb_class = stat_dict_tmp[stat_type][comb_class]
                        stat_dict[stat_type][comb_class] = {}
                        stat_dict[stat_type][comb_class]["all"] = len(stat_for_comb_class)
                        stat_dict[stat_type][comb_class]["diff_with_higher_conf"] = len(
                            stat_for_comb_class - prev_class_stat[stat_type]) if len(
                            prev_class_stat[stat_type]) > 0 else None
                        prev_class_stat[stat_type] = stat_for_comb_class | prev_class_stat[stat_type]
                stat_dict["variant_count"] = len(filtered_result["variants"])
                filtered_result["stats"] = dict(stat_dict)
                return filtered_result
    except Exception as e:
        raise Exception("{0} - {1}".format(e, traceback.format_exc()))
    return varcopp_result

