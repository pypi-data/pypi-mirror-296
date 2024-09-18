import logging
import traceback
from oligopipe.preprocess.annotation import Annotator

logger = logging.getLogger(__name__)


class DigenicEffectPredictor:
    def __init__(self, model):
        """
        :param model: loaded (sklearn) model to use
        """
        self.model = model

    def predict(self, feature_vector):
        # new version of DE predictor (hg19 and hg38) that uses same features as VarCoPP
        """
        Predicts DE using the same features as VarCoPP.
        If a feature is missing then the probabilities for each class are "NaN"
        (Dual molecular Diagnosis / Monogenic + Modifier / True Digenic)

        :param feature_vector: feature vector (same as the one for VarCoPP2.0 so can be taken from the JSON)
        :return: dictionary with probability for each class {'DD': , 'MM': , 'TD': }
        """
        logger.debug("Starting DE prediction")
        if None in feature_vector:
            prediction = {'DD': 'NaN', 'MM': 'NaN', 'TD': 'NaN'}
        else:
            try:
                d_pred = self.model.predict_proba([feature_vector])[0]
                prediction = {'DD': d_pred[1], 'MM': d_pred[0], 'TD': d_pred[2]}
            except Exception as e:
                logger.error(e)
                logger.error(traceback.format_exc())
                prediction = {'DD': 'NaN', 'MM': 'NaN', 'TD': 'NaN'}
        logger.debug("Finished DE prediction!!")
        return prediction

    def predict_old(self, data, db_credentials, genome_build):
        # old version (only hg19) that used other features
        annotator = Annotator(db_credentials, genome_build)

        ensg_1 = data['varA']['gene']['ensembl_gene']
        ensg_2 = data['varB']['gene']['ensembl_gene']

        annotator.annotation_repository.connect()
        if annotator.db_schema == 'old':
            query = '''select ensembl_gene_id, array_agg(pathway_id), essential_in_mouse 
                                  FROM gene
                                  INNER JOIN aaid USING(ensembl_gene_id)
                                  INNER JOIN protein_to_pathway USING(uniprot_acc)
                                  INNER JOIN pathway USING(pathway_id)
                                  INNER JOIN pathway_hierarchy USING(pathway_id)
                                  WHERE ensembl_gene_id IN ({0})
                                  GROUP BY ensembl_gene_id;'''.format("'" + "','".join((ensg_1, ensg_2)) + "'")
        elif annotator.db_schema == 'new':
            query = '''select ensembl_gene_id, array_agg(pathway_id), essential_in_mouse 
                              FROM gene
                              INNER JOIN protein USING(ensembl_gene_id)
                              INNER JOIN protein_to_pathway USING(uniprot_acc)
                              INNER JOIN pathway USING(pathway_id)
                              INNER JOIN pathway_hierarchy USING(pathway_id)
                              WHERE ensembl_gene_id IN ({0})
                              GROUP BY ensembl_gene_id;'''.format("'" + "','".join((ensg_1, ensg_2)) + "'")
        cur = annotator.annotation_repository.execute(query)

        lookup_ess = {}
        lookup_pathways = {}
        for row in cur.fetchall():
            ensembl_gene_id, pathway_ids, essential_in_mouse = row
            lookup_ess[ensembl_gene_id] = essential_in_mouse
            lookup_pathways[ensembl_gene_id] = set(pathway_ids)

        if ensg_1 in lookup_ess and lookup_ess[ensg_1] == True:
            data['varA']['gene']['essentiality'] = 1
        else:
            data['varA']['gene']['essentiality'] = 0

        if ensg_2 in lookup_ess and lookup_ess[ensg_2] == True:
            data['varB']['gene']['essentiality'] = 1
        else:
            data['varB']['gene']['essentiality'] = 0
        try:
            if len(set(lookup_pathways[ensg_1]) & set(lookup_pathways[ensg_2])) > 0:
                res = 1
            else:
                res = 0
            data['Pathway'] = res
        except Exception:
            data['Pathway'] = 0

        annotator.annotation_repository.disconnect()

        entry = []
        # entry.append(data['combid'])
        entry.append(data['varA']['variants'][0].get('cadd_raw'))
        entry.append(-1 if len(data['varA']['variants']) == 1 else data['varA']['variants'][1].get('cadd_raw'))
        entry.append(data['varA']['gene'].get('P_rec'))
        entry.append(data['varA']['gene'].get('essentiality'))
        entry.append(data['varB']['variants'][0].get('cadd_raw'))
        entry.append(-1 if len(data['varB']['variants']) == 1 else data['varB']['variants'][1].get('cadd_raw'))
        entry.append(data['varB']['gene'].get('P_rec'))
        entry.append(data['varB']['gene'].get('essentiality'))
        entry.append(data.get('Pathway'))
        if None in entry:
            return {'DD': 'NaN', 'MM': 'NaN', 'TD': 'NaN'}
        try:
            d_pred = self.model.predict_proba([entry])
            d_pred_arr = d_pred[0]
            return {'DD': d_pred_arr[0], 'MM': d_pred_arr[1], 'TD': d_pred_arr[2]}
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return {'DD': 'NaN', 'MM': 'NaN', 'TD': 'NaN'}
