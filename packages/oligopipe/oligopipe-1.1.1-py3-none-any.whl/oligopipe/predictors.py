import importlib.resources
import logging
import traceback
from abc import abstractmethod

import numpy as np
import json

from oligopipe.entities import VarCoPPResults, HOPInputData, HOPResults, Results
from oligopipe.hop.compute_ds_fs import compute_hop_scores
from oligopipe.hop.compute_rwr import run_rwr_hop
from oligopipe.hop.filter_rank_combs import filter_set, rank_all
from oligopipe.hop.hop_transform_data import chunked_transform_data
from oligopipe.varcopp.transform_data import transform_data

logger = logging.getLogger(__name__)


class Predictor:
    CONFIG_PACKAGE_PATH = "oligopipe"
    CONFIG_FILENAME = "predictors_config.json"

    def __init__(self, varcopp_model, genome_build):
        """
        :param varcopp_model: loaded VarCoPP model, currently a Balanced Random Forest model generating one score
        :param genome_build: "hg19" or "hg38"
        """
        self.varcopp_model = varcopp_model
        self.genome_build = genome_build
        if self.genome_build == "hg19":
            self.varcopp_model_name = "varcopp_19"
        else:
            self.varcopp_model_name = "varcopp_38"
        self.thresholds = None
        self.defaults_imputation = None
        self.set_model_constants()

    def set_model_constants(self):
        """
        Sets the threshold for the model and the imputation values for missing features (as {feature: default})
        """
        with importlib.resources.open_text(self.CONFIG_PACKAGE_PATH, self.CONFIG_FILENAME) as predictors_config_file:
            predictors_config = json.load(predictors_config_file)
        self.thresholds = predictors_config[self.varcopp_model_name]["thresholds"]
        self.defaults_imputation = predictors_config[self.varcopp_model_name]["imputation_values"]

    @abstractmethod
    def run_method(self, input, db_schema):
        pass

    @abstractmethod
    def get_results(self, combinations):
        pass

    def execute(self, input, db_schema):
        """
        Transforms input data, runs the prediction/prioritization and formats the results.
        If there are no gene pairs, no prediction/prioritization is performed and an empty (formatted) JSON is returned
        :param input: VarCoPPInputData or HOPInputData object
        :param db_schema: 'old' or 'new' (to correctly create the input vector)
        :return: results of prediction/prioritization in JSON format
        """
        logger.debug("Starting predictor...")
        logger.debug("Checking input: it has "+str(len(input.gene_pairs))+" gene pairs")
        logger.debug("Checking input: it has "+str(len(input.annotated_variants))+" annotated variants")
        if isinstance(input, HOPInputData):
            logger.info("Checking input: it has " + str(len(input.seeds)) + " seeds")

        # if less than two variants left after filtering, no need to run
        if len(input.gene_pairs) == 0:
            return Results({}).to_dict_vec()

        result_combinations = self.run_method(input, db_schema)
        # TODO what if we want to change chunk_length for hop from a higher level? need to be passed as variable

        results_object = self.get_results(result_combinations)
        return results_object.to_dict_vec()

    def run_varcopp(self, combinations, comb_feat_dict):
        """
        Iterates through the combinations and predicts them with VarCoPP in chunks of 10000
        :param combinations: dictionary of Combination objects {comb_id: comb_vct}
        :param comb_feat_dict: dictionary of feature vectors per combination
        :return: the updated combinations dictionary, with each combination having its VarCoPP score,
                prediction and confidence zone
        """
        combination_ids = []
        comb_features_matrix = []

        for comb_id, comb_feat in comb_feat_dict.items():
            if len(comb_features_matrix) < 10000:
                combination_ids.append(comb_id)
                comb_features_matrix.append(comb_feat)
            else:
                combination_ids.append(comb_id)
                comb_features_matrix.append(comb_feat)

                self.predict_chunk(comb_features_matrix, combination_ids, combinations)
                combination_ids = []
                comb_features_matrix = []

        self.predict_chunk(comb_features_matrix, combination_ids, combinations)
        return combinations

    def predict_chunk(self, comb_features_matrix, combination_ids, combinations):
        """
        Runs VarCoPP on a chunk of combinations and updates the combinations dictionary with the results
        :param comb_features_matrix: matrix of feature vectors for the chunk
        :param combination_ids: list of IDs in the chunk
        :param combinations: dict containing all combinations {comb_id: comb_vct}
        """
        prob_classes = self.varcopp_model.predict_proba(comb_features_matrix)
        # take probabilities for class 1 (disease-causing)
        varcopp_scores = np.array(prob_classes)[:, 1]

        for i in range(len(combination_ids)):
            comb_id = combination_ids[i]
            score = varcopp_scores[i]

            # Update the combination
            comb = combinations[comb_id]
            comb.varcopp_score = score
            if comb.varcopp_score > self.thresholds["DISEASE_CAUSING"]:
                comb.prediction = 'Disease-causing'
            else:
                comb.prediction = 'Neutral'
            comb.confidence_zone = self.get_confidence_zone(comb.prediction, comb.varcopp_score)

    def get_confidence_zone(self, prediction, varcopp_score):
        """
        Gives confidence zone according to prediction based on model-specific thresholds
        :param prediction: "Disease-causing" or "Neutral"
        :param varcopp_score: float value
        :return None or confidence zone (String)
        """
        if prediction == "Disease-causing":
            if varcopp_score >= self.thresholds["CONF_99"]:
                if varcopp_score >= self.thresholds["CONF_99.9"]:
                    return "99.9%-zone"
                else:
                    return "99%-zone"
        return None


