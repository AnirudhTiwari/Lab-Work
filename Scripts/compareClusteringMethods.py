import os
import math
from igraph import *
from sklearn.cluster import *
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import re
from compiler.ast import flatten
from operator import itemgetter
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import MeanShift
from sklearn.cluster import spectral_clustering
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn import mixture
# from sklearn import Birch


def value_finder(start_residue, array):
	coordinate = ''

	while(array[start_residue]==' '):
		start_residue = start_residue+1

	while(array[start_residue]!=' '):
		coordinate = coordinate + array[start_residue];
		start_residue = start_residue + 1

		if(array[start_residue]=='-'):
			break

	return coordinate

def getCordsList(fileRead, chain):
	cords_list = []
	realId_list = []

	while 1:

		data = fileRead.readline()

		if not data:
			break

		if(data[0]=='E' and data[1]=='N' and data[2]=='D'):
			break

		if(data[0]=='A' and data[1]=='T' and data[2]=='O' and data[21]==chain and data[13]=='C' and data[14]=='A'):

			coord_x = float(value_finder(27, data))
			coord_y = float(value_finder(39, data))
			coord_z = float(value_finder(47, data))
			val = value_finder(22, data)
		
			if not re.search('[a-zA-Z]+', val):
				real_id = int(val)

				if real_id not in realId_list:

					coordinates = [coord_x,coord_y,coord_z]

					cords_list.append(coordinates)
					realId_list.append(real_id)

	return cords_list,realId_list

def domainBoundaries(matrix, realId_list, domains):
	new_dict = {}
	for y in range(len(matrix)):
		if matrix[y] in new_dict:
			new_dict[matrix[y]].append(realId_list[y])

		else:
			new_dict[matrix[y]] = [realId_list[y]]

	return new_dict

def makeReadable(boundaries):
	# print boundaries
	temp_list = []
	flag = 0

	for x in range(0,len(boundaries)-1):
		if boundaries[x+1] - boundaries[x]==1:
			temp_list.append(boundaries[x])

		else:
			if len(temp_list)!=0:
				temp_list.append(boundaries[x])
				# print temp_list
				print min(temp_list), "-", max(temp_list),
				temp_list = []

	if flag==0 and len(temp_list)!=0:
		# print temp_list
		print  min(temp_list), "-", max(temp_list)+1,

	print "&",

def dist(a,b):
	# print a, b
	for x in range(3):
		distance = math.pow((math.pow((a[0]-b[0]),2) + math.pow((a[1]-b[1]),2) + math.pow((a[2]-b[2]),2)), 0.5)
		return distance

def getInteractionEnergy(matrix, num_domains, cords_list):
	clusters_dict = defaultdict(list)

	for x in range(len(matrix)):
		clusters_dict[matrix[x]].append(x)

	energy = 0

	for y in clusters_dict:
		for z in clusters_dict:
			if y!=z:
				for a in clusters_dict[y]:
					for b in clusters_dict[z]:
						distance = dist(cords_list[a],cords_list[b])
						if distance < 7.0:
							energy = energy + 1/distance

	return (energy/2)/len(matrix)

def maxOverlap(cath_domain, k_means):
	overlap = -1000000000
	for key, value in k_means.iteritems():
		counter = 0
		for x in value:
			if x in cath_domain:
				counter+=1
		if counter > overlap:
			kmeans_key = key
			overlap = counter
	return kmeans_key

def mapCorrectly(cath, k_means):

	kmeans_keys = []
	for key, value in cath.iteritems():
		kmeans_keys.append(maxOverlap(value,k_means))

	new_kmeans = {}

	if len(list(set(kmeans_keys)))!=len(cath):
		kmeans_keys = list(set(kmeans_keys))

	for x in range(len(kmeans_keys)):
		new_kmeans[x] = k_means.get(kmeans_keys[x])

	return cath, new_kmeans



