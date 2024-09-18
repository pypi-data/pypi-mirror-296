from scipy.stats import rankdata


def filter_set(combinations, filtered_combinations, N):
    """
    Merges a set of predicted combinations with the current filtered set and retains only the top N based on final score
    (Is iteratively applied to all chunks of combinations predicted by VarCoPP)
    :param combinations: new set of combinations as dict {comb_id: CombinationData}
    :param filtered_combinations: current filtered result set as dict {comb_id: CombinationData}
    :param N: number of combinations to retain
    :return: new filtered set as dict {comb_id: CombinationData}
    """
    combinations.update(filtered_combinations)
    min_final_score = sorted([c.hop_final_score for c in combinations.values()], reverse=True)[
        min([len(combinations.values()), N])-1]
    filtered_combinations = {c: comb for c, comb in combinations.items() if comb.hop_final_score >= min_final_score}
    return filtered_combinations


def rank_all(filtered_combinations):
    """
    Adds HOP final rank to every combination and sorts all combinations based on the rank
    :param filtered_combinations: set of combinations left after HOP filtering as dict {comb_id: CombinationData}
    :return: dict {comb_id: CombinationData} sorted by ascending rank of the combination
    """
    final_scores = [c.hop_final_score for c in filtered_combinations.values()]
    ranks = rankdata([-1 * i for i in final_scores])
    rank_dict = {score: r for score, r in zip(final_scores, ranks)}
    for c in filtered_combinations.values():
        c.hop_rank = int(rank_dict[c.hop_final_score])
    sorted_combs = {c_id: comb for c_id, comb in sorted(filtered_combinations.items(),
                                                        key=lambda item: item[1].hop_rank)}
    return sorted_combs
