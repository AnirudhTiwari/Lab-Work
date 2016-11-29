import os
import math
from igraph import *
from sklearn.cluster import *
import numpy as np
from collections import defaultdict
import re
from compiler.ast import flatten
from operator import itemgetter

patch_size = 20 #Defines the min length a segment of a non-contiguous domain can be. Any segment less than this should be merged to the contiguous part.

def value_finder(start_value, end_value, array):

	coordinate = ''

	while array[start_value]==' ':
		start_value = start_value+1



	while int(start_value)!=int(end_value):
		coordinate = coordinate + array[start_value];
		start_value = start_value + 1

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

			val = value_finder(22, 26, data)	
						
			coord_x = float(value_finder(30, 38, data))

			coord_y = float(value_finder(38, 46, data))

			coord_z = float(value_finder(46, 54, data))
		
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
				print min(temp_list), "-", max(temp_list), "  ",
				temp_list = []

	if flag==0 and len(temp_list)!=0:
		# print temp_list
		print  min(temp_list), "-", max(temp_list)+1,

	# print "--",
	# print

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
		print "K-MEANS SCREWED IT UP",

	for x in range(len(kmeans_keys)):
		new_kmeans[x] = k_means.get(kmeans_keys[x])

	return cath, new_kmeans

def checkLastTwoResidues(value, island):
	answer = []
	
	if value[-2]-value[-3]!=1:
		answer.append(value[-2])

	if value[-1]-value[-2]!=1 and len(answer)==0:
		answer.append(value[-1])
		island.append(answer)

	if value[-1]-value[-2]!=1 and len(answer)==1:
		island.append(answer)
		island.append([value[-1]])

	if value[-1]-value[-2]==1 and len(answer)==1:
		answer.append(value[-1])
		island.append(answer)

	return island


def stitchPatches(k_means, cluster_centers, coordinates, realId_list,patch_length): #WRITE A SEPARATE FUNCTION TO FIND ISLANDS
	# print k_means
	# print "BEFORE STITCHING PATCHES"
	
	# for key,value in k_means.iteritems():
	# 	print key, value

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

		island = checkLastTwoResidues(value, island)


	# print "ISLANDS BEFORE INTERNAL STITCH"
	# print sorted(island)
	island = internalStitch(sorted(island), patch_length)

	# print 
	# print "ISLANDS AFTER INTERNAL STITCH"
	# print island

	mean_list = []
	for key, value in k_means.iteritems():
		# mean_list.append(1.0*sum(value)/len(value))
		for patches in island:
			for x in patches:
				if x in value:
					value.remove(x)

	k_means, island = sequenceStitch(k_means, island)

	# print "RESIDUAL ISLAND"
	# print island 
	if len(island)!=0:
		k_means = centroidStitch(k_means, island, coordinates, realId_list)

	# k_means = centroidStitch(k_means, island, coordinates, realId_list, cluster_centers)
	
	# k_means = interactionEnergyStitch(k_means, island, coordinates, realId_list)

	# print "FINALLY RETURN K-MEANS 2"


	# for key, value in k_means.iteritems():
	# 	print key, value
	# 	print
	# 	print

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

def calculateCentroid(residues, coordinates, realId_list):
	centroid = [0.0, 0.0, 0.0]

	for residue in residues:
		if residue in realId_list:
			for a in range(len(centroid)):
				centroid[a] = centroid[a] + coordinates[realId_list.index(residue)][a]

	for x in range(len(centroid)):
		centroid[x] = (1.0*centroid[x])/len(residues)

	return centroid


def centroidStitch(k_means, island, coordinates, realId_list):

	# print "Onto Centroid STITCH"

	cluster_centroid_dict = {};

	for key, value in k_means.iteritems():
		cluster_centroid = calculateCentroid(value, coordinates, realId_list)
		# print "FOR CLUSTER ", key, "Centroid is ", cluster_centroid

		cluster_centroid_dict[key] = cluster_centroid

	# for key, value in k_means.iteritems():
	# 	print key, value
	# 	print
	# 	print


	# for x in island:
	# 	print x

	merging_cluster_index = -10000000

	for patch in island:
		patch_centroid = calculateCentroid(patch, coordinates, realId_list)

		minimum_distance = 100000000000

		# print "PATCH CENTROID"
		# print patch_centroid


		for key, value in cluster_centroid_dict.iteritems():
			
			# if min(patch)-1 == max(k_means[key]) or max(patch) + 1 == min(k_means[key]):
			if len(patch) < patch_size:
				if min(patch) - 1 in k_means[key] or max(patch) + 1 in k_means[key]:
					# print "VAlid key", key


					distance_with_cluster  =  dist(value, patch_centroid)

					# print "distance with cluster", distance_with_cluster
			# print "Distance with cluster ", key, value, "IS ",distance_with_cluster

					if  distance_with_cluster < minimum_distance:
						merging_cluster_index = key
						minimum_distance = distance_with_cluster

			else:
				# print "patch is ", patch

				distance_with_cluster  =  dist(value, patch_centroid)
				# print "Distance with cluster ", key, value, "IS ",distance_with_cluster

				if  distance_with_cluster < minimum_distance:
					merging_cluster_index = key
					minimum_distance = distance_with_cluster

				


		k_means[merging_cluster_index] = sorted(k_means[merging_cluster_index] + patch)


	# print "FINALLLY"

	# for key, value in k_means.iteritems():
	# 	print key, value
	# 	print
	# 	print

	return k_means


