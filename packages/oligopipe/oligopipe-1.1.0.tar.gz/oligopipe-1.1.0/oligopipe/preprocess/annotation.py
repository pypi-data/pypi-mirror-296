import itertools
import logging
import traceback
import psycopg2

from oligopipe.preprocess.calc_aa_diff import *
from oligopipe.entities import *
from oligopipe.repositories import AnnotationRepository
from oligopipe.utils import chunks, iter_chunks
from oligopipe.preprocess.filters import Filter

logger = logging.getLogger(__name__)


class Annotator:
    SCHEMA_PER_BUILD = {'hg19': 'old', 'hg38': 'new'}

    def __init__(self, db_credentials, genome_build="hg19"):
        self.genome_build = genome_build    # default can be used in cases where it doesn't make a difference (e.g. HPO)
        self.db_schema = self.SCHEMA_PER_BUILD[genome_build]
        self.annotation_repository = AnnotationRepository(db_credentials)


class VariantAnnotator(Annotator):

    def __init__(self, db_credentials, genome_build):
        super().__init__(db_credentials, genome_build)
        self.annotated_vars_compkeys = []
        self.discarded_vars = {'missing': [], 'filtered': []}
        self.unique_genes = set()

    def annotate(self, variants, zygosities_dict, filters, gene_panel):
        """
        :param variants: list of composite keys
        :param zygosities_dict: dict {composite_key: zygosity}
        :param filters: list with filters e.g. [('MAX_MAF', 0.035), 'REMOVE_INTERGENIC', 'REMOVE_INTRONS']
        :param gene_panel: None or list with genes
        :return: annotated_vars: list of AnnotationData objects
                discarded_vars: dict with list of composite keys per category of discarded variant
        """
        annotated_vars = self.annotate_variants_basic(variants, zygosities_dict, filters, gene_panel)
        filtered_or_missing = set(variants) - set(self.annotated_vars_compkeys)
        if filtered_or_missing:
            self.split_missing_filtered(filtered_or_missing)
        return annotated_vars, self.discarded_vars

    def split_missing_filtered(self, filtered_or_missing):
        self.annotation_repository.connect()
        q = r"""SELECT composite_key FROM variant WHERE composite_key IN ('{0}');""".format(
            "','".join(filtered_or_missing))
        filtered = [row[0] for row in self.annotation_repository.execute(q).fetchall()]
        missing = list(filtered_or_missing - set(filtered))
        self.discarded_vars["missing"] = missing
        self.discarded_vars["filtered"] = filtered
        self.annotation_repository.disconnect()

    def annotate_variants_basic(self, variants, zygosity_dict, variant_filters, gene_panel):
        self.annotation_repository.connect()
        tot_variant_nb = len(variants)
        processed_variants = 0
        all_annotated = []
        for variants_chunk in chunks(variants, 10000):
            query = self.build_annotation_filtering_query(variants_chunk, variant_filters, gene_panel)
            results = []
            try:
                cur = self.annotation_repository.execute(query)
                results = cur.fetchall()
                results = set(results)
                # some variants can be returned multiple times if there are multiple exons close enough
                # (happens e.g. for variant 14,23866189,G,A which is returned 3 times)
            except (Exception, psycopg2.DatabaseError) as error:
                logger.error(error)
                logger.error(traceback.format_exc())
            processed_variants += len(variants_chunk)
            logger.info("Fetching annotations for {0}/{1} variants ({2:.2f} %)"
                        .format(processed_variants, tot_variant_nb, (processed_variants/tot_variant_nb)*100))
            for row in results:
                cdnapos = None  # because will be missing from old db_schema
                if self.db_schema == 'old':
                    comp_key, chrom, pos, ref, alt, aapos, aaref, aaalt, ensembl_gene, ensembl_transcriptid, \
                        gene_name, P_HI, P_rec, GDI, sequence, uniprot_acc, maf, cadd_raw, cadd_phred, \
                        ISPP_AD, ISPP_AR, ISPP_XL, HIPred, dn_ds, RVIS = row
                elif self.db_schema == 'new':
                    comp_key, chrom, pos, ref, alt, aapos, aaref, aaalt, cdnapos, ensembl_gene, ensembl_transcriptid, \
                        gene_name, P_HI, P_rec, GDI, sequence, uniprot_acc, maf, cadd_raw, cadd_phred, \
                        ISPP_AD, ISPP_AR, ISPP_XL, HIPred, dn_ds, RVIS = row
                zygosity = zygosity_dict[comp_key]
                gene = Gene(gene_name, ensembl_gene, P_HI, P_rec, GDI, ISPP_AD, ISPP_AR, ISPP_XL, HIPred, dn_ds,
                            RVIS, sequence, uniprot_acc)
                # gene sequence is used and afterwards removed by calc_aa_diff
                var = AnnotatedVariant(chrom, pos, ref, alt, aapos, aaref, aaalt, ensembl_transcriptid, zygosity, cdnapos)
                var.maf = maf
                var.cadd_raw = cadd_raw
                var.cadd_phred = cadd_phred
                annotation_data = AnnotationData(gene, var)
                self.annotated_vars_compkeys.append(comp_key)
                self.unique_genes.add(gene.gene_name)
                all_annotated.append(calc_aa_diff(annotation_data))
                # note: the aa_diff calculations are actually not used anymore, keeping them for reference
        self.annotation_repository.disconnect()
        return all_annotated

    def build_annotation_filtering_query(self, variant_keys, variant_filters, gene_panel):
        gene_panel_query = ""
        if gene_panel:
            gene_panel_query += """ DROP TABLE IF EXISTS gene_panel_temp; """
            gene_panel_query += """ CREATE TEMP TABLE gene_panel_temp(ensembl_gene_id TEXT primary key); """
            gene_panel_query += """ INSERT INTO gene_panel_temp(ensembl_gene_id) VALUES ('{0}') ON CONFLICT DO NOTHING;
                                    ANALYZE gene_panel_temp;
                                """.format("'),('".join(str(g) for g in gene_panel))

        if self.db_schema == 'old':
            query = """
                            DROP TABLE IF EXISTS selected_variants;
                            CREATE TEMP TABLE selected_variants as
                            SELECT composite_key, chr, pos, ref, alt, aa_pos, aa_ref, aa_alt, ensembl_gene_id, cadd_raw, cadd_phred
                            FROM variant
                            WHERE composite_key IN ('{0}');
                            CREATE INDEX selected_variants_composite_idx ON selected_variants(composite_key);
                            CREATE INDEX selected_variants_ensembl_idx ON selected_variants(ensembl_gene_id);
                            ANALYZE selected_variants;  
                             """.format("','".join(variant_keys))
        elif self.db_schema == 'new':
            query = """
                    DROP TABLE IF EXISTS selected_variants;
                    CREATE TEMP TABLE selected_variants as
                    SELECT composite_key, chr, pos, ref, alt, aa_pos, aa_ref, aa_alt, cdna_pos, ensembl_gene_id, cadd_raw, cadd_phred
                    FROM variant
                    WHERE composite_key IN ('{0}');
                    CREATE INDEX selected_variants_composite_idx ON selected_variants(composite_key);
                    CREATE INDEX selected_variants_ensembl_idx ON selected_variants(ensembl_gene_id);
                    ANALYZE selected_variants;  
                     """.format("','".join(variant_keys))

        if self.db_schema == 'old':
            query += """
                            DROP TABLE IF EXISTS joined_variants;
                            CREATE TEMP TABLE joined_variants as 
                            SELECT composite_key, chr, pos, ref, alt, aa_pos, aa_ref, aa_alt, cadd_raw, cadd_phred,
                                gene.ensembl_gene_id, gene.start_position as gene_start, gene.end_position as gene_end, 
                                ensembl_can_transcript_id, gene.gene_name, p_hi, p_rec, gdi, ispp_ad_score, 
                                   ispp_ar_score, ispp_xl_score, hipred, dn_ds, rvis
                            FROM selected_variants
                            INNER JOIN gene USING(ensembl_gene_id)
                            LEFT JOIN gene_new_features using(ensembl_gene_id)
                            """
        elif self.db_schema == 'new':
            query += """
                    DROP TABLE IF EXISTS joined_variants;
                    CREATE TEMP TABLE joined_variants as 
                    SELECT composite_key, chr, pos, ref, alt, aa_pos, aa_ref, aa_alt, cdna_pos, cadd_raw, cadd_phred,
                        gene.ensembl_gene_id, gene.start_position as gene_start, gene.end_position as gene_end, 
                        ensembl_can_transcript_id, gene.gene_name, p_hi, p_rec, gdi, ispp_ad_score, 
                           ispp_ar_score, ispp_xl_score, hipred, dn_ds, rvis
                    FROM selected_variants
                    INNER JOIN gene USING(ensembl_gene_id)
                    """

        variant_filter_types = Filter.get_variant_filter_types(variant_filters)

        if gene_panel:
            query = gene_panel_query + query
            query += """ INNER JOIN gene_panel_temp ON gene.ensembl_gene_id = gene_panel_temp.ensembl_gene_id   """

        query += """ 
                   WHERE gene.gene_name IS NOT NULL AND gene.ensembl_gene_id IS NOT NULL;
                   CREATE INDEX joined_variants_composite_idx ON joined_variants(composite_key);
                   CREATE INDEX joined_variants_transcript_idx ON joined_variants(ensembl_can_transcript_id);
                   ANALYZE joined_variants;
                 """

        if self.db_schema == 'old':
            query += """  
                    SELECT joined_variants.composite_key, joined_variants.chr, joined_variants.pos, joined_variants.ref, joined_variants.alt, aa_pos, aa_ref, aa_alt,
                        joined_variants.ensembl_gene_id, ensembl_can_transcript_id, gene_name, p_hi, p_rec, gdi,
                        sequence, uniprot_acc, af_filter, cadd_raw, cadd_phred, ispp_ad_score, ispp_ar_score, ispp_xl_score, hipred, dn_ds, rvis
                    FROM joined_variants 
                    LEFT JOIN aaid ON(ensembl_transcript_id=ensembl_can_transcript_id)
                    LEFT JOIN aaseq ON(uniprot_acc=aaseq.name)
                    LEFT JOIN exac USING (composite_key)
                    """
        elif self.db_schema == 'new':
            query += """  
                    SELECT joined_variants.composite_key, joined_variants.chr, joined_variants.pos, joined_variants.ref, joined_variants.alt, aa_pos, 
                    aa_ref, aa_alt, cdna_pos, joined_variants.ensembl_gene_id, ensembl_can_transcript_id, gene_name, p_hi, 
                    p_rec, gdi, aaseq, uniprot_acc, af_filter, cadd_raw, cadd_phred, ispp_ad_score, ispp_ar_score, ispp_xl_score, 
                    hipred, dn_ds, rvis
                    FROM joined_variants 
                    LEFT JOIN protein USING (ensembl_can_transcript_id)
                    LEFT JOIN variant_freq USING (composite_key)
                    """

        if Filter.REMOVE_INTRONS in variant_filter_types:
            query += """ LEFT JOIN exons ON (ensembl_can_transcript_id=exons.ensembl_transcript_id) """

        if len(variant_filters) > 0:
            query += """ WHERE TRUE """

        if Filter.REMOVE_INTERGENIC in variant_filter_types:
            query += """ AND (gene_start IS NULL 
                            OR gene_end IS NULL
                            OR (joined_variants.pos >= gene_start 
                                AND joined_variants.pos <= gene_end))
                     """
        if Filter.REMOVE_INTRONS in variant_filter_types:
            query += """ AND (exon_start_pos IS NULL OR exon_end_pos IS NULL OR 
                            ((aa_ref IS NULL OR aa_ref != aa_alt) AND joined_variants.pos >= exon_start_pos - 13 AND joined_variants.pos <= exon_end_pos + 13) OR 
                            (aa_ref = aa_alt AND ((joined_variants.pos >= exon_start_pos - 195 AND joined_variants.pos <= exon_start_pos + 195) OR 
                                                (joined_variants.pos >= exon_end_pos - 195 AND joined_variants.pos <= exon_end_pos + 195))
                            ))
                     """
        elif Filter.REMOVE_INTRONS_AND_SYNONYNOUS in variant_filter_types:
            query += """ AND (exon_start_pos IS NULL OR exon_end_pos IS NULL OR
                            ((aa_ref IS NULL OR aa_ref != aa_alt) AND joined_variants.pos >= exon_start_pos - 13 AND joined_variants.pos <= exon_end_pos + 13))
                     """
        if Filter.MAX_MAF in variant_filter_types:
            max_maf_threshold = Filter.get_variant_filter_value(variant_filters, Filter.MAX_MAF)
            query += """ AND (af_filter IS NULL OR af_filter <= {0}) """.format(max_maf_threshold)
        return query