class VarcoppPredictor(Predictor):

    def run_method(self, input, db_schema):
        """
        Runs a prediction by creating the input feature vector and running VarCoPP.
        :param input: VarCoPPInputData object
        :param db_schema: "old" or "new"
        :return: combinations: dict containing all predicted combinations {comb_id: comb_vct}
        """
        pair_data, combination_vectors = transform_data(self.defaults_imputation, input.gene_pairs,
                                                        input.annotated_variants, db_schema)
        try:
            combinations = self.run_varcopp(pair_data, combination_vectors)
        except Exception as e:
            raise VarcoppRunningError("{0} - {1}".format(e, traceback.format_exc()))
        return combinations

    def get_results(self, combinations):
        return VarCoPPResults(combinations)

class HOPPredictor(Predictor):

    def run_method(self, input, db_schema):
        """
        Runs a prioritization by calculating the random walk, then creating chunks of the input of which feature vectors
        are created, VarCoPP is run, HOP scores are calculated and only the top ranked combinations are retained.
        The retained combinations from each chunk are finally combined and ranked again.
        :param input: HOPInputData object
        :param db_schema: "old" or "new"
        :return: ranked_combinations: dict {comb_id: CombinationData} sorted by ascending rank of the combination
        """
        filtered_combinations = {}
        rwr_results, max_pair, min_pair = run_rwr_hop(input.annotated_variants, input.seeds)

        for pair_data, combination_vectors in chunked_transform_data(self.defaults_imputation, input.gene_pairs,
                                                                     input.annotated_variants, db_schema,
                                                                     chunk_length=100000):
            try:
                combinations = self.run_varcopp(pair_data, combination_vectors)
            except Exception as e:
                raise VarcoppRunningError("{0} - {1}".format(e, traceback.format_exc()))
            combinations = compute_hop_scores(combinations, rwr_results, max_pair, min_pair)
            filtered_combinations = filter_set(combinations, filtered_combinations, input.output_nb)

        ranked_combinations = rank_all(filtered_combinations)
        return ranked_combinations

    def get_results(self, combinations):
        return HOPResults(combinations)


class VarcoppRunningError(Exception):
    pass


# Legacy methods:

# def run(varcopp_model, combinations, comb_feat_dict):
#     """
#     Runs the 500 RF ensemble VarCoPP method
#     """
#     thresholds = load_thresholds()
#     varcopp_length = len(varcopp_model)
#
#     test_d = []
#     run_d = []
#
#     for comb_id, comb_feat in comb_feat_dict.items():
#         if len(run_d) < 10000:
#             test_d.append(comb_id)
#             run_d.append(comb_feat)
#         else:
#             test_d.append(comb_id)
#             run_d.append(comb_feat)
#
#             predict(run_d, test_d, thresholds, varcopp_length, varcopp_model, combinations)
#             test_d = []
#             run_d = []
#
#     predict(run_d, test_d, thresholds, varcopp_length, varcopp_model, combinations)
#     return combinations

# def predict(run_d, test_d, thresholds, varcopp_length, varcopp_model, combinations):
#     total_allclass_prob_lists = []
#     for trial in range(varcopp_length):
#         prob_classes = varcopp_model[trial][0].predict_proba(run_d)
#         total_allclass_prob_lists += [prob_classes]
#     total_allclass_prob_lists = np.array(total_allclass_prob_lists)[:, :, 1]
#     sample_medians = np.median(total_allclass_prob_lists, axis=0)
#     sample_ss = np.count_nonzero(total_allclass_prob_lists >
#                                  thresholds["DISEASE_CAUSING"], axis=0) / varcopp_length * 100
#     for i in range(len(test_d)):
#         comb_id = test_d[i]
#         v_cs = sample_medians[i]
#         v_ss = sample_ss[i]
#
#         # Update combination
#         comb = combinations[comb_id]
#         comb.cs = v_cs
#         comb.ss = v_ss
#
#         # find majority vote for this combination
#         if v_ss > 50.0:
#             comb.prediction = 'Disease-causing'
#         else:
#             comb.prediction = 'Neutral'
#
#         comb.confidence_zone = get_confidence_zone(comb.prediction, comb.cs, comb.ss, thresholds)

# def predict_classes(class_probs, threshold):
#     '''Function that takes the probabilities of class assignments for each
#     element and the threshold for class 1 and returns an array with class
#     labels for each element in the list'''
#
#     # list to hold labels
#     predicted_classes = []
#
#     # iterate over the elements
#     for el in class_probs:
#         # check threshold for class 1
#         if el[1] > threshold:
#             predicted_classes += [1]
#         else:
#             predicted_classes += [0]
#
#     predicted_classes = np.array(predicted_classes)
#
#     return predicted_classes

