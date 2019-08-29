'''
This module computes various features for a given input and the desired list of features.
This program is the ultimate authority when it comes to feature calculation. Any new feature that needs to be calculated
should have an ingress point from here. Currently supported features are
Density, Length, Interaction Energy, Radius Of Gyration, and Density Sum
'''
import Density as density
import radius_of_gyration as RG
import InteractionEnergy as IE
import DensitySum as DS
import Length as length
import common_functions as utils

def calculateLength(pdb, chain):
	return length.calculateLength(pdb, chain)

def calculateInteractionEnergy(pdb, chain, num_of_clusters):
	return IE.calculateInteractionEnergy(pdb, chain, num_of_clusters)

def calculateRadiusOfGyration(pdb, chain):
	return RG.calculateRadiusOfGyration(pdb, chain)

def calculateDensity(pdb, chain):
	return density.calculateDensity(pdb, chain)

def calculateDensitySum(pdb, chain, num_of_clusters):
	return DS.calculateDensitySum(pdb, chain, num_of_clusters)

#A map of feature and its corresponding method which is to be invoked
features = {
	"Length" : calculateLength,
	"Interaction_Energy" : calculateInteractionEnergy,
	"IS-Sum_2" : calculateInteractionEnergy,
	"IS-Sum_3" : calculateInteractionEnergy,
	"IS-Sum_4" : calculateInteractionEnergy,
	"Radius_Of_Gyration" : calculateRadiusOfGyration,
	"Density" : calculateDensity,
	"Density_Sum" : calculateDensitySum
}

'''
This method is the ingress point for calculating features for a given input list of chains in the format pdb+chain
Feature set is a list of the features that needs to be calculated. The Interaction Strength & Density Sum are 
calculated for as many number of domains as per CATH. 

PLEASE USE THIS METHOD FOR TRAINING DATASET

Returns the calculated features in the following format in a map
{
	pdb1+chain1: [feature11, feature12, feature13, feature14]
	pdb2+chain2: [feature21, feature22, feature23, feature24]
	.
	.
	.
	.

}
'''
def calculateFeatures(input_chains, feature_set):
	feature_map = {}
	for input_chain in input_chains:


		input_chain = list(input_chain)

		pdb = ''.join(input_chain[:4])
		chain = input_chain[4].strip()

		feature_map[pdb+chain.upper()] = {}

		#Artificially adding number of domains a feature.
		feature_map[pdb+chain.upper()]["Domains"] = utils.findNumberOfDomains(pdb, chain)

		for feature in feature_set:
			feature_calculator = features.get(feature, "Invalid input feature")
			feature_value = feature_calculator(pdb, chain)


			if isinstance(feature_value, float):
				feature_map[pdb+chain.upper()][feature] = '{0:.3}'.format(feature_value)
			else:
				feature_map[pdb+chain.upper()][feature] = feature_value

	return feature_map

'''
This method is the ingress point for calculating features for a given input list of chains in the format pdb+chain
along with the number of clusters as an input. The number of clusters are important for calculating features
like Interaction Energy & Density Sum.

PLEASE USE THIS METHOD FOR TESTING DATASET

Feature set is a list of the features that needs to be calculated.

Returns the calculated features in the following format in a map
{
	pdb1+chain1: [feature11, feature12, feature13, feature14]
	pdb2+chain2: [feature21, feature22, feature23, feature24]
	.
	.
	.
	.

}
'''
def calculateFeatures_v2(input_chains, feature_set, num_of_clusters):
	feature_map = {}
	for input_chain in input_chains:
		feature_values = []
		input_chain = list(input_chain)

		pdb = ''.join(input_chain[:4])
		chain = input_chain[4]

		# feature_map[pdb+chain.upper()] = {}

		# feature_map[pdb+chain.upper()]["Domains"] = utils.findNumberOfDomains(pdb, chain)

		for feature in feature_set:
			feature_calculator = features.get(feature, "Invalid input feature") 

			if feature=="Interaction_Energy" or feature=="Density_Sum" or feature=="IS-Sum_2" or feature=="IS-Sum_3" or feature=="IS-Sum_4":
				if feature=="IS-Sum_2":
					feature_value = feature_calculator(pdb, chain, 2)

				elif feature=="IS-Sum_3":
					feature_value = feature_calculator(pdb, chain, 3)
					
				elif feature=="IS-Sum_4":
					feature_value = feature_calculator(pdb, chain, 4)
				else:
					feature_value = feature_calculator(pdb, chain, num_of_clusters)
			else:
				feature_value = feature_calculator(pdb, chain)	

			if isinstance(feature_value, float):
				feature_values.append('{0:.3}'.format(feature_value))
				# feature_map[pdb+chain.upper()][feature] = '{0:.3}'.format(feature_value)
			else:
				feature_values.append(feature_value)
				# feature_map[pdb+chain.upper()][feature] = feature_value
		feature_map[pdb+chain] = feature_values

	return feature_map





