import SVM_v2
import common_functions as utils

def get_input_dataset_name(x):
	return {
		'A' : "Benchmark_2",
		'B' : "Benchmark_3",
		'C' : "ASTRAL SCOP30",
		'D' : "Self-Created"
	}[x]

def get_input_feature_name(x):
	return {
		'L' : "Length",
		'I' : "Interaction_Energy",
		'R' : "Radius_Of_Gyration",
		'D' : "Density"
	}[x]

def get_input_dataset_features_file(x):
	return {
		"Benchmark_2" : "BenchmarkTwo_Features_v2.csv",
		"Benchmark_3" : "BenchmarkThree_Features_v2.csv",
		"ASTRAL SCOP30" : "Astral_Scop30_features_v2.csv",
		"Self-Created" : "self_created_dataset_features_v2.csv"
	}[x]

def get_input_classifier(x):
	return {
		"A" : "single vs multi-domain",
		"B" : "multi-domain"
	}[x]

#Taking user input for test dataset
while 1:
	testing_dataset_input = raw_input("Input Testing Dataset: Type A for Benchmark_2, B for Benchmark_3, C for ASTRAL SCOP 30, D for Self-Created\n")
	try:
		testing_dataset = get_input_dataset_name(testing_dataset_input)
		print "You selected " + testing_dataset + " for testing the SVM\n"
		break
	except KeyError:
		print "Invalid input!!"

file_testing_dataset_features = get_input_dataset_features_file(testing_dataset)



with open(file_testing_dataset_features) as f:
	SVM_test_data = f.readlines()

feature_set = []
while 1:
	featureSet_input = raw_input("Select features to be used for training and testing: Type L for Length, I for Interaction_Energy, R for Radius_of_Gyration, D for Density. For multiple features, give space sepearated input. For ex. L D for Length & Density\n").split()
	print "You selected: ",

	try:
		for features in featureSet_input:
			feature_set.append(get_input_feature_name(features))
			print get_input_feature_name(features),
		print
		break
	except KeyError:
		print "Invalid Input!!"


while 1:
	classifier_input = raw_input("Select SVM classification mode: Type A for single vs multi-domain classifier, B for multi-domain classifier\n")
	try:
		classifier = get_input_classifier(classifier_input)
		print "You selected: " + classifier + " classifier"
		break
	except KeyError:
		print "Invalid input!!"

if classifier=="single vs multi-domain":
	file_training_dataset_features = "self_created_training_dataset_features_v3.csv"
else:
	file_training_dataset_features = "self_created_multi_training_dataset_features.csv"

with open(file_training_dataset_features) as f:
	SVM_train_data = f.readlines()

correct_chains, incorrect_chains = SVM_v2.classify(SVM_train_data, SVM_test_data, feature_set, classifier)

print "INCORRECTLY PREDICTED CHAINS"
for x in incorrect_chains:
	print x.strip()

print "CORRECTLY PREDICTED CHAINS"
for x in correct_chains:
	print x.strip()

utils.SVM_Performance_Analyser(correct_chains, SVM_test_data, classifier)





