import common_functions as utils
import calculateFeatures as cf
import json

with open ('Training_dataset_chains_complete_v2.txt') as f:
	input_chains = f.readlines()

featureSet = ["Length", "Interaction_Energy"]

feature_dict = {}

for input_chain in input_chains:
	pdb = input_chain[:4].lower()
	chain = input_chain[4].lower()
	domains = utils.findNumberOfDomains(pdb, chain)
	

	try:
		if domains >= 2:
			feature_dict[pdb+chain.upper()] = {}
			feature_dict[pdb+chain.upper()] = cf.calculateFeatures_v2([input_chain], featureSet, domains)[pdb+chain.upper()]

	except Exception as e:
		raise e
		print pdb, chain
	

json_string = json.dumps(feature_dict, indent=4)

fw = open("self_created_multi_training_dataset_features_vAlt.json", "w+")

fw.write(json_string)












