'''Script to find cluster density and radius of gyration for chains in my constructed database 
and to generate .csv files for plotting graphs for length vs radius and length vs cluster density.
Also to calculate interaction energy for single vs multi domain proteins'''

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
import radius_of_gyration
from mpl_toolkits.mplot3d import Axes3D
import pickle

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
	total_interaction = 0

	for y in clusters_dict:
		for z in clusters_dict:
			if y!=z:
				for a in clusters_dict[y]:
					for b in clusters_dict[z]:
						total_interaction+=1
						distance = dist(cords_list[a],cords_list[b])
						# print cords_list[a], cords_list[b]
						if distance < 7.0:
							energy+=1
							# energy = energy + 1/distance

	return (1.0*energy/2)/len(matrix)
	# return (1.0*energy)/(total_interaction)

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
			if numOFSegments>1:
				return cathDict, True
			dom = cath_boundaries[x:x+6*numOFSegments+1]
			dom = makeList(dom)
			cathDict[key] = dom
			key+=1
			x+=6*numOFSegments+1
	return cathDict, False

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

def calculateDensity(coordinates):
	
	centroid_x=0
	centroid_y=0
	centroid_z=0

	for x in coordinates:
		centroid_x=x[0]+centroid_x
		centroid_y=x[1]+centroid_y
		centroid_z=x[2]+centroid_z

	centroid_x = 1.0*centroid_x/len(coordinates)
	centroid_y = 1.0*centroid_y/len(coordinates)
	centroid_z = 1.0*centroid_z/len(coordinates)

	centroid = [centroid_x, centroid_y, centroid_z]		

	radius = 0.0

	for a in coordinates:
		radius = radius + dist(a, centroid)	

	radius = radius/len(coordinates)

	density = 1.0*len(coordinates)/(radius*radius*radius)
	return density
	# return radius

file_counter = 0
correct = 0
accuracy = 0.0

length_list_a = []
interactionEnergy_list_a = []
density_list_a = []


length_list_b = []
interactionEnergy_list_b = []
density_list_b = []

visited_list = []
gyration_list_a = []
gyration_list_b = []


# path = "temp2/"
path = "Second Dataset/"

# with open("../Output Data/cath_scop_intersection/cath_scop_intersection.txt") as f12:
with open("Second Dataset Chains/multi_domain") as f12:
# with open("test_input") as f12:
	req_chains = f12.readlines()

for pdb_file in os.listdir(path):

	pdb_path = pdb_file
	pdb_file = pdb_file.split(".")[0].lower()

	flag = 0


	var = open('../Input Files/CathDomall', 'r')
	# not_list = ['3g4s', '1adh', '1baa', '1a4k', '1abk','2w8p', '1tj7', '1z5h', '1p9h', '1dve', '1aon', '1fjg', '1jfw', '1nkq', '1byr', '1abz','1t6t','1c21', '1a18', '1bal', '1am4', '1vea', '1foe', '1t11', '1hci']
	not_list = [] 

	while 1:

		pdb_id = var.readline()

		if not pdb_id:
			break

		else:

			if pdb_id[:4].lower()==pdb_file[:4].lower(): #and pdb_file not in not_list: #and pdb_file not in visited_list:

				flag = 1
				var_1 = open(path+pdb_path, 'r')
				frags = int(pdb_id[11] + pdb_id[12])
				var_2 = open(path+pdb_path, 'r')
				chain = pdb_id[18]
				domains = int(pdb_id[7] + pdb_id[8])

				for r in req_chains:
					# print pdb_id[:4].lower()
					if r[:4]==pdb_id[:4].lower() and chain.lower()==r[4].lower():					
						if frags==0:
							# print pdb_id.strip()
							visited_list.append(pdb_file)
							domain_boundary = pdb_id[14:].strip()

							cords_list, realId_list = getCordsList(var_1,chain)

							x = np.asarray(cords_list)

							file_counter+=1

							try:
								radius_gy = radius_of_gyration.radius_of_gyration(var_2, chain)
							except Exception, e:
									print "Error hai isme ", pdb_id, e
							length = len(cords_list)

							density = calculateDensity(cords_list)
#								
							# radius_vish = calculateDensity(cords_list)

							simulated_domains = 3

							km = KMeans(n_clusters=simulated_domains).fit(x)
							labels_km = km.labels_
								
							interaction_energy = getInteractionEnergy(labels_km, simulated_domains, cords_list)
							# interaction_energy_count = getInteractionEnergy(labels_km, simulated_domains, cords_list)

							if domains!=1:
								length_list_a.append(length)
								interactionEnergy_list_a.append(interaction_energy)
								density_list_a.append(density)
								print pdb_id[:4], ",", chain, "," ,domains, "," ,length, ", ", '{0:.3f}'.format(interaction_energy),", ", '{0:.3f}'.format(density),", ", '{0:.3f}'.format(radius_gy)  
								# print pdb_id[:4], ",", chain, "," ,domains, "," ,length, ", ", interaction_energy,", ", density,", ", '{0:.3f}'.format(radius_gy)  
			


