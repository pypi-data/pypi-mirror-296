from __future__ import division
from oligopipe.entities import *
import itertools

# predictor features
# the order here determines order of input to the model
# BiolDist as pair feature follows the variant features so added it to that set

VARFEATS = ['CADD1', 'CADD2', 'CADD3', 'CADD4', 'BiolDist']
GENEFEATS = ['ISPP_AR_A', 'ISPP_AR_B', 'ISPP_AD_A', 'ISPP_AD_B', 'ISPP_XL_A', 'HIPred_A', 'HIPred_B', 'dn_ds_A']
PAIRFEATS = ['BP_similarity', 'KG_dist']


# this method is not used anymore, the pairs are created by the input preprocessing (directly in the annotation)
# the GenePairData object also doesn't exist anymore
def create_pair_dict(pairdata):
    """ Takes a list of GenePairData objects and creates a dictionary:
    [(geneA,geneB)]=GenePairData object"""

    pairdict = {}

    for pair in pairdata:
        pairdict[(pair.geneA.gene_name, pair.geneB.gene_name)] = pair

    return pairdict


def create_variant_gene_dict(variants, db_schema):
    """
    :param variants: list of AnnotationData objects
    :param db_schema: "old" or "new", defines whether genes are identified by ENSG or gene name
    :return: variant per gene and zygosity dict as {gene:{hom:[variants],het:[variants],hemi:[variants]}}
    """
    # initiate dictionary
    genevar_dict = {}

    # parse the variants
    for var in variants:
        if db_schema == 'old':
            gene = var.gene.gene_name
        elif db_schema == 'new':
            gene = var.gene.ensembl_gene
        zyg = var.gene_var.zygosity

        # append information to both dictionaries
        if gene not in genevar_dict:

            genevar_dict.update({gene: {'hom': [], 'het': [], 'hemi': []}})

            # append in the heterozygous/homozygous/hemizygous dictionary of the gene

            if zyg in ['hom', 'Hom', 'homozygous', 'Homozygous', 'Homo']:
                genevar_dict[gene]['hom'] += [var]

            elif zyg in ['het', 'Het', 'Heterozygous', 'heterozygous']:
                genevar_dict[gene]['het'] += [var]
            elif zyg in ['hemi', 'Hemi', 'Hemizygous', 'hemizygous', 'hem', 'Hem']:
                genevar_dict[gene]['hemi'] += [var]

        else:

            # append in the heterozygous/homozygous/hemizygous dictionary of the gene
            if zyg in ['hom', 'Hom', 'homozygous', 'Homozygous', 'Homo']:
                genevar_dict[gene]['hom'] += [var]

            elif zyg in ['het', 'Het', 'Heterozygous', 'heterozygous']:
                genevar_dict[gene]['het'] += [var]

            elif zyg in ['hemi', 'Hemi', 'Hemizygous', 'hemizygous', 'hem', 'Hem']:
                genevar_dict[gene]['hemi'] += [var]

    return genevar_dict


def get_compvars(var_list):
    """
    Function that takes a list of heterozygous variants and returns a list 
    of lists with all possible combinations of those variants.
    It orders the variants inside the combination based on CADD score, so that
    the variant with the highest score is appended first.
    """

    combs_list = []

    # iterate over the variants
    for varA, varB in itertools.combinations(var_list, 2):

        # find CADD score
        varA_pred = varA.gene_var.cadd_raw
        varB_pred = varB.gene_var.cadd_raw

        try:
            comb = find_dangerous_allele(varA, varB, varA_pred, varB_pred)
        except ValueError:
            print('##### Check that all CADD scores have a value.')
            print('##### Script is terminated')
            quit()

        combs_list += [comb]

    return combs_list