# def majority_vote(class_0, class_1):
#     '''
#     Function that takes an array with the true and predicted labels of the instance,
#     among all iterations and provides the majority vote for this instance.
#
#     '''
#
#     # check which class has more trees
#     if class_0 >= class_1:
#         majority_vote = 0
#     elif class_0 < class_1:
#         majority_vote = 1
#
#     return majority_vote


# def percentage_vote(predicted_probabilities, true_keys, combinations, threshold):
#     ''' Function that takes an array with the true labels of test data and a matrix
#     with iterations of predicted classes of the test data (in the same order),
#     as well as the assigned probabilities and returns a dictionary with
#     information on how each instance is voted for all iterations
#     and a list with the majority votes in the same order as the labels'''
#
# #    start_time = time.time()
#
#     # iterate over the combination IDs
#     for i in range(len(true_keys)):
#
#         predictions = []  # list to hold all class predictions for this element
#         disease_probabilities = []  #probability for the disease-causing class
#
#         #take the combination ID
#         true_key = true_keys[i]
#
#         # iterate over the iterations
#         for j in range(len(predicted_probabilities)):
#
#             # define probabilities
#             prob_iteration = predicted_probabilities[j][i]
#
#             # append probabilities
#             disease_probabilities += [prob_iteration[1]]
#
#             #define correct class label based on the probability
#             if prob_iteration[1]>threshold:
#                 predictions += [1]
#             else:
#                 predictions += [0]
#
#         # count disease class votes
#         num_1 = predictions.count(1)
#         perc_1 = (num_1 * 100) / len(predictions)
#
#         # count median disease probabilities
#         probability_1_median = np.median(disease_probabilities)
#
#  #       print("--- %s seconds (1) ---" % (time.time() - start_time))
#  #       start_time = time.time()
#
#         #update combination with ss, cs and confidence zone info
#         comb = combinations[true_key]
#
#         comb.cs = probability_1_median
#         comb.ss = perc_1
#
#         #find majority vote for this combination
#         if perc_1>50.0:
#             comb.prediction='Disease-causing'
#         else:
#             comb.prediction='Neutral'
#
#         comb.confidence_zone = get_confidence_zone(comb.prediction, comb.cs, comb.ss)
#
#         #reassign the combination to the key
#         combinations[true_key] = comb
#
# #        print("--- %s seconds (2) ---" % (time.time() - start_time))
# #        start_time = time.time()
#
#     return combinations


# def rank_data(votes_dictionary):
#     ''' Function that takes a dictionary of information about votes and ranks
#     the instances from more-probably disease causing to less probably,
#     based first on the median probability and second, on the
#     number of trees agreeing to the classification.
#     '''
#
#     # take positive and negative keys
#     pos_keys = list(votes_dictionary['positive'].keys())
#     neg_keys = list(votes_dictionary['negative'].keys())
#
#     # take info on Classification score and Support score
#     prob_pos = []
#     prob_neg = []
#
#     for key in pos_keys:
#         prob_pos += [(votes_dictionary['positive'][key]['perc_1'],
#                       votes_dictionary['positive'][key]['prob_1'],
#                       pos_keys.index(key)
#                       )]
#
#     for key in neg_keys:
#         prob_neg += [(votes_dictionary['negative'][key]['perc_1'],
#                       votes_dictionary['negative'][key]['prob_1'],
#                       neg_keys.index(key)
#                       )]
#
#     # sort the instances first Support score and then on Classification Score
#     sorted_keys = []
#
#     prob_pos.sort(reverse=True)
#     prob_neg.sort(reverse=True)
#
#     # create sorted keys
#     for el in prob_pos:
#         sorted_keys += [pos_keys[el[2]]]
#
#     for el in prob_neg:
#         sorted_keys += [neg_keys[el[2]]]
#
#     return sorted_keys, prob_pos, prob_neg, pos_keys, neg_keys

# def run_pred(model, combinations, test_set, test_keys):
#
#     # initiation of probability list for CS and SS calculations
#     probability_label_lists = []
#
#     ######################################### Predict digenic combinations
#     print('##### Predicting... ')
#
#     for trial in range(0, len(model)):
#         # initiate the Random Forest instance
#         trained_model = model[trial][0]
#
#         # see probabilities of predicted classes for test dataset
#         # first element for 0, second for 1
#         for test_set_chunk in chunks(test_set, 50):
#             prob_classes = trained_model.predict_proba(test_set_chunk)
#
#         # append predicted values in the total test and probability labels
#         probability_label_lists += [prob_classes]
#
#     ######################################### calculate majority vote and SS, CS, confidence zones
#     print('##### Calculating majority vote')
#
#     annotated_combinations = percentage_vote(probability_label_lists,
#                         test_keys, combinations, 0.4891)
#
#     return annotated_combinations