def sequenceStitch(k_means, island):
	# print "Printing the K-means sequence stitch received"

	# for key,value in k_means.iteritems():
	# 	print key, value
	# 	print

	for key, value in k_means.iteritems():
		if len(value)==0:
			k_means[key] = island[0]
			island.remove(island[0])
	# 	print key, value
	# 	print
	# 	print

	# print
	# print

	# print k_means
	minimum = 100000000

	maximum = -10000000

	remaining_island = []

	for key, values in k_means.iteritems():
		if minimum > min(values):
			minimum = min(values)

		if maximum < max(values):
			maximum = max(values)

	# print "min and max is ", minimum, maximum
	for patch in island:
		# low = patch[0]
		# high = patch[-1] + 1
		flag = 0
		for key, value in k_means.iteritems():
			# print "PATCH"
			# print patch

			# print

			# print "Domain"
			# print value

			# print 
			if max(patch) == minimum - 1 and min(value)==minimum:
				flag = 1
				k_means[key] = sorted(list(k_means[key] + patch))
				# print "Start"
				# island.remove(patch)
				break

			elif min(patch) == maximum + 1 and max(value)==maximum:
				flag = 1
				k_means[key] = sorted(list(k_means[key] + patch))
				# print "End"
				# island.remove(patch)
				break

			elif min(patch) - 1 in value and max(patch) + 1 in value:
				flag = 1
				k_means[key] = sorted(list(k_means[key] + patch))
				# print "Between"
				# island.remove(patch)
				break

		if flag==0:
			remaining_island.append(patch)

			# if low < minimum:
			# 	if high in value:
			# 		k_means[key] = sorted(list(set(k_means[key]  + patches)))

			# if low in value and high in value:
			# 	k_means[key] = sorted(list(set(k_means[key]  + patches)))

			# if low in value and high not in value:
			# 	k_means[key] = sorted(list(set(k_means[key]  + patches)))

	return k_means, remaining_island

def isContiguous(cath_boundaries, domains):
	# print cath_boundaries
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
			if numOFSegments > 1:
				return False
			dom = cath_boundaries[x:x+6*numOFSegments+1]
			cathDict[key] = dom
			key+=1
			x+=6*numOFSegments+1
	return True

def internalStitch(island, patch_length):
	remove = []
	final = []
	x = 0
	while x < len(island):
		flag = 0
		# print "x is ", x
		# print "First patch is ", island[x]
		high = island[x][-1] + 1
		low = island[x][0] - 1

		for y in range(0, len(island)):
			if island[y]==island[x]:
				continue
			if high in island[y] or low in island[y]:
				# print "merged with ", island[y]
				island[x] = sorted(island[x] + island[y])
				island.remove(island[y])
				# print "now x is ", x
				flag = 1
				break

		if flag==0:
			x+=1
		# print "Reuslting island is ", island

	return sorted(island)
	# for patch in island:
	# 	high = patch[-1] + 1
	# 	low = patch[0] - 1

	# 	for patch2 in island:
	# 		if patch==patch2:
	# 			continue

	# 		else:
	# 			if high in patch2 or low in patch2:
	# 				final = sorted(patch + patch2)
	# 				remove.append(patch)

	# # for x in range(len(island)-1):
	# # 	island.sort(key=itemgetter(0))
	# # 	high = max(island[x])+1

	# # 	if high==island[x+1][0]:# and (len(island[x]) + len(island[x+1]) <= patch_length):
	# # 		remove.append(x)
	# # 		island[x+1] = sorted(island[x] + island[x+1])

	# final = []
	# for x in range(len(island)):
	# 	if x not in remove:
	# 		final.append(island[x])

	# return final

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
# path = "../Output Data/500_proteins/Non Contiguous/"
# path = "temp2/"
path = "Second Dataset/"
file_counter = 0
correct = 0
accuracy = 0.0

