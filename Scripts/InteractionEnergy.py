from itertools import combinations
import common_functions as utils
from collections import defaultdict


cutoff_distance = 7.0; #The maximum distance between two residues for them to be considered interacting

'''
Those residues which are closer than the cutoff_distance are said to be interacting. The interaction energy is the total number of 
such inter-cluster residues divided by total number of intra-cluster residues. 
Formally, IE = Nxy/Nx+Ny => Nxy: Number of inter-cluster interactions, Nx: Intra-cluster interaction in cluster X, Ny: Intra-cluster interactions in cluster Y
'''
def calculateInteractionEnergy(cluster_labels, coordinates_list):
	#A dictionary of cluster label as key and the corresponding residue indices as values
	clusters_dict = defaultdict(list)
	
	for x in range(len(cluster_labels)):
		clusters_dict[cluster_labels[x]].append(x)


	intra_cluster_interaction_energy_dict = {}

	for key, value in clusters_dict.iteritems():
		intra_cluster_interaction_energy_dict[key] = calculateIntraClusterInteractionEnergy(value, coordinates_list)

	pairs_of_clusters = list(combinations(clusters_dict.keys(), 2))

	interacton_energy = 0.0

	for pair in pairs_of_clusters:
		cluster_X = clusters_dict[pair[0]]
		cluster_Y = clusters_dict[pair[1]]
		Nxy = calculateInterClusterInteractionEnergy(cluster_X, cluster_Y, coordinates_list)
		Nx = intra_cluster_interaction_energy_dict[pair[0]]
		Ny = intra_cluster_interaction_energy_dict[pair[1]]

		interacton_energy+=100.0*(Nxy/(Nx+Ny))

	return interacton_energy


def calculateInterClusterInteractionEnergy(cluster_X, cluster_Y, coordinates_list):
	inter_cluster_interaction_energy = 0.0
	pairs_of_inter_cluster_residues = [(x,y) for x in cluster_X for y in cluster_Y]

	for pair in pairs_of_inter_cluster_residues:
		inter_cluster_interaction_energy+=getPairwiseInteractionEnergy(pair, coordinates_list)

	return inter_cluster_interaction_energy



def calculateIntraClusterInteractionEnergy(cluster_X, coordinates_list):
	intra_cluster_interaction_energy = 0.0

	pairs_of_intra_cluster_residues = list(combinations(cluster_X, 2))

	for pair in pairs_of_intra_cluster_residues:
		intra_cluster_interaction_energy+=getPairwiseInteractionEnergy(pair, coordinates_list)
		

	return intra_cluster_interaction_energy


def getPairwiseInteractionEnergy(pair, coordinates_list):
	coordinate_A = coordinates_list[pair[0]]
	coordinate_B = coordinates_list[pair[1]]
	
	distance = utils.dist(coordinate_A, coordinate_B)
	
	if distance <= cutoff_distance:
		return 1
	
	return 0

