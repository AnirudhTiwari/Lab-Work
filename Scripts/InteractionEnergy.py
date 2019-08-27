from itertools import combinations
import common_functions as utils
from collections import defaultdict
import numpy as np
from sklearn.cluster import KMeans
import K_Means as kMeansInternal

cutoff_distance = 7.0; #The maximum distance between two residues for them to be considered interacting

path_to_pdb_files = 'All PDBs/'
'''
This method assumes that the number of domains is as per CATH and fetches the
same from CATH and performs k-means based on that number of domains.
'''
# def calculateInteractionEnergy(pdb, chain):
# 	domains = utils.findNumberOfDomains(pdb, chain)

# 	coordinates_list = utils.getCoordinatesListFromPDB(pdb, chain)

# 	numpy_array = np.asarray(coordinates_list)
# 	kMeans = KMeans(n_clusters=domains).fit(numpy_array)

# 	labels_kMeans = kMeans.labels_

# 	return calculateInteractionEnergyForAGivenSplit(labels_kMeans, coordinates_list)


'''
This method calculates the pairwise interactionEnergy for a given pdb, chain and the number of clusters.
'''
def calculateInteractionEnergy(pdb, chain, number_of_clusters=None):
	if number_of_clusters==None:
		number_of_clusters = utils.findNumberOfDomains(pdb, chain)
	if number_of_clusters==1:
		number_of_clusters=2

	coordinates_list = utils.getCoordinatesListFromPDB(pdb, chain)

	numpy_array = np.asarray(coordinates_list)
	kMeans = KMeans(n_clusters=number_of_clusters).fit(numpy_array)

	# Merging/Re-arranging small fragments before calculating Interaction Energy.

	labels_kMeans = kMeans.labels_
	clusters_km =  kMeans.cluster_centers_

	#unecessary step as getCordsList take pdb_file as an input!
	pdb_file = open(path_to_pdb_files+pdb+'.pdb','r')
	cords_list, realId_list = kMeansInternal.getCordsList(pdb_file, chain.upper())

	boundaries = kMeansInternal.getDomainBoundaries(labels_kMeans, realId_list, number_of_clusters)

	for key,value in boundaries.iteritems():
		boundaries[key] = list(set(value))

	if not kMeansInternal.TooManyMissingResidues(boundaries):
		boundaries = kMeansInternal.fillVoids(boundaries)
	else:
		boundaries = kMeansInternal.fillVoids(boundaries)

#Hard coding patch size as 20
	new_boundaries = kMeansInternal.stitchPatchesWithoutSequenceStitch(boundaries, clusters_km, cords_list, realId_list, 20)

	return calculateInteractionEnergyForAGivenSplit(labels_kMeans, coordinates_list)


'''
Those residues which are closer than the cutoff_distance are said to be interacting. The interaction energy is the total number of 
such inter-cluster residues divided by total number of intra-cluster residues. 
Formally, IE = Nxy/Nx+Ny => Nxy: Number of inter-cluster interactions, Nx: Intra-cluster interaction in cluster X, Ny: Intra-cluster interactions in cluster Y
'''
def calculateInteractionEnergyForAGivenSplit(cluster_labels, coordinates_list):

	#A dictionary of cluster label as key and the corresponding residue indices as values
	clusters_dict = defaultdict(list)
	
	for x in range(len(cluster_labels)):
		clusters_dict[cluster_labels[x]].append(x)

	clusters_dict = defaultdict(int, clusters_dict)

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
	coordinate_A = coordinates_list[pair[0]-1]
	coordinate_B = coordinates_list[pair[1]-1]
	
	distance = utils.dist(coordinate_A, coordinate_B)
	
	if distance <= cutoff_distance:
		return 1
	
	return 0

def transformNewBoundariesToLabels_kMeans(coordinatesDict):
	return 0


