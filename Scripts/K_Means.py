# This file takes as an input chain+pdb in lowercase and outputs the result of k-means after reading k from CATH.
# The output is in a .csv format fine tuned to be human readable when imported as an excel sheet. Also, it evaluates the
# cluster output and deems is to be correct if more than 75% of the residues are correctly assigned to the correct cluster as per CATH. 

from sklearn.cluster import *
import numpy as np
import common_functions as utils
import re
from compiler.ast import flatten
import itertools

#Following are the Methods used within the program
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

			val = utils.value_finder(22, 26, data)	
						
			coord_x = float(utils.value_finder(30, 38, data))

			coord_y = float(utils.value_finder(38, 46, data))

			coord_z = float(utils.value_finder(46, 54, data))

		
			if not re.search('[a-zA-Z]+', val):
				real_id = int(val)

				coordinates = [coord_x,coord_y,coord_z]

				cords_list.append(coordinates)
				realId_list.append(real_id)

	return cords_list,realId_list

def getDomainBoundaries(matrix, realId_list, domains):
	new_dict = {}
	for y in range(len(matrix)):
		if matrix[y] in new_dict:
			new_dict[matrix[y]].append(realId_list[y])
		else:
			new_dict[matrix[y]] = [realId_list[y]]

	return new_dict

def TooManyMissingResidues(boundaries):
	counter = 0
	artificially_added = []
	for key, value in boundaries.iteritems():
		for x in range(min(value), max(value)+1):
			if x not in value:
				if x not in flatten(boundaries.values()):
					counter+=1
					artificially_added.append(x)

	if len(artificially_added) > 25:
		print len(artificially_added)
		return True
		
	return False

def fillVoids(boundaries):
	for key, value in boundaries.iteritems():
		for x in range(min(value), max(value)+1):
			if x not in value:
				if x not in flatten(boundaries.values()):
					value.append(x)
		boundaries[key] = sorted(value)
	return boundaries

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

def internalStitch(island, patch_length):
	remove = []
	final = []
	x = 0
	while x < len(island):
		flag = 0

		high = island[x][-1] + 1
		low = island[x][0] - 1

		for y in range(0, len(island)):
			if island[y]==island[x]:
				continue
			if high in island[y] or low in island[y]:
				island[x] = sorted(island[x] + island[y])
				island.remove(island[y])
				flag = 1
				break

		if flag==0:
			x+=1

	return sorted(island)

def sequenceStitch(k_means, island):
	
	for key, value in k_means.iteritems():
		if len(value)==0:
			k_means[key] = island[0]
			island.remove(island[0])

	minimum = 100000000

	maximum = -10000000

	remaining_island = []

	for key, values in k_means.iteritems():
		if minimum > min(values):
			minimum = min(values)

		if maximum < max(values):
			maximum = max(values)

	for patch in island:
		flag = 0
		for key, value in k_means.iteritems():
			if max(patch) == minimum - 1 and min(value)==minimum:
				flag = 1
				k_means[key] = sorted(list(k_means[key] + patch))
				break

			elif min(patch) == maximum + 1 and max(value)==maximum:
				flag = 1
				k_means[key] = sorted(list(k_means[key] + patch))
				break

			elif min(patch) - 1 in value and max(patch) + 1 in value:
				flag = 1
				k_means[key] = sorted(list(k_means[key] + patch))
				break

		if flag==0:
			remaining_island.append(patch)
	return k_means, remaining_island

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
	cluster_centroid_dict = {};

	for key, value in k_means.iteritems():
		cluster_centroid = calculateCentroid(value, coordinates, realId_list)
		cluster_centroid_dict[key] = cluster_centroid

	merging_cluster_index = -10000000

	for patch in island:
		patch_centroid = calculateCentroid(patch, coordinates, realId_list)

		minimum_distance = 100000000000

		for key, value in cluster_centroid_dict.iteritems():
			if len(patch) < patch_size:
				if min(patch) - 1 in k_means[key] or max(patch) + 1 in k_means[key]:
					distance_with_cluster  =  utils.dist(value, patch_centroid)
					if  distance_with_cluster < minimum_distance:
						merging_cluster_index = key
						minimum_distance = distance_with_cluster

			else:
				distance_with_cluster  =  utils.dist(value, patch_centroid)
				if  distance_with_cluster < minimum_distance:
					merging_cluster_index = key
					minimum_distance = distance_with_cluster

		k_means[merging_cluster_index] = sorted(k_means[merging_cluster_index] + patch)

	return k_means

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

		island = checkLastTwoResidues(value, island)

	island = internalStitch(sorted(island), patch_length)

	mean_list = []
	for key, value in k_means.iteritems():
		for patches in island:
			for x in patches:
				if x in value:
					value.remove(x)

	k_means, island = sequenceStitch(k_means, island)

	if len(island)!=0:
		k_means = centroidStitch(k_means, island, coordinates, realId_list)
 		
	return k_means

