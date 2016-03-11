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
max_rg = 45
max_length = 610
max_energy = 0.15

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
						# if distance < 7.0:
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

# path = "../Output Data/Two Domain Proteins/"

file_counter = 0
correct = 0
accuracy = 0.0
length_list_a = []
interactionEnergy_list_a = []
length_list_b = []
interactionEnergy_list_b = []
visited_list = []

gyration_list_a = []
gyration_list_b = []

a = int(raw_input("No. of domains(lesser) for protein A: "))
b = int(raw_input("No. of domains(higher) for protein B: "))
c = raw_input("Contiguous(C)/Non-Contiguous(N)/Both(B): ")

# if c=='C':
# 	path = "../Output Data/500_proteins/Contiguous/"

# if c=='N':
# 	path = "../Output Data/500_proteins/Non Contiguous/"

path = "temp2/"
# path = "../Output Data/500_proteins/Both/"



# print a, b, c

# print "No., PDB, Domains, CATH, Interaction Energy for 1 Domain, Interaction Energy for 2 Domains, Interaction Energy for 3 Domains, Interaction Energy for 4 Domains, Interaction Energy for 5 Domain, Interaction Energy for 6 Domain"

with open("../Output Data/cath_scop_intersection/cath_scop_intersection.txt") as f12:
	req_chains = f12.readlines()


for pdb_file in os.listdir(path):

	pdb_path = pdb_file
	pdb_file = pdb_file.split(".")[0].lower()

	flag = 0


	var = open('../Input Files/CathDomall', 'r')
	not_list = ['3g4s', '1adh', '1baa', '1a4k', '1abk','2w8p', '1tj7', '1z5h', '1p9h', '1dve', '1aon', '1fjg', '1jfw', '1nkq', '1byr', '1abz','1t6t','1c21', '1a18', '1bal', '1am4', '1vea', '1foe', '1t11']


	while 1:

		pdb_id = var.readline()

		if not pdb_id:
			break

		else:

			if pdb_id[:4].lower()==pdb_file[:4].lower()  and pdb_file not in not_list and pdb_id[:4] not in visited_list:

				flag = 1
				var_1 = open(path+pdb_path, 'r')
				frags = int(pdb_id[11] + pdb_id[12])
				var_2 = open(path+pdb_path, 'r')
				chain = pdb_id[18]
				domains = int(pdb_id[7] + pdb_id[8])

				for x in req_chains:
					if x[:4]==pdb_id[:4].lower() and chain.lower()==x[4].lower():					
						if frags==0 and domains==a and pdb_id[:4]:
							print pdb_id.strip()
							domain_boundary = pdb_id[14:].strip()

							visited_list.append(pdb_id[:4])

							cords_list, realId_list = getCordsList(var_1,chain)

							x = np.asarray(cords_list)

							file_counter+=1

							simulated_domains = 1

							while(simulated_domains!=b+1):

								km = KMeans(n_clusters=simulated_domains).fit(x)
								labels_km = km.labels_

								if simulated_domains==b:
									length_list_a.append(len(cords_list))
									try:
										gyration_list_a.append(radius_of_gyration.radius_of_gyration(var_2, chain))
									except:
										print "Error hai isme ", pdb_id
									interaction_energy = getInteractionEnergy(labels_km, simulated_domains, cords_list)
									interactionEnergy_list_a.append(interaction_energy)
								simulated_domains+=1


						if frags==0 and domains==b and pdb_id[:4]:
							domain_boundary = pdb_id[14:].strip()

							val, segmented = getCathDict(domain_boundary, domains)
							
							visited_list.append(pdb_id[:4])


							if segmented==True and c=='C':
								continue

							if segmented==False and c=='N':
								continue


							cords_list, realId_list = getCordsList(var_1,chain)

							x = np.asarray(cords_list)

							simulated_domains = 1

							while(simulated_domains!=b+1):

								km = KMeans(n_clusters=simulated_domains).fit(x)
								labels_km = km.labels_

								if simulated_domains==b:
									length_list_b.append(len(cords_list))
									try:
										gyration_list_b.append(radius_of_gyration.radius_of_gyration(var_2, chain))
									except:
										print "Error hai isme ", pdb_id
									interactionEnergy_list_b.append(getInteractionEnergy(labels_km, simulated_domains, cords_list))

								simulated_domains+=1	


