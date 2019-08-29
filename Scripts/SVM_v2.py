import common_functions as utils
from sklearn import svm
import calculateFeatures
import numpy as np

def classify(training_data, testing_data, feature_set, classification_type):
	X_train, y_train = utils.extractFeaturesAndLabelsForSVM(training_data, feature_set, classification_type)
	X_test, y_test = utils.extractFeaturesAndLabelsForSVM(testing_data, feature_set, classification_type)
	
	print "Training data => ", len(X_train), len(y_train)
	print "Testing data => ", len(X_test), len(y_test)

	clf = svm.SVC().fit(X_train, y_train)

	predicted_label = clf.predict(X_test)

	correct_chains = []
	incorrect_chains = []

	for i in range(0, len(y_test)):
		data = testing_data[i].split(",")
		if predicted_label[i]==y_test[i]:
			correct_chains.append(testing_data[i])
		else:
			incorrect_chains.append(testing_data[i])

	return correct_chains, incorrect_chains


'''
This method tries to find the number of domains for a multi-domain protein by executing the following steps:
1. The SVM is trained for the given features
2. For each k=2 to 4 for each entry in the test data set, features are calculated. Density Sum and Interaction Energy will vary 
for various values of k.
3. Then, for each set of features, test the SVM and get the confidence score. Pick the k with the max confidence.
'''

def classifyMultiDomainProteins(training_data, testing_data, feature_set, classification_type):
	X_train, y_train = utils.extractFeaturesAndLabelsForSVMFromJson(training_data, feature_set, classification_type)

	correct_chains = []
	incorrect_chains = []

	print "Training Data => ", len(X_train), len(y_train)
	print "Testing Data => ", len(testing_data)

	clf = svm.SVC(probability=True).fit(X_train, y_train)


	for chain in testing_data:

		domains = utils.findNumberOfDomains(chain, None)

		max_probablity = -1000000000

		for k in range (2,5):
			feature_map = calculateFeatures.calculateFeatures_v2([chain], feature_set, k)
			prediction_confidence = clf.predict_proba([feature_map[chain]])[0][k-2]

			if  prediction_confidence > max_probablity:
				max_probablity = prediction_confidence
				assigned_domains = k


		if assigned_domains == domains:
			correct_chains.append(chain)
		else:
			incorrect_chains.append(chain)

	return correct_chains, incorrect_chains


'''
This method is to be used when we are using the updated algorithm whereby we are using IS-Sum1, IS-Sum2, IS-Sum3 and Length as feature vectors. 
Thus, in this don't calculate the prediction confidence for each split, we use the SVM to classify in a single go by evaluating this 4-D feature vector.
Consult self_created_multi_training_dataset_features_v5.json to get an idea of the feature vector set that we will be calculating. NOTE: IF THE FEATURE SET
CONTAINS "Interaction_Energy" AS A FEATURE THAN IT WOULD BE TRANSLATED TO CORRESPONDING IS-SUM_2/3/4 BASED ON THE NUMBER OF DOMAINS IT IS SUPPOSED TO HAVE.
This function returns a list of list for correct and incorrect chains both. The fundamental list has 2 items [feature_map, AssignedDomains]
feature map looks like this -> "1a0hA": {
        "Domains": 2, 
        "IS-Sum_2": "1.03", 
        "IS-Sum_3": "4.61", 
        "IS-Sum_4": "28.7", 
        "Length": 159
    }
'''

def classifyMultiDomainProteins_v2(training_data, testing_data, feature_set, classification_type):
	X_train, y_train = utils.extractFeaturesAndLabelsForSVMFromJson(training_data, feature_set, classification_type)
	correct_chains = []
	incorrect_chains = []

	clf = svm.SVC(probability=True).fit(X_train, y_train)
	for chain in testing_data:

		domains = utils.findNumberOfDomains(chain, None)

		max_probablity = -1000000000

		feature_map = calculateFeatures.calculateFeatures_v2([chain], feature_set, domains)

		assigned_domains = clf.predict(np.array(feature_map[chain]).reshape(1,-1))[0]

		if assigned_domains == domains:
			correct_chains.append([feature_map, domains])
		else:
			incorrect_chains.append([feature_map, assigned_domains])

	return correct_chains, incorrect_chains


