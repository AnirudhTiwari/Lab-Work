'''
This module tries to identify the number of domains for a given multi-domain chain. The algorithm is a follows:
1. The feature set, training & test dataset is already provided, based on the training dataset the SVM is trained
2. For each of the test dataset entry, for k=2 to 4 features are calculated. 
3. For each feature set corresponding to a given k, the confidence score of the SVM is calculated
4. The k for which the confidence score is maximum is taken to be the correct value
'''
from sklearn.cluster import *
import common_functions as utils
from collections import defaultdict
import InteractionEnergy
import numpy as np
import re
import Density
import calculateFeatures
from sklearn import svm

path_to_pdb_files = 'All PDBs/'

# def identifyNumberOfDomains(training_dataset_with_features, testing_dataset, feature_set):
	
	# X_train, y_train = utils.extractFeaturesAndLabelsForSVM(training_data, feature_set, classification_type)


def identifyNumberOfDomainsForAGivenPdbAndChain(pdb, chain, feature_set):
	print pdb, chain, feature_set

	for k in range (2, 5):
		numpy_array = np.asarray(coordinates_list)
		kMeans = KMeans(n_clusters=k).fit(numpy_array)

		labels_kMeans = kMeans.labels_

		features_map = calculateFeatures.calculateFeatures([pdb+chain], feature_set, k)

		features = features_map[pdb+chain]


	return num_of_clusters


'''
Given a cluster label for each coordinate and a coordinate list, this method returns a map of cluster label to list of coordinates
{
	0: [[x1, y1, z1], [x2, y2, z2], [x3, y3, z3].....]
	1: [[x130, y130, z130], [x131, y131, z131]....]
}
'''
def getCoordinatesListOfEachCluster(cluster_labels, coordinates_list):
	clusters_dict = defaultdict(list)
	
	for x in range(len(cluster_labels)):
		clusters_dict[cluster_labels[x]].append(coordinates_list[x])

	return clusters_dict


def calculateTotalDensityOfClusters(cluster_coordinates):
	total_density = 0.0
	for cluster, coordinates in cluster_coordinates.iteritems():
		total_density+=Density.calculateDensity(coordinates)

	return total_density



		


		
