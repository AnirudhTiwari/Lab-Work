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

	print "--",

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
		print "K-MEANS SCREWED IT UP", kmeans_keys,

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

	# k_means = sequenceStitch(k_means, island)
	# k_means = centroidStitch(k_means, island, coordinates, realId_list, cluster_centers)
	
	k_means = interactionEnergyStitch(k_means, island, coordinates, realId_list)
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

# path = "../Output Data/Two Domain Proteins/"
path = "../Output Data/500_proteins/"

file_counter = 0
correct = 0
accuracy = 0.0

print "No., PDB, Domains, CATH, K-Means, Accuracy"
for pdb_file in os.listdir(path):

	if file_counter>=1:
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

			if pdb_id[:4].lower()==pdb_file[:4].lower() and pdb_file!='1adh' and pdb_file!='1baa' and pdb_file!='1a4k' and pdb_file!='1abk' and pdb_file!='3g4s' and pdb_file=='1xf1':
				flag = 1

				var_1 = open(path+pdb_path, 'r')

				chain = pdb_id[18]

				domains = int(pdb_id[7] + pdb_id[8])

				frags = int(pdb_id[11] + pdb_id[12])

				if frags==0: #and domains==2:
					domain_boundary = pdb_id[14:].strip()

					print str(file_counter + 1) + "," + pdb_id[:4] + ", " + str(domains) + ", " + domain_boundary, "," ,
					cords_list, realId_list = getCordsList(var_1,chain)

					x = np.asarray(cords_list)
					file_counter+=1

					km = KMeans(n_clusters=domains, max_iter=1000, n_init=30, init='random').fit(x)

					labels_km = km.labels_
					clusters_km = km.cluster_centers_

					boundaries = domainBoundaries(labels_km, realId_list,domains)

					boundaries = fillVoids(boundaries)
					boundaries = stitchPatches(boundaries, clusters_km, cords_list, realId_list, 15)

					cathDict = getCathDict(domain_boundary, domains)

					cathDict, boundaries = mapCorrectly(cathDict, boundaries)

					overlap = compareResults(cathDict, boundaries, domains)

					accuracy = accuracy + overlap

					for key, value in boundaries.iteritems():
						makeReadable(value)
					print ", " + "{0:.2f}".format(overlap)

print "accuracy is", accuracy/file_counter
