import re
from collections import defaultdict

from oligopipe.varcopp.post_filtering import varcopp_post_filtering


class InputData:
    def __init__(self, patient_information, annotated_variants, gene_pairs):
        self.patient_information = patient_information
        self.annotated_variants = annotated_variants
        self.gene_pairs = gene_pairs

    def __repr__(self):
        return str(self.__dict__)


class VarCoPPInputData(InputData):
    pass


class HOPInputData(InputData):
    def __init__(self, patient_information, annotated_variants, gene_pairs, seeds, N):
        super().__init__(patient_information, annotated_variants, gene_pairs)
        self.seeds = seeds  # TODO make class seed?
        self.output_nb = N  # Number of top combinations to return


class Results:
    def __init__(self, digenic_combinations):
        self.digenic_combinations = digenic_combinations

    def gene_var_to_repr(self, gene_var):
        return ":".join(str(e) for e in [gene_var.chr, gene_var.pos, gene_var.ref, gene_var.alt])

    def to_dict_vec(self):
        """
        :return: json representation of results (keys: stats, genes, variants, combinations)
            The "stats" show the "variant_count" as well as a summary per category ("genes", "variant_combinations",
            "gene_combinations") and per confidence zone of the VarCoPP prediction ("Disease-causing_99.9%-zone",
            "Disease-causing_99%-zone", "Disease-causing", "Neutral"). For "genes" and "gene_combinations"
            the statistics are shown as "all" and "diff_with_higher_conf" (how many cases does the current confidence
            zone have more than the higher one?) for later filtering purposes.
            For HOPResults objects, the combinations are shown in ranked order
            and additionally contain the HOP related features.
        """
        combination_dict = {}
        gene_dict = {}
        variant_dict = {}
        stat_dict = {"var_combinations": defaultdict(int), "gene_combinations": defaultdict(set),
                     "genes": defaultdict(set)}

        for comb_id in self.digenic_combinations:

            c = self.digenic_combinations[comb_id]

            var_A_variants = [self.gene_var_to_repr(v.gene_var) for v in c.varA]
            var_A_zygosities = [v.gene_var.zygosity for v in c.varA]
            var_B_variants = [self.gene_var_to_repr(v.gene_var) for v in c.varB]
            var_B_zygosities = [v.gene_var.zygosity for v in c.varB]

            for gene in [c.varA[0].gene, c.varB[0].gene]:
                gene_dict[gene.ensembl_gene] = {
                    'gene_name': gene.gene_name,
                    'uniprot_id': gene.uniprot_id,
                    'P_HI': gene.P_HI,
                    'P_rec': gene.P_rec,
                    'GDI': gene.GDI,
                    'RVIS': gene.RVIS,
                    'dn_ds': gene.dn_ds,
                    'HIPred': gene.HIPred,
                    'ISPP_AR': gene.ISPP_AR,
                    'ISPP_AD': gene.ISPP_AD,
                    'ISPP_XL': gene.ISPP_XL
                }

            for variants in [c.varA, c.varB]:
                for variant in variants:
                    variant = variant.gene_var
                    variant_dict[self.gene_var_to_repr(variant)] = {
                        "chr": variant.chr,
                        "pos": variant.pos,
                        "ref": variant.ref,
                        "alt": variant.alt,
                        "zygosity": variant.zygosity,
                        "aapos": variant.aapos,
                        "aaref": variant.aaref,
                        "aaalt": variant.aaalt,
                        "cdnapos": variant.cdnapos,
                        "ensembl_transcriptid": variant.ensembl_transcriptid,
                        "fl_diff": variant.fl_diff,
                        "h_diff": variant.h_diff,
                        "maf": variant.maf,
                        "cadd_raw": variant.cadd_raw
                    }

            minimal_combination = {
                "varcopp_score": c.varcopp_score,
                "prediction": c.prediction,
                "confidence_zone": c.confidence_zone,
                "vectorcomb": c.vectorcomb,
                "BiolDist": c.BiolDist,
                "KG_dist": c.KG_dist,
                "BP_similarity": c.BP_similarity,
                "varA": {
                    "ensembl_gene": c.varA[0].gene.ensembl_gene,
                    "variants": var_A_variants,
                    "zygosities": var_A_zygosities
                },
                "varB": {
                    "ensembl_gene": c.varB[0].gene.ensembl_gene,
                    "variants": var_B_variants,
                    "zygosities": var_B_zygosities
                }
            }

            if isinstance(self, HOPResults):
                minimal_combination["hop_disease_score"] = round(c.hop_disease_score, 3)
                minimal_combination["hop_final_score"] = round(c.hop_final_score, 3)
                minimal_combination["hop_rank"] = c.hop_rank

            combination_dict[str(comb_id)] = minimal_combination
            comb_class = c.prediction + ("_" + c.confidence_zone if c.confidence_zone is not None else "")
            stat_dict["var_combinations"][comb_class] += 1
            stat_dict["gene_combinations"][comb_class].add(c.varA[0].gene.ensembl_gene+c.varB[0].gene.ensembl_gene)
            stat_dict["genes"][comb_class].add(c.varA[0].gene.ensembl_gene)
            stat_dict["genes"][comb_class].add(c.varB[0].gene.ensembl_gene)

        prev_class_stat = {}
        for stat_type in ["genes", "gene_combinations"]:
            if stat_type not in prev_class_stat:
                prev_class_stat[stat_type] = set()
            for comb_class in ["Disease-causing_99.9%-zone", "Disease-causing_99%-zone", "Disease-causing", "Neutral"]:
                stat_for_comb_class = stat_dict[stat_type][comb_class]
                stat_dict[stat_type][comb_class] = {}
                stat_dict[stat_type][comb_class]["all"] = len(stat_for_comb_class)
                stat_dict[stat_type][comb_class]["diff_with_higher_conf"] = len(stat_for_comb_class - prev_class_stat[stat_type]) if len(prev_class_stat[stat_type]) > 0 else None
                prev_class_stat[stat_type] = stat_for_comb_class | prev_class_stat[stat_type]

        stat_dict["variant_count"] = len(variant_dict)
        result = {
            "stats": stat_dict,
            "genes": gene_dict,
            "variants": variant_dict,
            "combinations": combination_dict
        }
        return result