class GenePairAnnotator(Annotator):

    def __init__(self, db_credentials, genome_build):
        super().__init__(db_credentials, genome_build)

    def annotate(self, variants):
        return self.annotate_genepairs(variants)

    def annotate_genepairs(self, annotated_variants):
        """
        Creates the unique gene pairs, sorts them on RVIS (for VarCoPP) and queries the DB for their values.
        The query contains the alphanumerically sorted pair (on their ENSGs), since this is the pair present in gene_pairs table
        :param annotated_variants: list of AnnotationData objects
        :return: Dictionary with gene pairs as keys (using gene names) and annotated values as value in subdictionary
        """
        self.annotation_repository.connect()
        # create all possible (unique) pairs WITHOUT ANY variant info
        annotated_genepairs = {}
        if self.db_schema == 'old':
            gene_pair_iterator = self.make_genepairs(annotated_variants)
            for genepairs_chunk in iter_chunks(gene_pair_iterator, 1000):
                genepairs_keys = []
                for genea, geneb in genepairs_chunk:
                    geneA, geneB = self.ordered_pairs_with_rvis(genea, geneb)
                    annotated_genepairs[(geneA.gene_name, geneB.gene_name)] = {"biol_dist": None, "BP_similarity": None,
                                                                               "KG_dist": None}
                    genepairs_keys.append(geneA.gene_name + "," + geneB.gene_name)
                try:
                    query = """SELECT c_gene, m_gene, distance, bpo_sim, distance_kg 
                               FROM pair_table WHERE composite_key IN('{0}');""".format("','".join(genepairs_keys))
                    cur = self.annotation_repository.execute(query)
                    results = cur.fetchall()
                    for row in results:
                        gene_name1, gene_name2, biol_dist, bpo_sim, distance_kg = row
                        annotated_genepairs[(gene_name1, gene_name2)] = {"biol_dist": biol_dist,
                                                                         "BP_similarity": bpo_sim,
                                                                         "KG_dist": distance_kg}
                except Exception as e:  # could be connection error or genename error
                    logger.error(e)
                    logger.error(traceback.format_exc())

        elif self.db_schema == 'new':
            unique_pairs = self.make_genepairs(annotated_variants)
            gene_pairs_rvis_sorted = [self.ordered_pairs_with_rvis(geneA, geneB) for (geneA, geneB) in unique_pairs]
            for genepairs_chunk in iter_chunks(gene_pairs_rvis_sorted, 1000):
                query_list = []
                for gene_a, gene_b in genepairs_chunk:
                    annotated_genepairs[(gene_a.ensembl_gene, gene_b.ensembl_gene)] = {"biol_dist": None,
                                                                                       "BP_similarity": None,
                                                                                       "KG_dist": None}
                    geneA, geneB = self.ordered_pairs_with_ensg(gene_a, gene_b)
                    query_list.append((geneA.ensembl_gene, geneB.ensembl_gene))
                try:
                    query = """SELECT ensg_a, ensg_b, distance, bpo_sim, distance_kg 
                               FROM gene_pairs WHERE (ensg_a, ensg_b) IN({0});""".format(str(query_list).strip('[]'))
                    cur = self.annotation_repository.execute(query)
                    results = cur.fetchall()
                    for row in results:
                        ensg1, ensg2, biol_dist, bpo_sim, distance_kg = row
                        if (ensg1, ensg2) in annotated_genepairs:
                            annotated_genepairs[(ensg1, ensg2)] = {"biol_dist": biol_dist, "BP_similarity": bpo_sim,
                                                                   "KG_dist": distance_kg}
                        elif (ensg2, ensg1) in annotated_genepairs:
                            annotated_genepairs[(ensg2, ensg1)] = {"biol_dist": biol_dist, "BP_similarity": bpo_sim,
                                                                   "KG_dist": distance_kg}
                        else:
                            raise Exception("There is an error. Check GenePairAnnotator.annotate_genepairs()")
                except Exception as e:  # could be connection error or genename error
                    logger.error(e)
                    logger.error(traceback.format_exc())

        self.annotation_repository.disconnect()
        return annotated_genepairs

    def make_genepairs(self, annotated_entries):
        """ Makes all possible GENE PAIR combinations from the set """
        genes = set()

        # collect unique genes
        for annotation_data in annotated_entries:
            # is AnnotationData object, instantiated in VariantAnnotator.annotate()
            genes.add(annotation_data.gene)

        return list(itertools.combinations(genes, 2))

    def ordered_pairs_with_ensg(self, geneA, geneB):
        """ Orders genes based on ENSG (alphanumerical sorting) """
        if geneA.ensembl_gene < geneB.ensembl_gene:
            return geneA, geneB
        else:
            return geneB, geneA

    def ordered_pairs_with_rvis(self, gene_A, gene_B):
        """ Orders genes based on RVIS.
        GeneA is always the gene with the lowest RVIS. """

        rvisA = gene_A.RVIS
        rvisB = gene_B.RVIS

        if (rvisA is None or rvisA == 'None') and rvisB is not None and rvisB != 'None':
            final_geneA, final_geneB = gene_B, gene_A

        elif (rvisA is not None and rvisA != 'None') and (rvisB is None or rvisB == 'None'):
            final_geneA, final_geneB = gene_A, gene_B

        elif (rvisA is None or rvisA == 'None') and (rvisB is None or rvisB == 'None'):
            final_geneA, final_geneB = gene_A, gene_B

        else:
            if min(float(rvisA), float(rvisB)) == float(rvisA):
                final_geneA, final_geneB = gene_A, gene_B
            else:
                final_geneA, final_geneB = gene_B, gene_A

        return final_geneA, final_geneB