def makeList(domain):
	domainList = []
	segments = domain[0]
	chain = domain[1]
	insert_character = domain[3]
	copy_domain = domain
	domain = list(filter(lambda x: x!=chain and x!=insert_character, domain[1:]))

	if chain==copy_domain[2]:
		domain = [copy_domain[2]] + domain

	for x in xrange(0,len(domain)-1,2):
		temp_list = []
		lower_bound = int(domain[x])
		upper_bound = int(domain[x+1])

		for y in range(lower_bound, upper_bound+1):
			temp_list.append(y)
		domainList.append(temp_list)

	return flatten(domainList)

def getCathBoundaries(cath_boundaries, domains):
	cath_boundaries = cath_boundaries.split(" ")
	cath_boundaries = filter(None, cath_boundaries)
	cathDict = {}
	key = 0
	numOFSegments = 1
	x = 0
	counter=0
	while 1:
		# print cath_boundaries
		if x >= len(cath_boundaries):
			break
		else:
			if counter==domains:
				break
			numOFSegments = int(cath_boundaries[x])

			dom = cath_boundaries[x:x+6*numOFSegments+1]

			dom = makeList(dom)
			cathDict[key] = dom
			key+=1
			x+=6*numOFSegments+1
			counter+=1
	return cathDict

def matchDicts(cath, k_means):
	perm_base_list = []

	for key, value in k_means.iteritems():
		perm_base_list.append(key)

	final_list = perm_base_list
	max_overlap = -1000

	permutations_list = list(itertools.permutations(perm_base_list))

	#Now for every permutation of k_means, compute overlap and compare

	for permutation in permutations_list:
		overlap = 0
		perm_iter = 0

		for key,value in cath.iteritems():
			set_a = set(value)
			set_b = set(k_means[permutation[perm_iter]])
			overlap+=len(set_a.intersection(set_b))
			perm_iter+=1

		if overlap > max_overlap:
			max_overlap = overlap
			final_list = list(permutation)

	final_kmeans_dict = {}
	domain_counter = 1
	for key in final_list:
		final_kmeans_dict[domain_counter] = k_means[key]
		domain_counter+=1

	return final_kmeans_dict

def makeReadable(boundaries):
	temp_list = []
	flag = 0

	for x in range(0,len(boundaries)-1):
		if boundaries[x+1] - boundaries[x]==1:
			temp_list.append(boundaries[x])

		else:
			if len(temp_list)!=0:
				temp_list.append(boundaries[x])
				print min(temp_list), "-", max(temp_list), "  ",
				temp_list = []

	if flag==0 and len(temp_list)!=0:
		print  min(temp_list), "-", max(temp_list)+1,

def printDicts(dictionary):
	domain_counter = 1
	print "\"",
	domains=len(dictionary)
	for key in sorted(dictionary, key=dictionary.get):
		value = dictionary[key]
		print "Domain", domain_counter,": ",
		makeReadable(sorted(value))
		if domain_counter!=domains:
			print
			print
		domain_counter+=1
	print "\"",

def printKMeansDict(k_means):
	print "\"",
	domain_counter = 1
	domains = len(k_means)
	for key,value in k_means.iteritems():
		print "Domain", key, ": ",
		makeReadable(sorted(value))
		if domain_counter!=domains:
			print
			print
		domain_counter+=1

	print "\"",

#Initialization etc

#For our own constructed dataset
# with open('multi_testing_dataset_post_phaseTwo.txt', 'r') as f:
# 	input_chains = f.readlines()

#For Benchmark 2
# with open('correct_Benchmark2_Dataset_PostPhaseTwo.txt', 'r') as f:
# 	input_chains = f.readlines()
	
#For Benchmark 3
with open('correct_Benchmark3_Dataset_PostPhaseTwo.txt', 'r') as f:
	input_chains = f.readlines()

with open('CathDomall', 'r') as f:
	cath_data = f.readlines()

# #For our own dataset
# path_to_pdb_files = 'Second Dataset/'

# #For Bennchmark2 dataset
# path_to_pdb_files = 'BenchmarkTwoDataset/'

#For Bennchmark3 dataset
path_to_pdb_files = 'BenchmarkThreeDataset/'

cath_dict = {} # A dictionary to hold cath pdb+chain and corresponding entry in CATH

for x in cath_data:
	if x[0]!='#':
		cath_dict[x[:5].lower()] = x

two_correct = 0
three_correct = 0
four_correct = 0

two_total = 0
three_total = 0
four_total = 0

total_correct = 0
counter = 0

missingPDB = []