def find_dangerous_allele(var1, var2, var1_pred, var2_pred):
    """ Function that takes two variants and re-orders their appearance
    based on their pathogenicity prediction. 
    The first variant is the one the highest score.
    """

    # first check values availability
    if var1_pred in ['NULL', 'NaN', 'NA', None] and \
            var2_pred not in ['NULL', 'NaN', 'NA', None]:
        comp_var = [var2, var1]

    elif var2_pred in ['NULL', 'NaN', 'NA', None] and \
            var1_pred not in ['NULL', 'NaN', 'NA', None]:
        comp_var = [var1, var2]

    elif var2_pred in ['NULL', 'NaN', 'NA', None] and \
            var1_pred in ['NULL', 'NaN', 'NA', None]:
        comp_var = [var1, var2]

    else:
        # find most dangerous
        var1_pred = float(var1_pred)
        var2_pred = float(var2_pred)

        most_dangerous = max(var1_pred, var2_pred)

        # create heterozygous compound combination
        if most_dangerous == var1_pred:
            comp_var = [var1, var2]
        else:
            comp_var = [var2, var1]

    return comp_var


def alleles_to_vector(defaults_imputation, comb):
    """
    Function that takes a CombinationData object and returns the vectorised version of it.
    """
    # initiate the vector
    vector = []
    # h = 0  # vector index - not used anymore

    # initiate dictionary with the vector start position of each feature - not used anymore
    # feat_pos_dict = {}

    # collect variant information
    # iterate over the features to vectorize them
    for i in range(len(VARFEATS)):

        # vectorize for CADD1
        if VARFEATS[i] in ['CADD1']:

            try:
                vector += [comb.varA[0].gene_var.cadd_raw]
            except ValueError:
                print('##### CADD1 raw score value is invalid. Please provide a score for CADD for all variants.')
                print('##### Script is terminated')
                quit()

            # save vector position of the feature
            # feat_pos_dict[VARFEATS[i]] = [h, len(vector) - 1]
            # h = len(vector)

        # vectorize for CADD3
        elif VARFEATS[i] in ['CADD3']:

            try:
                vector += [comb.varB[0].gene_var.cadd_raw]
            except ValueError:
                print('##### CADD3 raw score value is invalid. Please provide a score for CADD for all variants.')
                print('##### Script is terminated')
                quit()

            # save vector position of the feature
            # feat_pos_dict[VARFEATS[i]] = [h, len(vector) - 1]
            # h = len(vector)

        # vectorize for CADD2
        elif VARFEATS[i] in ['CADD2']:

            if len(comb.varA) == 1:
                if comb.varA[0].gene_var.zygosity == 'Heterozygous':
                    vector += [-3.0]
                elif comb.varA[0].gene_var.zygosity in ['Homozygous', 'Hemizygous']:
                    try:
                        vector += [comb.varA[0].gene_var.cadd_raw]
                    except ValueError:
                        print('##### CADD2 raw score value is invalid.'
                              ' Please provide a score for CADD for all variants.')
                        print('##### Script is terminated')
                        quit()

            elif len(comb.varA) == 2:
                try:
                    vector += [comb.varA[1].gene_var.cadd_raw]
                except ValueError:
                    print('##### CADD2 raw score value is invalid. Please provide a score for CADD for all variants.')
                    print('##### Script is terminated')
                    quit()

            # save vector position of the feature
            # feat_pos_dict[VARFEATS[i]] = [h, len(vector) - 1]
            # h = len(vector)

        # vectorize for CADD4
        elif VARFEATS[i] in ['CADD4']:

            if len(comb.varB) == 1:
                if comb.varB[0].gene_var.zygosity == 'Heterozygous':
                    vector += [-3.0]
                elif comb.varB[0].gene_var.zygosity in ['Homozygous', 'Hemizygous']:
                    try:
                        vector += [comb.varB[0].gene_var.cadd_raw]
                    except ValueError:
                        print('##### CADD4 raw score value is invalid. '
                              'Please provide a score for CADD for all variants.')
                        print('##### Script is terminated')
                        quit()

            elif len(comb.varB) == 2:
                try:
                    vector += [comb.varB[1].gene_var.cadd_raw]
                except ValueError:
                    print('##### CADD4 raw score value is invalid. Please provide a score for CADD for all variants.')
                    print('##### Script is terminated')
                    quit()

            # save vector position of the feature
            # feat_pos_dict[VARFEATS[i]] = [h, len(vector) - 1]
            # h = len(vector)

        # Biological distance (is a pair feature but handled here to have correct order of features for the model)
        elif VARFEATS[i] == 'BiolDist':

            try:
                if comb.BiolDist in ['N/A', 'NA', 'NaN', 'nan', 'None', None] \
                        or comb.BiolDist == [None] or comb.BiolDist is None:
                    vector += [defaults_imputation["BIOL_DIST"]]
                else:
                    vector += [comb.BiolDist]
            except ValueError:
                print('##### BiolDist is invalid. Please provide a value or write "NA","NaN", or "nan".')
                print('##### Script is terminated')
                quit()

            # save vector position of the feature
            # feat_pos_dict[VARFEATS[i]] = [h, len(vector) - 1]
            # initiate vector index
            # h = len(vector)

    # collect information on genes
    for i in range(len(GENEFEATS)):

        # Autosomal recessive ISPP A
        if GENEFEATS[i] == 'ISPP_AR_A':

            try:
                if comb.varA[0].gene.ISPP_AR in ['N/A', 'NA', 'NaN', 'nan', None] or comb.varA[0].gene.ISPP_AR is None:
                    vector += [defaults_imputation["ISPP_AR_A"]]
                else:
                    vector += [comb.varA[0].gene.ISPP_AR]
            except ValueError:
                print('##### ISPP_AR is invalid. Please provide a value or write "NA","NaN", or "nan".')
                print('##### Script is terminated')
                quit()

            # save vector position of the feature
            # feat_pos_dict[GENEFEATS[i]] = [h, len(vector) - 1]
            # initiate vector index
            # h = len(vector)

        # Autosomal recessive ISPP B
        elif GENEFEATS[i] == 'ISPP_AR_B':

            try:
                if comb.varB[0].gene.ISPP_AR in ['N/A', 'NA', 'NaN', 'nan', None] or comb.varB[0].gene.ISPP_AR is None:
                    vector += [defaults_imputation["ISPP_AR_B"]]
                else:
                    vector += [comb.varB[0].gene.ISPP_AR]
            except ValueError:
                print('##### ISPP_AR is invalid. Please provide a value or write "NA","NaN", or "nan".')
                print('##### Script is terminated')
                quit()

            # save vector position of the feature
            # feat_pos_dict[GENEFEATS[i]] = [h, len(vector) - 1]
            # initiate vector index
            # h = len(vector)

        # Autosomal dominant ISPP A
        elif GENEFEATS[i] == 'ISPP_AD_A':

            try:
                if comb.varA[0].gene.ISPP_AD in ['N/A', 'NA', 'NaN', 'nan', None] or comb.varA[0].gene.ISPP_AD is None:
                    vector += [defaults_imputation["ISPP_AD_A"]]
                else:
                    vector += [comb.varA[0].gene.ISPP_AD]
            except ValueError:
                print('##### ISPP_AD is invalid. Please provide a value or write "NA","NaN", or "nan".')
                print('##### Script is terminated')
                quit()

            # save vector position of the feature
            # feat_pos_dict[GENEFEATS[i]] = [h, len(vector) - 1]
            # initiate vector index
            # h = len(vector)

        # Autosomal dominant ISPP B
        elif GENEFEATS[i] == 'ISPP_AD_B':

            try:
                if comb.varB[0].gene.ISPP_AD in ['N/A', 'NA', 'NaN', 'nan', None] or comb.varB[0].gene.ISPP_AD is None:
                    vector += [defaults_imputation["ISPP_AD_B"]]
                else:
                    vector += [comb.varB[0].gene.ISPP_AD]
            except ValueError:
                print('##### ISPP_AD is invalid. Please provide a value or write "NA","NaN", or "nan".')
                print('##### Script is terminated')
                quit()

            # save vector position of the feature
            # feat_pos_dict[GENEFEATS[i]] = [h, len(vector) - 1]
            # initiate vector index
            # h = len(vector)

        # X-linked ISPP A
        elif GENEFEATS[i] == 'ISPP_XL_A':

            try:
                if not comb.varA[0].gene_var.chr == "X":
                    vector += [-0.500]
                elif comb.varA[0].gene.ISPP_XL in ['N/A', 'NA', 'NaN', 'nan', None] or comb.varA[0].gene.ISPP_XL is None:
                    vector += [defaults_imputation["ISPP_XL"]]
                else:
                    vector += [comb.varA[0].gene.ISPP_XL]
            except ValueError:
                print('##### ISPP_XL is invalid. Please provide a value or write "NA","NaN", or "nan".')
                print('##### Script is terminated')
                quit()

            # save vector position of the feature
            # feat_pos_dict[GENEFEATS[i]] = [h, len(vector) - 1]
            # initiate vector index
            # h = len(vector)

        #  Haploinsufficiency A
        elif GENEFEATS[i] == 'HIPred_A':

            try:
                if comb.varA[0].gene.HIPred in ['N/A', 'NA', 'NaN', 'nan', None] or comb.varA[0].gene.HIPred is None:
                    vector += [defaults_imputation["HIPRED_A"]]
                else:
                    vector += [comb.varA[0].gene.HIPred]
            except ValueError:
                print('##### HIPred is invalid. Please provide a value or write "NA","NaN", or "nan".')
                print('##### Script is terminated')
                quit()

            # save vector position of the feature
            # feat_pos_dict[GENEFEATS[i]] = [h, len(vector) - 1]
            # initiate vector index
            # h = len(vector)

        #  Haploinsufficiency B
        elif GENEFEATS[i] == 'HIPred_B':

            try:
                if comb.varB[0].gene.HIPred in ['N/A', 'NA', 'NaN', 'nan', None] or comb.varB[0].gene.HIPred is None:
                    vector += [defaults_imputation["HIPRED_B"]]
                else:
                    vector += [comb.varB[0].gene.HIPred]
            except ValueError:
                print('##### HIPred is invalid. Please provide a value or write "NA","NaN", or "nan".')
                print('##### Script is terminated')
                quit()

            # save vector position of the feature
            # feat_pos_dict[GENEFEATS[i]] = [h, len(vector) - 1]
            # initiate vector index
            # h = len(vector)

        #  Selection pressure A
        elif GENEFEATS[i] == 'dn_ds_A':

            try:
                if comb.varA[0].gene.dn_ds in ['N/A', 'NA', 'NaN', 'nan', None] or comb.varA[0].gene.dn_ds is None:
                    vector += [defaults_imputation["DN_DS"]]
                else:
                    vector += [comb.varA[0].gene.dn_ds]
            except ValueError:
                print('##### dn_ds is invalid. Please provide a value or write "NA","NaN", or "nan".')
                print('##### Script is terminated')
                quit()

            # save vector position of the feature
            # feat_pos_dict[GENEFEATS[i]] = [h, len(vector) - 1]
            # initiate vector index
            # h = len(vector)

    # collect information on pairs info
    for i in range(len(PAIRFEATS)):

        # Biological distance: handled within VARFEATS above

        # Knowledge graph distance
        if PAIRFEATS[i] == 'KG_dist':

            try:
                if comb.KG_dist in ['N/A', 'NA', 'NaN', 'nan', 'None', None] \
                        or comb.KG_dist == [None] or comb.KG_dist is None:
                    vector += [defaults_imputation["KG_DIST"]]
                else:
                    vector += [comb.KG_dist]
            except ValueError:
                print('##### KG_dist is invalid. Please provide a value or write "NA","NaN", or "nan".')
                print('##### Script is terminated')
                quit()

            # save vector position of the feature
            # feat_pos_dict[PAIRFEATS[i]] = [h, len(vector) - 1]
            # initiate vector index
            # h = len(vector)

        # BP terms similarity
        elif PAIRFEATS[i] == 'BP_similarity':

            try:
                if comb.KG_dist in ['N/A', 'NA', 'NaN', 'nan', 'None', None] or \
                        comb.BP_similarity == [None] or comb.BP_similarity is None:
                    vector += [defaults_imputation["BP_SIM"]]
                else:
                    vector += [comb.BP_similarity]
            except ValueError:
                print('##### BP_similarity is invalid. Please provide a value or write "NA","NaN", or "nan".')
                print('##### Script is terminated')
                quit()

            # save vector position of the feature
            # feat_pos_dict[PAIRFEATS[i]] = [h, len(vector) - 1]
            # initiate vector index
            # h = len(vector)

    return vector


