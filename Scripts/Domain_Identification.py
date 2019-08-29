import SVM_v2
import common_functions as utils
import multiDomainIdentifier
import calculateFeatures
import csv
import json
import K_Means
import K_means_experimental as Km_experimental


#This function takes as an input list of list where the fundamental list looks like this [{pdb: {length, IS-Sum_2, IS-Sum_3, IS-Sum_4}}, Domain] where the domain can be assigned/correct depending
# on the case. It extracts the features [Length, IS-Sum_2, IS-Sum_3, IS-Sum_4] along with CATH annotation and prints it out in .csv for ananlysis like this:
#Chain:  1fmtA ,  Domains (CATH):  2 ,  Domain 1 :  1 - 208 ,  Domain 2 :  209 - 313 ,  Length:  308 ,  IS-Sum_2:  3.6 ,  IS-Sum_3:  13.8 ,  IS-Sum_4:  34.0 ,  Assigned Domain:  2


def dumpMultiDomainClassificationOutput(chains_with_assignedDomains_and_featureSet):

	for entry in chains_with_assignedDomains_and_featureSet:
		
		chain_dict = entry[0]
		assigned_domain = entry[1]

		chain = chain_dict.keys()[0]
		feature_vector = chain_dict.values()[0]
		correct_domain = utils.findNumberOfDomains(chain)

		Km_experimental.applyKMeans(chain)
		counter = 0 
		for feature in feature_vector:
			if counter == 0:
				print "Length: ",
			elif counter == 1:
				print "IS-Sum_2: ",
			elif counter == 2:
				print "IS-Sum_3: ",
			elif counter == 3:
				print "IS-Sum_4: ",	
			print feature, ", ",
			counter+=1

		print "Assigned Domain: ", assigned_domain


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
		'S' : "Density_Sum",
		'IS': "IS_Sum"
	}[x]

def get_input_dataset_features_file(x):
	return {
		"Benchmark_2" : "BenchmarkTwo_Features_vAlt.csv",
		"Benchmark_3" : "BenchmarkThree_Features_v2.csv",
		"ASTRAL SCOP30" : "Astral_Scop30_features_v3.csv",
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
		if testing_dataset_input == 'E':
			testing_dataset = raw_input("Enter your chain for example: 1utgA\n")
		print "You selected " + testing_dataset + " for testing the SVM\n"
		break
	except KeyError:
		print "Invalid input!!"

print "Identifying single-domain vs multi-domain proteins\n"

feature_set = []
while 1:
	featureSet_input = raw_input("Select features to be used for training and testing:\nType L for Length\nType I for Interaction_Energy\nType R for Radius_of_Gyration\nType D for Density\nFor multiple features, give space sepearated input. For eg. L D for Length & Density\n").split()
	print "You selected: ",

	try:
		for features in featureSet_input:
			feature_set.append(get_input_feature_name(features))
			print get_input_feature_name(features),
		print
		break
	except KeyError:
		print "Invalid Input!!"

file_training_dataset_features = "self_created_training_dataset_features_vAlt.csv"

with open(file_training_dataset_features) as f:
	SVM_train_data = f.readlines()

classifier = "single vs multi-domain"

if testing_dataset_input != 'E':
	file_testing_dataset_features = get_input_dataset_features_file(testing_dataset)

	with open(file_testing_dataset_features) as f:
		SVM_test_data = f.readlines()

else:
	SVM_test_data = calculateFeatures.calculateFeatures_v2([testing_dataset], feature_set, 2)[testing_dataset]
	print SVM_test_data

correct_chains_with_features, incorrect_chains_with_features = SVM_v2.classify(SVM_train_data, SVM_test_data, feature_set, classifier)

utils.SVM_Performance_Analyser(correct_chains_with_features, SVM_test_data, classifier)

correct_chains_output_file_name = "output_correct"+"_"+testing_dataset+"_"+classifier+".txt"
inccorect_chains_with_features_output_file_name = "output_incorrect"+"_"+testing_dataset+"_"+classifier+".txt"


f = open(correct_chains_output_file_name,"w+")
f1 = open(inccorect_chains_with_features_output_file_name, "w+")

multi_correct_chains = []
single_correct_chains = []
total_test_chains = []

for x in SVM_test_data:
	x = x.split(",")
	pdb = x[0].strip()
	chain = x[1].strip()
  	total_test_chains.append(pdb+chain)


for chain_with_features in incorrect_chains_with_features:
	f1.write("%s\n" % chain_with_features.strip())

print "Saved incorrectly labelled chains to: ", inccorect_chains_with_features_output_file_name, "\n"


for chain_with_features in correct_chains_with_features:
  f.write("%s\n" % chain_with_features.strip())
  chain_with_features = chain_with_features.split(",")
  pdb = chain_with_features[0].strip()
  chain = chain_with_features[1].strip()
  domains = int(chain_with_features[2].strip())

  if domains > 1:
  	multi_correct_chains.append(pdb+chain)
  else:
  	single_correct_chains.append(pdb+chain)


print "Saved correctly labelled chains to: ", correct_chains_output_file_name, "\n"

print "Identifying multi-domain proteins\n"

feature_set = []

while 1:
	featureSet_input = raw_input("Select features to be used for training and testing:\nType L for Length\nType I for Interaction_Energy\nType S for Density Sum\nType IS for IS-Sum\nFor multiple features, give space sepearated input. For ex. L IS for Length & IS-Sum\n").split()
	print "You selected: ",

	try:
		for features in featureSet_input:
			feature = get_input_feature_name(features)
			if feature == "IS_Sum":
				feature_set.append("IS-Sum_2")
				feature_set.append("IS-Sum_3")
				feature_set.append("IS-Sum_4")
			else:
				feature_set.append(get_input_feature_name(features))
			print get_input_feature_name(features),
		print
		break
	except KeyError:
		print "Invalid Input!!"


with open('self_created_multi_training_dataset_features_v5.json', 'r') as f:
    SVM_multi_train_data = json.load(f)

classifier = "multi-domain"

print "Feature set is ", feature_set

correct_chains_withDomains, incorrect_chains_withAssignedDomains = SVM_v2.classifyMultiDomainProteins_v2(SVM_multi_train_data, multi_correct_chains, feature_set, classifier)

print ########################################################
print
print "PRINTING CORRECT CHAINS DATA"
print
dumpMultiDomainClassificationOutput(correct_chains_withDomains)
print
print ########################################################
print

print
print ########################################################
print
print "PRINTING INCORRECT CHAINS DATA"
print
dumpMultiDomainClassificationOutput(incorrect_chains_withAssignedDomains)
print
print ########################################################
print

print "Performance of multi-domin identification"

correct_chains = []
for chain in correct_chains_withDomains:
	correct_chains.append(chain[0].keys()[0])


utils.SVM_Multi_Domain_Performance_Analyser(correct_chains, multi_correct_chains)


correct_chains_post_kmeans, incorrect_chains_post_kmeans = K_Means.applyKMeans(correct_chains)

print
print "K-means Performance"
print
utils.SVM_Multi_Domain_Performance_Analyser(correct_chains_post_kmeans, correct_chains)


print
print "Overall Performance"
print
utils.SVM_Multi_Domain_Performance_Analyser(correct_chains_post_kmeans + single_correct_chains, total_test_chains)