class VarCoPPResults(Results):

    @staticmethod
    def post_filter(varcopp_result, threshold):
        """
        Filter VarCoPP results
        :param varcopp_result: JSON
        :param threshold: pathogenicity threshold to apply filtering of the digenic combinations (int 0-100)
        :return: filtered result JSON
        """
        return varcopp_post_filtering(varcopp_result, threshold)


class HOPResults(Results):
    pass


class CombinationData:
    def __init__(self, geneA=None, geneB=None, combid=None):
        self.geneA = geneA
        self.geneB = geneB
        self.BiolDist = None
        self.KG_dist = None
        self.BP_similarity = None
        self.Pathway = None
        self.varA = None #list of variants (max.2 for heterozygous compound)
        self.varB = None #list of variants (max.2 for heterozygous compound)
        self.vectorcomb = None
        self.varcopp_score = None
        self.prediction = None
        self.confidence_zone = None
        self.hop_disease_score = None
        self.hop_final_score = None
        self.hop_rank = None
        self.combid = combid

    def __iter__(self):
        for attr, value in self.__dict__.items():
            if attr in ["geneA","geneB"]:
                value = value.__dict__
            elif attr in ["varA","varB"]:
                for i in range(len(value)):
                    value[i] = dict(value[i])

            yield attr, value

    def __eq__(self, other):
        equal = True
        if self.geneA == other.geneA:
            if self.geneB == other.geneB:
                if len(self.varA) == len(other.varA):
                    if len(self.varB) == len(other.varB):
                        for var in self.varA:
                            if var not in other.varA:
                                equal = False
                        for var in self.varB:
                            if var not in other.varB:
                                equal = False
                    else:
                        equal = False
                else:
                    equal = False
            else:
                equal = False
        else:
            equal = False
        return equal

    def to_dict_vec(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_") and v is not None}


class PatientInformation:
    def __init__(self, id, sex):
        self.id = id
        self.sex = sex

    def __repr__(self):
        return str(self.__dict__)

    def to_dict(self):
        return self.__dict__


class Variant:
    def __init__(self, chr, pos, ref, alt_list=None, alt=None, raw_zygosity=None, zygosity=None, id=None):
        self.chr = chr.strip()
        self.pos = pos
        self.ref = ref.strip()
        self.alt_list = alt_list
        self.raw_zygosity = raw_zygosity.strip() if raw_zygosity is not None else raw_zygosity
            # string of zygosity from manual / VCF input
        self.alt = alt
        self.zygosity = zygosity
        self.id = id
        self.composite_key = None

    def __str__(self):
        return ":".join(str(e) for e in [self.chr, self.pos, self.ref, self.alt])

    def __repr__(self):
        return str(self.__dict__)

    def get_alt_from_list(self):
        """
        Pick the correct alt allele from the list, based on the raw_zygosity which is the GT column for VCF input.
        For manual input we only allow one possible alt allele, raising an error here if there are more.
        This does not run for cases with 2 alt alleles (GT = "1/2" etc.), they are already handled in
            VarcoppPreprocessPipeline.update_var_list()
        :return: the alt allele
        """
        alt_list = self.alt_list
        raw_zyg = self.raw_zygosity
        alt = None
        if "|" in raw_zyg or "/" in raw_zyg:
            try:
                a1, a2 = re.split("[|/]", raw_zyg)   # find the non-zero (if both non-zero they will be equal, so is ok)
                if a1 not in ["0", "."]:
                    index = int(a1)-1
                elif a2 not in ["0", "."]:
                    index = int(a2)-1
                else:
                    index = 0   # variant (0/0, ./., 0/.) will be discarded in later step
                alt = alt_list[index].strip()
            except IndexError:
                raise VariantParsingError("There was a problem determining the alternative allele for variant "
                                          "chr{c}:{pos}. Please review the GT info.".format(c=self.chr, pos=self.pos))
        else:   # manual input, missing value or single value
            try:
                if raw_zyg == "0":   # single value = 0 (those will get zygosity = None and be discarded so ok)
                    alt = None
                else:                # single value != 0
                    index = int(raw_zyg)-1
                    alt = alt_list[index].strip()
            except ValueError:      # missing value or manual input
                if len(alt_list) == 1:
                    alt = alt_list[0].strip()
                else:               # manual input, but now not allowed anymore - now checked in the parsing already
                    raise VariantParsingError("Cannot determine alternative allele from the list of options for variant"
                                        " chr{c}:{pos}. Please provide only one alt.".format(c=self.chr, pos=self.pos))
        if alt == "*":  # missing allele due to upstream deletion, missing value should be used
            alt = "-"
        return alt

    def set_zygosity(self, sex):
        """
        Initialize the zygosity of the variant based on the raw zygosity (GT column from VCF or manual input)
        and the patient's gender.
        :param sex: Sex of the patient ('U', 'F' or 'M')
        """
        self.zygosity = self.normalize_zygosity(sex)

    def normalize_zygosity(self, sex):
        """
        Normalize the raw zygosity in various formats into 'Homozygous' / 'Heterozygous' / 'Hemizygous'
        If it cannot do it, then the zygosity is set to None (later on used to filter out the variant).
        This does not run for cases with 2 alt alleles (GT = "1/2" etc.), they are already handled in
            VarcoppPreprocessPipeline.update_var_list()
        :param sex: Sex of the patient ('U', 'F' or 'M')
        :return: Normalized zygosity ('Homozygous' / 'Heterozygous' / 'Hemizygous') or None
        """
        zygosity = None
        if self.raw_zygosity is None:
            return None
        if '.' in self.raw_zygosity:
            # cases with e.g. "./1" are accepted, but "./.", ".", "./0" etc. aren't
            if not re.findall(r"[1-9]", self.raw_zygosity):
                return None
            else:
                zygosity = 'Heterozygous'
        if len(re.findall(r"\d+", self.raw_zygosity)) == 1:
            if self.raw_zygosity == '0':
                return None
            else:   # can be any number defining one of the alt alleles
                zygosity = 'Hemizygous'
        else:
            chrom_pres_l = re.split("[|/]", self.raw_zygosity)
            if chrom_pres_l[0] == '0' and chrom_pres_l[1] == '0':
                return None
            else:
                if self.chr == 'X' and sex == 'M':
                    zygosity = 'Hemizygous'
                elif self.chr == 'Y' and sex == 'M':
                    zygosity = 'Hemizygous'
                elif sex != 'M' or self.chr != 'X':
                    if "zygous" in self.raw_zygosity:
                        zygosity = self.raw_zygosity
                    else:
                        if len(chrom_pres_l) == 2:
                            if chrom_pres_l[0] == chrom_pres_l[1]:
                                zygosity = 'Homozygous'
                            else:
                                zygosity = 'Heterozygous'
                        else:
                            return None
        return zygosity

    def set_composite_key(self):
        if self.alt:
            compkey = self.get_composite_key(self.chr, self.pos, self.ref, self.alt)
            self.composite_key = compkey

    def get_composite_key(self, chr, pos, ref, alt):
        chr, pos, ref, alt = self.correct_variant(chr, pos, ref, alt)
        return ",".join(str(e) for e in [chr, pos, ref, alt])

    @staticmethod
    def correct_variant(chr, pos, ref, alt):
        """
        Modify non SNVs so that the composite key will be with dashes.
        This is the same function as used for creation of the composite keys in oligo pipeline annotation
        :returns (chr, pos, ref, alt) with pos, ref and alt adapted to the dash notation
        """

        # for SNVs and indels already dealt with dashes do nothing
        if (len(alt) == len(ref) == 1) or ('-' in (ref, alt)):
            return chr, pos, ref, alt

        #### for insertions
        elif len(alt) > len(ref):

            # for insertions at the end of the string or in the middle
            if ref[0] == alt[0]:

                # if insertion at the end of the string
                if ref == alt[0:len(ref)]:
                    # change position, ref, alt to include a dash
                    pos = pos + len(ref)
                    alt = alt[len(ref):]
                    ref = '-'
                    return chr, pos, ref, alt

                # if insertion in the middle of the string
                else:

                    changing_index = 0

                    # iterate over characters and find the position of the change
                    for i in range(len(ref)):
                        if ref[i] == alt[i]:
                            pos += 1
                        else:
                            changing_index = i
                            break

                    # define the change (insertion)
                    change = alt[changing_index:changing_index + (len(alt) - len(ref))]

                    # re-define the reference with a dash
                    ref = '-'

                    # correct in case the last nucleotide of the ref is the same as the first nucleotide of the insertion
                    # in this case we remove one position, to take this as the starting point
                    # we can never be 100% sure which change it is, but we take always the earliest position possible
                    if alt[changing_index - 1] == alt[changing_index]:
                        pos -= 1
                    return chr, pos, ref, change

            # if last nucleotides of alt are the same as ref, consider the insertion at the beginning of the string
            # this happens for some variants in hg19 at least
            elif ref == alt[len(alt) - len(ref):]:

                # change ref, alt to include a dash
                alt = alt[:len(alt) - len(ref)]
                ref = '-'
                return chr, pos, ref, alt

            else:
                return chr, pos, ref, alt

        #### for deletions
        elif len(alt) < len(ref):

            # for deletions at the beginning or the middle of the string
            if alt[0] == ref[0]:

                # if deletion at the end of the string
                if alt == ref[0:len(alt)]:

                    # change position, ref, alt to include a dash
                    pos = pos + len(alt)
                    ref = ref[len(alt):]
                    alt = '-'
                    return chr, pos, ref, alt

                # if deletion in the middle of the string
                else:

                    changing_index = 0

                    # iterate over characters and find the position of the change
                    for i in range(len(alt)):
                        if alt[i] == ref[i]:
                            pos += 1
                        else:
                            changing_index = i
                            break

                    # define the change (deletion)
                    change = ref[changing_index:changing_index + (len(ref) - len(alt))]

                    # re-define alternative with a dash
                    alt = '-'

                    # correct position in the same logic as the insertions
                    if ref[changing_index - 1] == ref[changing_index]:
                        pos -= 1
                    return chr, pos, change, alt

            # if last nucleotides of ref are the same as alt, consider the deletion at the beginning of the string
            # this happens for some variants in hg19 at least
            elif alt == ref[len(ref) - len(alt):]:

                # change ref, alt to include a dash
                ref = ref[:len(ref) - len(alt)]
                alt = '-'
                return chr, pos, ref, alt

            else:
                return chr, pos, ref, alt

        #### for multiple consecutive substitutions without deletion/insertions
        elif (len(alt) == len(ref) > 1) and (alt != ref):

            change, newref = '', ''
            ending_index = 0

            # iterate over characters and find the position of the change
            for i in range(len(ref)):
                if ref[i] == alt[i]:
                    pos += 1
                else:
                    ending_index = i
                    break

            for i in range(ending_index, len(ref)):
                change += alt[i]
                newref += ref[i]

            return chr, pos, newref, change


class VariantParsingError(Exception):
    pass


class AnnotatedVariant(Variant):
    def __init__(self, chr, pos, ref, alt, aapos, aaref, aaalt, ens_transcript_id, zygosity, cdnapos=None, id=None):
        super().__init__(chr=chr, pos=pos, ref=ref, alt=alt, zygosity=zygosity, id=id)
        self.aapos = aapos
        self.aaref = aaref
        self.aaalt = aaalt
        self.cdnapos = cdnapos
        self.ensembl_transcriptid = ens_transcript_id
        self.fl_diff = None  # flexibility difference (calc_aa_diff.py )
        self.h_diff = None  # hydrofobicity difference (calc_aa_diff.py)
        self.maf = None
        self.cadd_raw = None

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    def __eq__(self, other):
        if not isinstance(other, AnnotatedVariant):
            return False
        else:
            return self.chr == other.chr and self.pos == other.pos and self.ref == other.ref and self.alt == other.alt

    def __repr__(self):
        return str(self.__dict__)

    def to_dict_vec(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_") and v is not None}


class Gene:
    def __init__(self, gene_name, ens_gene_id, P_HI, P_rec, GDI, ISPP_AD, ISPP_AR, ISPP_XL, HIPred, dn_ds, RVIS,
                 aasequence=None, uniprot_id=None):
        self.ensembl_gene = ens_gene_id
        self.gene_name = gene_name
        # old VarCoPP features: P_rec and GDI still needed for DE prediction, P_HI could be removed
        self.P_HI = P_HI
        self.P_rec = P_rec
        self.GDI = GDI
        self.ISPP_AD = ISPP_AD
        self.ISPP_AR = ISPP_AR
        self.ISPP_XL = ISPP_XL
        self.HIPred = HIPred
        self.dn_ds = dn_ds
        self.RVIS = RVIS
        self.aasequence = aasequence
        self.uniprot_id = uniprot_id

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    def __eq__(self, other):
        return self.ensembl_gene == other.ensembl_gene

    def __hash__(self):
        return hash(self.ensembl_gene)

    def __repr__(self):
        return str(self.__dict__)

    def to_dict_vec(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_") and v is not None}


class AnnotationData:
    def __init__(self, gene=None, genevar=None):
        self.gene = gene
        self.gene_var = genevar  # Variant Alone or Heterozygous Compound object

    def __eq__(self, other):
        if (other is None and self is not None) or not isinstance(other, AnnotationData):
            return False
        else:
            return self.gene_var == other.gene_var and self.gene_var.zygosity == other.gene_var.zygosity

    def __iter__(self):
        for attr, value in self.__dict__.items():
            value = dict(value)

            yield attr, value

    def __repr__(self):
        return str(self.__dict__)

    def to_dict_vec(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_") and v is not None}