def same_variant(varA, varB, comp_varsA, comp_varsB):
    """
    Check if two variants (or more precisely two sets of variants, to handle compound heterozygous) are the same.
    :param varA: a set of variant A
    :param varB: a set of variant B
    :param comp_varsA: list of compound het A
    :param comp_varsA: list of compound het B
    :return: True if a variant in varA is also found in varB, False otherwise.
    """
    vsA = varA if varA in comp_varsA else [varA]
    vsB = varB if varB in comp_varsB else [varB]

    for vA in vsA:
        for vB in vsB:
            if vA == vB:
                return True
    return False


def create_combinations(geneA, geneB, pair_feats, comb_id, d, defaults_imputation, counter=None):
    """
    For a given pair of genes, create and annotate all possible variant combinations

    :param geneA / geneB: gene name (old DB schema) or ENSG (new DB schema)
    :param pair_feats: dict containing the gene pair features for this gene
    :param comb_id: combination ID
    :param d: variants per gene and zygosity as {gene:{hom:[variants],het:[variants],hemi:[variants]}}
                with each variant = AnnotationData object
    :param defaults_imputation: dict with the defaults of the features (for imputation of missing values)
    :param counter: only for HOP, in order to run VarCoPP on chunks of variant combinations
    :return: yields CombinationData objects for this pair, as well as the incremented comb_id (and counter)
    """
    if d.get(geneA) is not None and d.get(geneB) is not None:
        # categorize and collect variants
        homvarsA = []
        homvarsB = []
        hetvarsA = []
        hetvarsB = []
        hemivarsA = []
        hemivarsB = []
        comp_varsA = []
        comp_varsB = []

        if len(d[geneA]['hom']) > 0:
            for el in d[geneA]['hom']:
                homvarsA += [el]
        if len(d[geneA]['het']) > 0:
            for el in d[geneA]['het']:
                hetvarsA += [el]
        if len(d[geneA]['hemi']) > 0:
            for el in d[geneA]['hemi']:
                hemivarsA += [el]
        if len(d[geneB]['hom']) > 0:
            for el in d[geneB]['hom']:
                homvarsB += [el]
        if len(d[geneB]['het']) > 0:
            for el in d[geneB]['het']:
                hetvarsB += [el]
        if len(d[geneB]['hemi']) > 0:
            for el in d[geneB]['hemi']:
                hemivarsB += [el]

        # create heterozygous compound variants and order based on CADD
        if len(d[geneA]['het']) > 1:
            comp_varsA = get_compvars(d[geneA]['het'])
        if len(d[geneB]['het']) > 1:
            comp_varsB = get_compvars(d[geneB]['het'])

        # combine all variants A (list of AnnotationData objects)
        # include the heterozygous variants only through the compound heterozygous pairs
        # (unless there is only one heterozyg variant in the gene)
        if len(d[geneA]['het']) > 1:
            varsA = homvarsA + comp_varsA + hemivarsA
        else:
            varsA = homvarsA + hetvarsA + hemivarsA

        # iterate variants A
        for varA in varsA:
            if len(d[geneB]['het']) > 1:
                varsB = homvarsB + comp_varsB + hemivarsB
            else:
                varsB = homvarsB + hetvarsB + hemivarsB

            for varB in varsB:

                # Handle case where a variant is duplicated because of association with 2 different canonical
                # transcripts (and two different gene names).
                # This happens for example when the variant is at a position where there is 1 gene on strand
                # + and another gene on strand -.
                # We don't want to create a pair with the same variant in this case.
                if same_variant(varA, varB, comp_varsA, comp_varsB):
                    print(f"Skipping {varA} - {varB}")
                    continue

                # create CombinationData object
                comb = CombinationData(geneA, geneB, comb_id)

                if varA in comp_varsA:
                    comb.varA = varA
                else:
                    comb.varA = [varA]

                if varB in comp_varsB:
                    comb.varB = varB
                else:
                    comb.varB = [varB]

                # append pair features
                comb.BiolDist = pair_feats["biol_dist"]
                comb.BP_similarity = pair_feats["BP_similarity"]
                comb.KG_dist = pair_feats["KG_dist"]

                # transform combination to vector
                vector_comb = alleles_to_vector(defaults_imputation, comb)
                comb.vectorcomb = vector_comb

                comb_id += 1
                if counter is not None:  # in case of HOP; the incremented counter needs to be returned as well
                    counter += 1
                    output = (comb, comb_id, counter)
                else:                    # simple prediction case
                    output = (comb, comb_id)
                yield output