class GeneAnnotator(Annotator):
    def __init__(self, db_credentials, genome_build):
        super().__init__(db_credentials, genome_build)

    def annotate(self, ensembl_gene_ids):
        annotated_genes = []
        self.annotation_repository.connect()
        if self.db_schema == 'old':
            query = '''SELECT DISTINCT gene.gene_name, gene.ensembl_gene_id, p_hi, p_rec, gdi, uniprot_acc, 
                    ispp_ad_score, ispp_ar_score, ispp_xl_score, hipred, dn_ds, rvis
                    FROM gene
                    LEFT JOIN aaid ON(ensembl_transcript_id = ensembl_can_transcript_id)
                    LEFT JOIN gene_new_features gnf ON(gene.ensembl_gene_id = gnf.ensembl_gene_id)
                    WHERE gene.ensembl_gene_id IN ({0})'''.format("'" + "','".join(ensembl_gene_ids) + "'")
        elif self.db_schema == 'new':
            query = '''SELECT DISTINCT gene_name, gene.ensembl_gene_id, p_hi, p_rec, gdi, uniprot_acc, ispp_ad_score, 
                    ispp_ar_score, ispp_xl_score, hipred, dn_ds, rvis
                    FROM gene
                    LEFT JOIN protein USING(ensembl_can_transcript_id)
                    WHERE gene.ensembl_gene_id IN ({0})'''.format("'" + "','".join(ensembl_gene_ids) + "'")

        cur = self.annotation_repository.execute(query)
        for row in cur.fetchall():
            gene_name, ensembl_gene, P_HI, P_rec, GDI, uniprot_acc, ISPP_AD, \
                ISPP_AR, ISPP_XL, HIPred, dn_ds, RVIS = row
            gene = Gene(gene_name, ensembl_gene, P_HI, P_rec, GDI, ISPP_AD, ISPP_AR, ISPP_XL, HIPred, dn_ds, RVIS)
            gene.uniprot_id = uniprot_acc
            annotated_genes.append(gene)
        self.annotation_repository.disconnect()
        return annotated_genes