domain_string_a=""

if(a==1):
	domain_string_a="single"

if(a==2):
	domain_string_a="two"

if(a==3):
	domain_string_a="three"

if(a==4):
	domain_string_a="four"

if(a==5):
	domain_string_a="five"


length_a = domain_string_a + "_domain_length"
rg_a = domain_string_a + "_domain_rg"
interaction_energy_a  = domain_string_a + "_domain_interaction_energy"

domain_string_b=""

if(b==2):
	domain_string_b="two"
if(b==3):
	domain_string_b="three"

if(b==4):
	domain_string_b="four"

if(b==5):
	domain_string_b="five"


length_b_non_contiguous = domain_string_b + "_domain_length_non_contiguous"
rg_b_non_contiguous = domain_string_b + "_domain_rg_non_contiguous"
interaction_energy_b_non_contiguous =  domain_string_b + "_domain_interaction_energy_non_contiguous"

length_b_contiguous = domain_string_b + "_domain_length_contiguous"
rg_b_contiguous = domain_string_b + "_domain_rg_contiguous"
interaction_energy_b_contiguous = domain_string_b + "_domain_interaction_energy_contiguous"


fp1 = open(length_a, 'wb')
pickle.dump(length_list_a, fp1)
fp1.close()

fp2 = open(rg_a, 'wb')
pickle.dump(gyration_list_a, fp2)
fp2.close()

fp3 = open(interaction_energy_a, 'wb')
pickle.dump(interactionEnergy_list_a, fp3)
fp3.close()

if c=='C':
	fp4 = open(length_b_contiguous, 'wb')
	pickle.dump(length_list_b, fp4)
	fp4.close()

	fp5 = open(rg_b_contiguous, 'wb')
	pickle.dump(gyration_list_b, fp5)
	fp5.close()

	fp6 = open(interaction_energy_b_contiguous, 'wb')
	pickle.dump(interactionEnergy_list_b, fp6)
	fp6.close()

if c=='N':
	fp4 = open(length_b_non_contiguous, 'wb')
	pickle.dump(length_list_b, fp4)
	fp4.close()

	fp5 = open(rg_b_non_contiguous, 'wb')
	pickle.dump(gyration_list_b, fp5)
	fp5.close()

	fp6 = open(interaction_energy_b_non_contiguous, 'wb')
	pickle.dump(interactionEnergy_list_b, fp6)
	fp6.close()



# print "Single Domain Proteins"
print len(gyration_list_a)
print len(interactionEnergy_list_a)
print len(length_list_a)


# print "Multi Domain Proteins"
print len(gyration_list_b)
print len(interactionEnergy_list_b)
print len(length_list_b)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# # ax1 = fig.add_subplot(111, projection='3d')


# # ax.scatter(gyration_list_a, length_list_a, interactionEnergy_list_a, c='r')
# ax.scatter(gyration_list_b, length_list_b, interactionEnergy_list_b, c='b')

# ax.set_xlabel('Radius Of Gyration')
# ax.set_ylabel('Length')
# ax.set_zlabel('Interaction Energy')

# plt.show()


# plt.plot(length_list_a, interactionEnergy_list_a,'ro')
# plt.plot(length_list_b, interactionEnergy_list_b, 'bo')
# # plt.plot(length_list_b, y_line)

# # plt.plot(gyration_list_a, interactionEnergy_list_a,'ro')
# # plt.plot(gyration_list_b, interactionEnergy_list_b, 'bo')

# plt.xlabel('Length')
# # plt.xlabel('Radius Of Gyration')



# plt.ylabel('Interaction Energy')

# plt.show()