def transform_data(defaults_imputation, pairs, variants, db_schema):
    """
    Transform annotated data to vectors for prediction by creating all possible digenic combinations

    :param defaults_imputation: dict with the defaults of the features (for imputation of missing values)
    :param pairs: dictionary of (RVIS-sorted) gene pairs with their annotations,
                generated in VarcoppPreprocessPipeline.execute()
    :param variants: list of AnnotationData objects
    :param db_schema: 'old' or 'new', defines whether genes are identified by ENSG or gene name
    :return: combinations: dictionary of Combination objects
             combination_vectors: dictionary {comb_id: comb_vct}
    """
    combinations = {}
    combination_vectors = {}  # this removes reiterating the combinations to get the vectors for predictions afterwards

    # create dictionary of variants per gene and per zygosity
    variants_per_gene = create_variant_gene_dict(variants, db_schema)
    # track ID of digenic combination
    comb_id = 0

    # start iterating over the pairs
    for pair in pairs:
        geneA, geneB = pair[0], pair[1]
        pair_feats = pairs[(geneA, geneB)]
        for combination, comb_id in create_combinations(geneA, geneB, pair_feats, comb_id, variants_per_gene,
                                                        defaults_imputation):
            combinations[comb_id] = combination
            combination_vectors[comb_id] = combination.vectorcomb
    return combinations, combination_vectors


def filter_with_parents(child, mom, dad):
    """
    This scripts implies that we have the combinations of mom and dad in addition to the child combinations
    :param child: combination lists of the child
    :param mom: combination list of mom
    :param dad: combination list of dad
    :return: combination list of child without any combination present in the parents
    """
    filtered_combinations = []
    for comb in child:
        if comb not in mom and comb not in dad:
            filtered_combinations.append(comb)
    return filtered_combinations


def get_flatten_combination_data(varcopp_result, comb_id):
    comb_result = varcopp_result["combinations"][comb_id]
    for var in ["varA", "varB"]:
        ensembl_gene = comb_result[var]["ensembl_gene"]
        comb_result[var]["gene"] = varcopp_result["genes"][ensembl_gene]
        comb_result[var]["gene"]["ensembl_gene"] = ensembl_gene
        comb_result[var]["variants"] = [varcopp_result["variants"][variant_id] for variant_id in
                                           comb_result[var]["variants"]]
    return comb_result
