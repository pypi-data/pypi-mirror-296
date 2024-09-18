import logging

from treeinterpreter import treeinterpreter as ti
import numpy as np

logger = logging.getLogger(__name__)


class VarcoppContributionAnalyzer:
    def __init__(self, model):
        """
        :param model: loaded (sklearn) model
        """
        self.model = model

    def execute(self, comb_vector):
        """
        Uses treeinterpreter to calculate the contributions of each feature in the VarCoPP prediction
        :param comb_vector: feature vector for a variant combination (vectorcomb in varcopp json)
        :return: dictionary {"feature": contribution} with contribution = float value giving the contribution of
                the feature to the VarCoPP score for the disease-causing class
        """
        logger.debug("Starting Varcopp feature contribution calculation")
        # the combination to be tested
        test_comb = np.array(comb_vector)

        # reshape the test combination vector
        test_comb = test_comb.reshape(1, -1)
        prediction, bias, contributions = ti.predict(self.model, test_comb)
        class_1_contributions = list(contributions[0][:, 1])

        # order of features same as input to model:
        features = ["CADD1", "CADD2", "CADD3", "CADD4", "BiolDist", "ISPP_AR_A", "ISPP_AR_B", "ISPP_AD_A",
                    "ISPP_AD_B", "ISPP_XL_A", "HIPred_A", "HIPred_B", "dn_ds_A", "BP_similarity", "KG_dist"]
        contrib_dict = {}
        for i in range(len(features)):
            contrib_dict[features[i]] = class_1_contributions[i]

        logger.debug("Finished Varcopp feature contribution calculation!!")
        return contrib_dict


# legacy method for old VarCoPP model

# def interpret(model, data):
#     """
#
#     :param model: VarCoPP model (500 RF ensemble)
#     :param data: combination vector (vectorcomb in varcopp json)
#     :return:
#     """
#
#     # loading model
#     loaded_rf_models = model
#
#     # the combination to be tested
#     #### test example #####
#     #test_comb = np.array([-0.01, 0.02, 1.73, -3, 2.35, -3, 0.32, 0.23, 0.04, 0.9, 3.1])
#     test_comb = np.array(data)
#
#     # reshape the test combination vector
#     test_comb = test_comb.reshape(1, -1)
#
#     # initiate matrix for feature contributions (lines are rfs, columns are features)
#     test_comb_matrix = []
#
#     # iterate over the random forests
#     for i in range(len(loaded_rf_models)):
#         # take each RF
#         clf = loaded_rf_models[i][0]
#
#         # predict and calculate importances
#         prediction, bias, contributions = ti.predict(clf, test_comb)
#
#         # take only array with decision scores for the disease class, features are in the same order as in the vector
#         class_1_contributions = list(contributions[0][:, 1])
#
#         # add to the matrix
#         test_comb_matrix += [class_1_contributions]
#
#     return test_comb_matrix


