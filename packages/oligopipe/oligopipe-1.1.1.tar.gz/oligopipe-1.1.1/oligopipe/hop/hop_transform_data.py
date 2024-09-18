from __future__ import division
from oligopipe.varcopp.transform_data import create_variant_gene_dict, create_combinations


def chunked_transform_data(defaults_imputation, pairs, variants, db_schema, chunk_length):
    """
    Creates chunks of digenic combinations and their feature vector to be passed to VarCoPP (by re-using original code)

    :param defaults_imputation: dict with the defaults of the features (for imputation of missing values)
    :param pairs: dictionary of (RVIS-sorted) gene pairs with their annotations,
                generated in HOPPreprocessPipeline.execute()
    :param variants: list of AnnotationData objects
    :param db_schema: 'old' or 'new', defines whether genes are identified by ENSG or gene name
    :param chunk_length: number of combinations to include in a chunk
    :return: yields (per chunk) combinations: dictionary of Combination objects
                              combination_vectors: dictionary {comb_id: comb_vct}
    """
    combinations = {}
    combination_vectors = {}  # this removes reiterating the combinations to get the vectors for predictions afterwards

    # create dictionary of variants per gene and per zygosity
    variants_per_gene = create_variant_gene_dict(variants, db_schema)
    # track ID of digenic combination and counter
    comb_id = 0
    counter = 0

    # start iterating over the pairs
    for pair in pairs:
        geneA, geneB = pair[0], pair[1]
        pair_feats = pairs[(geneA, geneB)]
        for combination, comb_id, counter in create_combinations(geneA, geneB, pair_feats, comb_id, variants_per_gene,
                                                        defaults_imputation, counter):
            combinations[comb_id] = combination
            combination_vectors[comb_id] = combination.vectorcomb

            if counter == chunk_length:
                counter = 0
                yield combinations, combination_vectors
                combinations = {}
                combination_vectors = {}
    yield combinations, combination_vectors
