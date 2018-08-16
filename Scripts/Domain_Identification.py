import SVM_v2
import common_functions as utils
import multiDomainIdentifier
import calculateFeatures
import csv
import json


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
		'D' : "Density",
		'S' : "Density_Sum"
	}[x]

def get_input_dataset_features_file(x):
	return {
		"Benchmark_2" : "BenchmarkTwo_Features_v2.csv",
		"Benchmark_3" : "BenchmarkThree_Features_v2.csv",
		"ASTRAL SCOP30" : "Astral_Scop30_features_v2.csv",
		"Self-Created" : "self_created_dataset_features_v2.csv"
	}[x]

def get_multi_domain_identification_method(x):
	return {
		"A" : "Identification based on optimizing Density And Interaction Energy",
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


print "Identifying single-domain vs multi-domain proteins\n"

with open(file_testing_dataset_features) as f:
	SVM_test_data = f.readlines()

feature_set = []
while 1:
	featureSet_input = raw_input("Select features to be used for training and testing:\nType L for Length\nType I for Interaction_Energy\nType R for Radius_of_Gyration\nType D for Density\nFor multiple features, give space sepearated input. For ex. L D for Length & Density\n").split()
	print "You selected: ",

	try:
		for features in featureSet_input:
			feature_set.append(get_input_feature_name(features))
			print get_input_feature_name(features),
		print
		break
	except KeyError:
		print "Invalid Input!!"

file_training_dataset_features = "self_created_training_dataset_features_v3.csv"

with open(file_training_dataset_features) as f:
	SVM_train_data = f.readlines()

classifier = "single vs multi-domain"

correct_chains_with_features, incorrect_chains_with_features = SVM_v2.classify(SVM_train_data, SVM_test_data, feature_set, classifier)

utils.SVM_Performance_Analyser(correct_chains_with_features, SVM_test_data, classifier)

name_output_file = "output_correct"+"_"+testing_dataset+"_"+classifier+".txt"

f = open(name_output_file,"w+")

multi_correct_chains = []
for chain_with_features in correct_chains_with_features:
  f.write("%s\n" % chain_with_features.strip())
  chain_with_features = chain_with_features.split(",")
  pdb = chain_with_features[0].strip()
  chain = chain_with_features[1].strip()
  domains = int(chain_with_features[2].strip())

  if domains > 1:
  	multi_correct_chains.append(pdb+chain)



print "Saved correctly labelled chains to: ", name_output_file, "\n"

print "Identifying multi-domain proteins\n"

feature_set = []

while 1:
	featureSet_input = raw_input("Select features to be used for training and testing:\nType L for Length\nType I for Interaction_Energy\nType S for Density Sum\nFor multiple features, give space sepearated input. For ex. L S for Length & DensitySum\n").split()
	print "You selected: ",

	try:
		for features in featureSet_input:
			feature_set.append(get_input_feature_name(features))
			print get_input_feature_name(features),
		print
		break
	except KeyError:
		print "Invalid Input!!"


with open('self_created_multi_training_dataset_features_v3.json', 'r') as f:
    SVM_multi_train_data = json.load(f)

classifier = "multi-domain"

correct_chains_with_features, incorrect_chains_with_features = SVM_v2.classifyMultiDomainProteins(SVM_multi_train_data, multi_correct_chains, feature_set, classifier)






# utils.SVM_Performance_Analyser(correct_chains_with_features, SVM_test_data, classifier)


# multi_correct_chains_post_second_classification, multi_incorrect_chains_post_second_classification = multiDomainIdentifier.identifyNumberOfDomains(multi_training_dataset_features, multi_correct_chains, feature_set)
'''
We now need to calcuate the features for each k=2 to 4 for each entry in the test data set. Interaction Energy & 
Density Sum will vary for each value of k. Then, for each set of features, test the SVM and get the confidence score.
Pick the k with the max confidence.
'''





