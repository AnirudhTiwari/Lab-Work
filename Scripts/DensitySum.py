'''
This method splits a given chain into the given number of domains and calculates the sum of densities of each domain
'''

path_to_pdb_files = 'All PDBs/'

from sklearn.cluster import KMeans
import common_functions as utils
from collections import defaultdict
import numpy as np
import Density


def calculateDensitySumForAChainWithGivenDomains(pdb, chain, domains):
	pdb_file = open(path_to_pdb_files+pdb+'.pdb','r')
	coordinates_list = utils.getCoordinatesListFromPDB(pdb, chain)

	numpy_array = np.asarray(coordinates_list)
	kMeans = KMeans(n_clusters=domains).fit(numpy_array)

	labels_kMeans = kMeans.labels_

	cluster_coordinates = getCoordinatesListOfEachCluster(labels_kMeans, coordinates_list)

	total_density = calculateTotalDensityOfClusters(cluster_coordinates)

	return total_density

def getCoordinatesListOfEachCluster(cluster_labels, coordinates_list):
	clusters_dict = defaultdict(list)
	
	for x in range(len(cluster_labels)):
		clusters_dict[cluster_labels[x]].append(coordinates_list[x])

	return clusters_dict


def calculateTotalDensityOfClusters(cluster_coordinates):
	total_density = 0.0
	for cluster, coordinates in cluster_coordinates.iteritems():
		total_density+=Density.calculateDensityOfACluster(coordinates)

	return total_density


'''
In the case when the number of clusters are not specified, this program then fetches
the number of domains from CATH and uses it.
'''
def calculateDensitySum(pdb, chain, num_of_clusters=None):
	if num_of_clusters==None:
		num_of_clusters = utils.findNumberOfDomains(pdb, chain)

	return calculateDensitySumForAChainWithGivenDomains(pdb, chain, num_of_clusters)