def printCATHDomains(cath_boundaries,domains):
	cath_dict = {}
	domain_counter = 1
	
	cath_boundaries = cath_boundaries.split(" ")
	cath_boundaries = filter(None, cath_boundaries)

	# print cath_boundaries
	print "\"",
	initial_position = 0
	while domain_counter <= domains:
		print "Domain", domain_counter, ":",
		value = ""
		num_of_segments = int(cath_boundaries[initial_position])

		for y in range(1, num_of_segments+1):
			print cath_boundaries[initial_position + 2],
			print "-",
			print cath_boundaries[initial_position + 5],

			# value+=cath_boundaries[initial_position + 2] + "-" + cath_boundaries[initial_position + 5] + " "
			# print ,
			# print ,
			# print ,"  ",
			initial_position+=6
		initial_position+=1

		cath_dict[domain_counter] = value.strip()

		# print traverser
		if domain_counter!=domains:
			print
			print
		domain_counter+=1


	# for key,value in cath_dict.iteritems():
	# 	print key, value


	# domain_counter = 1
	# print "\"",
	# for key in sorted(cath_dict, key=cath_dict.get, reverse=True):
	# 	value = cath_dict[key]
	# 	print "Domain", domain_counter,": ",
	# 	print value,
	# 	# makeReadable(sorted(value))
	# 	if domain_counter!=domains:
	# 		print
	# 		print
	# 	domain_counter+=1
	# # print ", " + "{0:.2f}".format(overlap)
	# print "\",",

	print "\",",
		# for x in range(len(cath_boundaries)):

# intersection_file = "../Output Data/cath_scop_intersection/cath_scop_intersection.txt"

input_file = "Second Dataset Chains/two_domains"
with open(input_file) as f23:
	intersection_data = f23.readlines()

# not_list = ['3g4s', '1adh', '1baa', '1a4k', '1abk','2w8p', '1tj7', '1z5h', '1p9h', '1dve', '1aon', '1fjg', '1jfw', '1nkq', '1byr', '1abz','1t6t','1c21', '1a18', '1bal', '1am4', '1vea', '1foe', '1t11', '1hci', '3ci0', '1d0g', '1olz', '1bs2','3bzc','1c4a','2oce', '1m2o', '1g3p','1dkg','1f0i','1aye','3bzk', '1cjd', '1xi8']
# not_list = ["3doa", "1d4v", "3lie", "2hyv"];

# not_list = ["1aye"]

visited_list = []

# print "No., PDB, Domains, CATH, K-Means, Accuracy"
print "No., PDB, Chain, Domains, CATH, K-Means"

for pdb_file in os.listdir(path):

	# if file_counter>=100:
	# 	break

	pdb_path = pdb_file
	pdb_file = pdb_file.split(".")[0].lower()

	flag = 0


	var = open('../Input Files/CathDomall', 'r')


	while 1:

		pdb_id = var.readline()

		if not pdb_id:
			break

		else:

			if pdb_id[:4].lower()==pdb_file[:4].lower() and pdb_file[:4].lower():#in not_list:#and pdb_file not in visited_list:
				flag = 1

				var_1 = open(path+pdb_path, 'r')

				chain = pdb_id[18]
				frags = int(pdb_id[11] + pdb_id[12])
				
				domains = int(pdb_id[7] + pdb_id[8])

				for x in intersection_data:
					x = x.split(" ")[0].strip()
					if x==pdb_file[:4].lower() + chain.lower():

						domain_boundary = pdb_id[14:].strip()
						if frags==0 and domains == 2 and isContiguous(domain_boundary, domains):
							
							# visited_list.append(pdb_id[:4].lower())

							print str(file_counter + 1) + "," + pdb_id[:4] + ", " + chain + ", "+ str(domains)+ ", ", #\" ",# + domain_boundary, "," ,

							printCATHDomains(domain_boundary, domains)

							cords_list, realId_list = getCordsList(var_1,chain)

							x = np.asarray(cords_list)
							file_counter+=1

							km = KMeans(n_clusters=domains).fit(x)

							labels_km = km.labels_
							clusters_km = km.cluster_centers_

							boundaries = domainBoundaries(labels_km, realId_list,domains)

							# print boundaries

							boundaries = fillVoids(boundaries)

							# print "Boundaries after fillings voids"
							# print boundaries

							for key,value in boundaries.iteritems():
								boundaries[key] = list(set(value))


							# print "Boundaries after removing duplicates"
							# for key, value in boundaries.iteritems():
							# 	print key, value
							# 	print


							# print "STICTHCADFA"
							boundaries = stitchPatches(boundaries, clusters_km, cords_list, realId_list, patch_size)

							# print "CHIGA CHIGA"
							# print boundaries

							cathDict = getCathDict(domain_boundary, domains)

							# cathDict, boundaries = mapCorrectly(cathDict, boundaries)

							# print "MAPPED CORRECTLY"

							# print boundaries

							# print boundaries

							# overlap = compareResults(cathDict, boundaries, domains)

							# accuracy = accuracy + overlap

							for key,value in boundaries.iteritems():
								boundaries[key] = list(set(value))


							domain_counter = 1
							print "\"",
							# for key, value in boundaries.iteritems():
							for key in sorted(boundaries, key=boundaries.get):
								value = boundaries[key]
								print "Domain", domain_counter,": ",
								makeReadable(sorted(value))
								if domain_counter!=domains:
									print
									print
								domain_counter+=1
							# print ", " + "{0:.2f}".format(overlap)
							print "\""

# print "accuracy is", accuracy/file_counter