def stitchPatches(k_means, cluster_centers, coordinates, realId_list,patch_length):
	island = []
	for key, value in k_means.iteritems():
		x=0
		while x!=len(value):
			counter=0
			for y in range(x+1,len(value)-1,1):
				if value[y]-value[y-1]!=1:
					if len(value[x:y])<= patch_length:
						patch = value[x:y]
						island.append(patch)
					break

				elif y==len(value)-2:
					if len(value[x:y+2])<=patch_length:
						patch = value[x:y+2]
						island.append(patch)
					break
				counter+=1
			x+=(counter+1)

	island = internalStitch(island, patch_length)

	mean_list = []
	for key, value in k_means.iteritems():
		# mean_list.append(1.0*sum(value)/len(value))
		for patches in island:
			for x in patches:
				if x in value:
					value.remove(x)

	k_means = sequenceStitch(k_means, island)
	# k_means = centroidStitch(k_means, island, coordinates, realId_list, cluster_centers)
	
	# k_means = interactionEnergyStitch(k_means, island, coordinates, realId_list)
	return k_means

def interactionEnergyStitch(k_means, island, coordinates, realId_list):

	for patches in island:
		energy_list = []
		energy = 0
		for key,value in k_means.iteritems():
			for x in patches:
				for y in value:
					if y!=x:
						if x in realId_list and y in realId_list:
							a = coordinates[realId_list.index(x)]
							b = coordinates[realId_list.index(y)]
							val = math.pow((math.pow((a[0]-b[0]),2) + math.pow((a[1]-b[1]),2) + math.pow((a[2]-b[2]),2)), 0.5)
							energy = energy + 1/1.0*val
			energy_list.append(energy)

		index = energy_list.index(max(energy_list))
		k_means[index] = sorted(list(set(k_means[key] + patches)))

	return k_means

def centroidStitch(k_means, island, coordinates, realId_list, cluster_centers):
	
	for patch in island:
		mean = [0, 0, 0]
		distance_list = []
		for residue in patch:
			if residue in realId_list:
				for x in range(len(mean)):
					mean[x] = mean[x] + coordinates[realId_list.index(residue)][x]
		for x in range(len(mean)):		
			mean[x] = (1.0*mean[x])/len(patch)

		for centers in cluster_centers:
			distance =  math.pow((math.pow((centers[0]-mean[0]),2) + math.pow((centers[1]-mean[1]),2) + math.pow((centers[2]-mean[2]),2)), 0.5)
			distance_list.append(distance)
		key = distance_list.index(min(distance_list))
		k_means[key] = sorted(list(set(k_means[key]  + patch)))

	return k_means

def sequenceStitch(k_means, island):
	minimum = 100000000
	for key, values in k_means.iteritems():
		if minimum > min(values):
			minimum = min(values)

	for patches in island:
		low = patches[0] - 1
		high = patches[-1] + 1
		for key, value in k_means.iteritems():
			if low < minimum:
				if high in value:
					k_means[key] = sorted(list(set(k_means[key]  + patches)))

			if low in value and high in value:
				k_means[key] = sorted(list(set(k_means[key]  + patches)))

			if low in value and high not in value:
				k_means[key] = sorted(list(set(k_means[key]  + patches)))
	return k_means

def internalStitch(island, patch_length):
	remove = []
	for x in range(len(island)-1):
		island.sort(key=itemgetter(0))
		high = max(island[x])+1

		if high==island[x+1][0] and (len(island[x]) + len(island[x+1]) <= patch_length):
			remove.append(x)
			island[x+1] = sorted(island[x] + island[x+1])

	final = []
	for x in range(len(island)):
		if x not in remove:
			final.append(island[x])

	return final

def compareResults(cath, k_means,domains):
	domain_length = 0
	for x in range(domains):
		domain_length = domain_length + len(cath.get(x))

	score = 0
	domains = min(len(k_means), len(cath))
	for x in range(domains):
		temp_list = []

		if len(cath.get(x)) < len(k_means.get(x)):
			for y in cath.get(x):
				if y in k_means.get(x):
					temp_list.append(y)
			# score =  ((100*len(temp_list))/len(k_means.get(x)))*(1.0*len(temp_list)/domain_length) + score
			score = len(temp_list) + score

		else:
			for y in k_means.get(x):
				if y in cath.get(x):
					temp_list.append(y)

			# score = (100*len(temp_list))/len(cath.get(x))*(1.0*len(temp_list)/domain_length) + score
			score = len(temp_list) + score


	return (100.0*(1.0*score/domain_length))

