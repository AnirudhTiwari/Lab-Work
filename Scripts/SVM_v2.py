import common_functions as utils
from sklearn import svm

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

