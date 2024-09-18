def compute_hop_scores(combinations, rwr_results, max_pair, min_pair):
    for comb in combinations.values():
        ensgA = comb.varA[0].gene.ensembl_gene
        ensgB = comb.varB[0].gene.ensembl_gene
        disease_score = (rwr_results.get(ensgA, 0) + rwr_results.get(ensgB, 0)) / 2
        comb.hop_disease_score = (disease_score - min_pair) / (max_pair - min_pair)
        comb.hop_final_score = (comb.varcopp_score + comb.hop_disease_score) / 2
    return combinations