def getCathDict(cath_boundaries, domains):
	cath_boundaries = cath_boundaries.split(" ")
	cath_boundaries = filter(None, cath_boundaries)
	cathDict = {}
	key = 0
	numOFSegments = 1
	x = 0
	while 1:
		if x >= len(cath_boundaries):
			break
		else:
			numOFSegments = int(cath_boundaries[x])
			dom = cath_boundaries[x:x+6*numOFSegments+1]
			dom = makeList(dom)
			cathDict[key] = dom
			key+=1
			x+=6*numOFSegments+1
	return cathDict

def makeList(domain):
	domainList = []
	segments = domain[0]
	chain = domain[1]
	insert_character = domain[3]
	domain = list(filter(lambda x: x!=chain and x!=insert_character, domain[1:]))

	for x in xrange(0,len(domain)-1,2):
		temp_list = []
		lower_bound = int(domain[x])
		upper_bound = int(domain[x+1])

		for y in range(lower_bound, upper_bound+1):
			temp_list.append(y)
		domainList.append(temp_list)

	return flatten(domainList)

def fillVoids(boundaries):
	for key, value in boundaries.iteritems():
		for x in range(min(value), max(value)+1):
			if x not in value:
				if x not in flatten(boundaries.values()):
					value.append(x)
		boundaries[key] = sorted(value)
	return boundaries


def isContiguous(cath_boundaries):
	cath_boundaries = cath_boundaries.split(" ")
	cath_boundaries = filter(None, cath_boundaries)
	x = 0
	while 1:
		if x >= len(cath_boundaries):
			break
		else:
			numOFSegments = int(cath_boundaries[x])
			if numOFSegments > 1:
				return False
			else:
				x+=6*numOFSegments+1
	return True

# path = "../Output Data/Two Domain Proteins/"
# path = "../Output Data/500_proteins/"
path = "../Output Data/500_proteins/Contiguous/"

file_counter = 0
correct = 0
km_accuracy = 0.0
ap_accuracy = 0.0
ms_accuracy = 0.0
sc_accuracy = 0.0
wh_accuracy = 0.0
ca_accuracy = 0.0
aa_accuracy = 0.0
dbscan_accuracy = 0.0
gauss_accuracy = 0.0
birch_accuracy = 0.0

not_list = ['1adh','1baa', '1a4k', '1abk','3g4s', '1aak', '1ace', '1fnr']#'4gcr', '2pmg', '1vsg', '8atc', '8adh', '1wsy', '3grs', '1gky','1rhd','1ezm', '1sgt']

