# This script is responsible for calculating the value of given feature set (input to the program)
# and outputting the data as a .json in the format where key is pdb+chain and value are 
# all the features. This file is introduced to calculate IS-Sum_2, IS-Sum_3 and IS-Sum_4
# for every multi-domain chain.
# Something like this
#'2wr1A': {'Length': 490, 'IS-Sum_4': '16.4', 'IS-Sum_3': '7.11', 'IS-Sum_2': '2.49', 'Domains': 2}, '1dw9B': {'Length': 152, 'IS-Sum_4': '32.9', 'IS-Sum_3': '9.09', 'IS-Sum_2': '2.1', 'Domains': 2}}

import common_functions as utils
import calculateFeatures
import json

#Defining constants here

multiDomain_trainingDataset_chains_file = "multiDomainTrainingDatasetChains.txt"
features_list = ["Length", "Interaction_Energy"]

with open(multiDomain_trainingDataset_chains_file, 'r') as f:
	input_chains = f.readlines()
	
feature_dictionary = {}

for chain in input_chains:
	chain = chain.strip()
	for k in range(2, 5):
		feature_map = calculateFeatures.calculateFeatures_v2([chain], features_list, k)
		feature_map[chain]["IS-Sum_"+str(k)] = feature_map[chain]["Interaction_Energy"]
		feature_map[chain].pop("Interaction_Energy")
		if chain in feature_dictionary: 
			feature_dictionary[chain]["IS-Sum_"+str(k)] = feature_map[chain]["IS-Sum_"+str(k)]
		else:
			feature_dictionary[chain] = feature_map[chain]
	feature_dictionary_json = json.dumps(feature_dictionary, sort_keys=True, indent=4)

json.dump(feature_dictionary, open("self_created_multi_training_dataset_features_v5.json", "wb"), sort_keys=True, indent=4)