#Main loop of the program which calculates the boundaries and outputs the final results.
for input_chain in input_chains:
	counter+=1
	
	pdb = input_chain[:4]
	chain = input_chain[4]
	

	cath_entry = cath_dict[pdb+chain]

	domains = int(cath_entry[7] + cath_entry[8])

	domain_boundary = cath_entry[14:].strip()

	print str(counter) + "," + pdb + ", " + chain.upper() + ", "+ str(domains)+ ", ",
	
	open_pdb = open(path_to_pdb_files+pdb+'.pdb','r') #Opening pdb file for k-means
	
	cords_list, realId_list = getCordsList(open_pdb, chain.upper())
	
	x = np.asarray(cords_list)

	km = KMeans(n_clusters=domains).fit(x)

	labels_km = km.labels_
	clusters_km = km.cluster_centers_

	boundaries = getDomainBoundaries(labels_km, realId_list, domains) #The clusters(boundaries) outputted by k-means

	#Removing duplicates. This happen when there are two set of coordinates of the same residue like 142 and 142A. I just pick the first one.
	for key,value in boundaries.iteritems():
		boundaries[key] = list(set(value))

	#There are missing residues in pdb files but are not always shown in CATH data. 
	#Thus, if there are less than 25 residues missing then I fill those missing residues based on the
	#cluster in which they can belong as per their sequence number. Else, the missing residues are reflected in the final answer.
	if not TooManyMissingResidues(boundaries):
		boundaries = fillVoids(boundaries)
	else:
		boundaries = fillVoids(boundaries) #Comment this out if you are not testing benchmark 2/3
		print "THIS PDB IS MISSED!!", pdb+chain
		missingPDB.append(pdb+chain)
		# continue

	patch_size = 20 #Defines the min length a segment of a non-contiguous domain can be. Any segment less than this should be merged to the contiguous part.
	
	#This method looks for scattered patches of residues which are present in the wrong cluster.
	#And based on the sequence as well as centroid distance, merges them in the right cluster.
	new_boundaries = stitchPatches(boundaries, clusters_km, cords_list, realId_list, patch_size)

	#Again removing duplicates post stitching patches.
	for key,value in new_boundaries.iteritems():
		new_boundaries[key] = list(set(value))

	#This a dictionary of the CATH domains and their correpsonding boundaries.
	cathBoundaries = getCathBoundaries(domain_boundary, domains)

	#Final boundaries of both CATH and K-Means which are sorted based on the values of residues, for example the first cluster should be from 1-80.
	#The second from 81-160 and not the other way round.
	sorted_cathBoundaries = {}
	sorted_kMeansBoundaries = {}

	domain_counter = 1

	for key in sorted(new_boundaries, key=new_boundaries.get):
		value = new_boundaries[key]
		sorted_kMeansBoundaries[domain_counter] = value
		domain_counter+=1

	domain_counter = 1

	for key in sorted(cathBoundaries, key=cathBoundaries.get):
		value = cathBoundaries[key]
		sorted_cathBoundaries[domain_counter] = value
		domain_counter+=1

	#Matching algorithm which maps the clusters of CATH and K-Means to figure out which cluster mapping would give the highest overlap
	sorted_kMeansBoundaries = matchDicts(sorted_cathBoundaries, sorted_kMeansBoundaries)

	#Calculating the final overlap score between CATH and K-Means Boundaries
	domain_counter = 1
	overlap = 0
	total_residues = 0
	while domain_counter<=domains:
		total_residues += len(sorted_kMeansBoundaries[domain_counter])
		overlap+=len(set(sorted_cathBoundaries[domain_counter]).intersection(sorted_kMeansBoundaries[domain_counter]))
		domain_counter+=1

	#Print CATH and K-Means boundaries in a human readable format for Excel.
	printDicts(cathBoundaries)
	print ", ",
	printKMeansDict(sorted_kMeansBoundaries)
	print ", ",
	print "{0:.2f}".format((1.0*overlap)/total_residues)

	if domains==2:
		two_total+=1
	
	elif domains==3:
		three_total+=1

	elif domains==4:
		four_total+=1


	if (1.0*overlap)/total_residues >= 0.75:
		if domains==2:
			two_correct+=1
		elif domains==3:
			three_correct+=1
		elif domains==4:
			four_correct+=1

		total_correct+=1

# Performance of the program
print "Two correct => ", two_correct, "Two total => ", two_total, "Two domain boundary prediction accuracy => ", '{0:.2f}'.format(two_correct*100.0/two_total)
print "Three correct => ", three_correct, "Three total => ", three_total, "Three domain boundary prediction accuracy => ", '{0:.2f}'.format(three_correct*100.0/three_total)
print "Four correct => ", four_correct, "Four total => ", four_total, "Four domain boundary prediction accuracy => ", '{0:.2f}'.format(four_correct*100.0/four_total)
print "Total correct => ", total_correct, "Total => ", counter, "Overall boundary prediction accuracy => ", '{0:.2f}'.format(total_correct*100.0/counter)

for x in missingPDB:
	print x
	