print "No., PDB, Domains, CATH, K-Means, Overlap, Affinity Propagation, Overlap, Mean Shift, Overlap, Ward-Hierarchical, Overlap, Complete Agglomerative, Overlap, Avg. Agglomerative, Overlap, DBSCAN, Overlap, Birch, Overlap"
for pdb_file in os.listdir(path):

	if file_counter>=100:
		break

	pdb_path = pdb_file
	pdb_file = pdb_file.split(".")[0].lower()

	flag = 0


	var = open('../Input Files/CathDomall', 'r')


	while 1:

		pdb_id = var.readline()

		if not pdb_id:
			break

		else:

			if pdb_id[:4].lower()==pdb_file[:4].lower() and pdb_file not in not_list:

				var_1 = open(path+pdb_path, 'r')

				chain = pdb_id[18]

				domains = int(pdb_id[7] + pdb_id[8])

				frags = int(pdb_id[11] + pdb_id[12])
			
				domain_boundary = pdb_id[14:].strip()

				if frags==0 and isContiguous(domain_boundary) and domains > 1:

					print str(file_counter + 1) + "," + pdb_id[:4] + ", " + str(domains) + ", " + domain_boundary, "," ,
					cords_list, realId_list = getCordsList(var_1,chain)

					x = np.asarray(cords_list)
					file_counter+=1
					cathDict = getCathDict(domain_boundary, domains)


					#======================K-MEANS================================================

					km = KMeans(n_clusters=domains).fit(x)

					labels_km = km.labels_
					clusters_km = km.cluster_centers_

					km_boundaries = domainBoundaries(labels_km, realId_list,domains)

					km_boundaries = fillVoids(km_boundaries)
					# boundaries = stitchPatches(boundaries, clusters_km, cords_list, realId_list, 15)


					cathDict, km_boundaries = mapCorrectly(cathDict, km_boundaries)

					km_overlap = compareResults(cathDict, km_boundaries, domains)

					km_accuracy = km_accuracy + km_overlap

					for key, value in km_boundaries.iteritems():
						makeReadable(value)
					print ", " + "{0:.2f}".format(km_overlap)+", ",

					#======================AFFINITY-PROPAGATION=================================================


					ap = AffinityPropagation().fit(x)

					labels_ap = ap.labels_
					clusters_ap = ap.cluster_centers_

					ap_boundaries = domainBoundaries(labels_ap, realId_list,domains)

					ap_boundaries = fillVoids(ap_boundaries)

					# ap_boundaries = stitchPatches(ap_boundaries, clusters_ap, cords_list, realId_list, 15)

					cathDict, ap_boundaries = mapCorrectly(cathDict, ap_boundaries)

					ap_overlap = compareResults(cathDict, ap_boundaries, domains)

					ap_accuracy = ap_accuracy + ap_overlap

					for key, value in ap_boundaries.iteritems():
						makeReadable(value)
					print ", " + "{0:.2f}".format(ap_overlap)+", ",

					#==============================MEAN-SHIFT================================================

					ms = MeanShift().fit(x)

					labels_ms = ms.labels_
					clusters_ms = ms.cluster_centers_

					ms_boundaries = domainBoundaries(labels_ms, realId_list,domains)

					ms_boundaries = fillVoids(ms_boundaries)

					# ms_boundaries = stitchPatches(ms_boundaries, clusters_ms, cords_list, realId_list, 15)

					cathDict, ms_boundaries = mapCorrectly(cathDict, ms_boundaries)

					ms_overlap = compareResults(cathDict, ms_boundaries, domains)

					ms_accuracy = ms_accuracy + ms_overlap

					for key, value in ms_boundaries.iteritems():
						makeReadable(value)
					print ", " + "{0:.2f}".format(ms_overlap)+", ",

					#==============================SPECTRAL-CLUSTERING================================================

					# sc = spectral_clustering(cords_list)

					# labels_sc = sc.labels_
					# clusters_sc = sc.cluster_centers_

					# sc_boundaries = domainBoundaries(labels_sc, realId_list,domains)

					# sc_boundaries = fillVoids(sc_boundaries)

					# # sc_boundaries = stitchPatches(sc_boundaries, clusters_sc, cords_list, realId_list, 15)

					# cathDict, sc_boundaries = mapCorrectly(cathDict, sc_boundaries)

					# sc_overlap = compareResults(cathDict, sc_boundaries, domains)

					# sc_accuracy = sc_accuracy + sc_overlap

					# for key, value in sc_boundaries.iteritems():
					# 	makeReadable(value)
					# print ", " + "{0:.2f}".format(sc_overlap)+", ",

					#==============================WARD-HIERARCHICAL================================================

					wh = AgglomerativeClustering(n_clusters=domains).fit(x)

					labels_wh = wh.labels_

					# clusters_wh = wh.cluster_centers_

					wh_boundaries = domainBoundaries(labels_wh, realId_list,domains)

					wh_boundaries = fillVoids(wh_boundaries)

					# wh_boundaries = stitchPatches(wh_boundaries, clusters_wh, cords_list, realId_list, 15)

					cathDict, wh_boundaries = mapCorrectly(cathDict, wh_boundaries)

					wh_overlap = compareResults(cathDict, wh_boundaries, domains)

					wh_accuracy = wh_accuracy + wh_overlap

					for key, value in wh_boundaries.iteritems():
						makeReadable(value)
					print ", " + "{0:.2f}".format(wh_overlap)+", ",

					

					#==============================COMPLETE-AGGLOMERATIVE================================================

					ca = AgglomerativeClustering(n_clusters=domains, linkage="complete").fit(x)

					labels_ca = ca.labels_

					# clusters_ca = ca.cluster_centers_

					ca_boundaries = domainBoundaries(labels_ca, realId_list,domains)

					ca_boundaries = fillVoids(ca_boundaries)

					# ca_boundaries = stitchPatches(ca_boundaries, clusters_ca, cords_list, realId_list, 15)

					cathDict, ca_boundaries = mapCorrectly(cathDict, ca_boundaries)

					ca_overlap = compareResults(cathDict, ca_boundaries, domains)

					ca_accuracy = ca_accuracy + ca_overlap

					for key, value in ca_boundaries.iteritems():
						makeReadable(value)
					print ", " + "{0:.2f}".format(ca_overlap)+", ",


					#==============================AVERAGE-AGGLOMERATIVE================================================

					aa = AgglomerativeClustering(n_clusters=domains, linkage="average").fit(x)

					labels_aa = aa.labels_

					# clusters_aa = aa.cluster_centers_

					aa_boundaries = domainBoundaries(labels_aa, realId_list,domains)

					aa_boundaries = fillVoids(aa_boundaries)

					# aa_boundaries = stitchPatches(aa_boundaries, clusters_aa, cords_list, realId_list, 15)

					aathDict, aa_boundaries = mapCorrectly(cathDict, aa_boundaries)

					aa_overlap = compareResults(aathDict, aa_boundaries, domains)

					aa_accuracy = aa_accuracy + aa_overlap

					for key, value in aa_boundaries.iteritems():
						makeReadable(value)
					print ", " + "{0:.2f}".format(aa_overlap)+", ",

					
					#==============================DBSCAN================================================

					dbscan = DBSCAN().fit(x)

					labels_dbscan = dbscan.labels_

					# clusters_dbscan = dbscan.cluster_centers_

					dbscan_boundaries = domainBoundaries(labels_dbscan, realId_list,domains)

					dbscan_boundaries = fillVoids(dbscan_boundaries)

					# dbscan_boundaries = stitchPatches(dbscan_boundaries, clusters_dbscan, cords_list, realId_list, 15)

					cathDict, dbscan_boundaries = mapCorrectly(cathDict, dbscan_boundaries)

					dbscan_overlap = compareResults(cathDict, dbscan_boundaries, domains)

					dbscan_accuracy = dbscan_accuracy + dbscan_overlap

					for key, value in dbscan_boundaries.iteritems():
						makeReadable(value)
					print ", " + "{0:.2f}".format(dbscan_overlap)+", ",

					#==============================Gaussian Mixture================================================

					# gauss = mixture.GMM().fit(x)

					# labels_gauss = gauss.labels_

					# # clusters_gauss = gauss.cluster_centers_

					# gauss_boundaries = domainBoundaries(labels_gauss, realId_list,domains)

					# gauss_boundaries = fillVoids(gauss_boundaries)

					# # gauss_boundaries = stitchPatches(gauss_boundaries, clusters_gauss, cords_list, realId_list, 15)

					# cathDict, gauss_boundaries = mapCorrectly(cathDict, gauss_boundaries)

					# gauss_overlap = compareResults(cathDict, gauss_boundaries, domains)

					# gauss_accuracy = gauss_accuracy + gauss_overlap

					# for key, value in gauss_boundaries.iteritems():
					# 	makeReadable(value)
					# print ", " + "{0:.2f}".format(gauss_overlap)+", ",

					#==============================BIRCH================================================

					birch = Birch(n_clusters=domains).fit(x)

					labels_birch = birch.labels_

					# clusters_birch = birch.cluster_centers_

					birch_boundaries = domainBoundaries(labels_birch, realId_list,domains)

					birch_boundaries = fillVoids(birch_boundaries)

					# birch_boundaries = stitchPatches(birch_boundaries, clusters_birch, cords_list, realId_list, 15)

					cathDict, birch_boundaries = mapCorrectly(cathDict, birch_boundaries)

					birch_overlap = compareResults(cathDict, birch_boundaries, domains)

					birch_accuracy = birch_accuracy + birch_overlap

					for key, value in birch_boundaries.iteritems():
						makeReadable(value)
					print ", " + "{0:.2f}".format(birch_overlap)

print "No., PDB, Domains, CATH, K-Means, Avg. Overlap(K-Means), Affinity Propagation, Avg. Overlap(Affinity), Mean Shift, Avg. Overlap(Mean Shift), Ward-Hierarchical, Avg. Overlap(Ward), Complete Agglomerative, Avg. Overlap(Complete Agglo), Average Agglomerative(Avg. Agglo), Avg. Overlap, DBSCAN, Avg. Overlap(DBSCAN), Birch, Avg. Overlap(Birch)"
print ",,,,,",km_accuracy/file_counter,",,",ap_accuracy/file_counter,",,",ms_accuracy/file_counter,",,",wh_accuracy/file_counter,",,",ca_accuracy/file_counter,",,",aa_accuracy/file_counter,",,",dbscan_accuracy/file_counter,",,",birch_accuracy/file_counter

# print "accuracy is", accuracy/file_counter
