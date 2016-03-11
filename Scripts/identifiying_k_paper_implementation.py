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


def dist(a,b):
	for x in range(3):
		distance = math.pow((math.pow((a[0]-b[0]),2) + math.pow((a[1]-b[1]),2) + math.pow((a[2]-b[2]),2)), 0.5)
		return distance


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
			if numOFSegments>1:
				return cathDict, True
			dom = cath_boundaries[x:x+6*numOFSegments+1]
			dom = makeList(dom)
			cathDict[key] = dom
			key+=1
			x+=6*numOFSegments+1
	return cathDict, False

def calculateDistortion(centers, matrix, cluster_num, cords_list):
	clusters_dict = defaultdict(list)

	for x in range(len(matrix)):
		clusters_dict[matrix[x]].append(x)

	distortion = 0.0

	for cord in clusters_dict[cluster_num]:
		a = dist(centers[cluster_num], cords_list[cord])
		a = a*a
		distortion = distortion + a

	return distortion

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


with open("energy_single_radius_7.csv") as f1:
	single = f1.readlines()

with open("energy_multi_radius_7.csv") as f2:
	multi = f2.readlines()

chains_attributes = {}

for x in single:
	x = x.split(",")
	chains_attributes[x[0].strip() + str(x[1].strip().lower())] = [int(x[3]), float(x[4])]

for x in multi:
	x = x.split(",")
	chains_attributes[x[0].strip() + str(x[1].strip().lower())] = [int(x[3]), float(x[4])]


# print chains_attributes
path = "temp2/"

print "PDB, Chain, CATH, Length, Interaction Energy, Min. F(k), Single/Multi, Suggested K, FINAL" 

with open("../Output Data/cath_scop_intersection/cath_scop_intersection.txt") as f12:
	req_chains = f12.readlines()

histogram_list = []

for pdb_file in os.listdir(path):

	pdb_path = pdb_file
	pdb_file = pdb_file.split(".")[0].lower()

	flag = 0


	var = open('../Input Files/CathDomall', 'r')
	not_list = ['3g4s', '1adh', '1baa', '1a4k', '1abk','2w8p', '1tj7', '1z5h', '1p9h', '1dve', '1aon', '1fjg', '1jfw', '1nkq', '1byr', '1abz','1t6t','1c21', '1a18', '1bal', '1am4', '1vea', '1foe', '1t11', '1hci', '3ci0']


	while 1:

		pdb_id = var.readline()

		if not pdb_id:
			break

		else:

			if pdb_id[:4].lower()==pdb_file[:4].lower()  and pdb_file not in not_list and pdb_file not in visited_list and int(pdb_id[7] + pdb_id[8])==2:

				flag = 1
				var_1 = open(path+pdb_path, 'r')
				frags = int(pdb_id[11] + pdb_id[12])
				var_2 = open(path+pdb_path, 'r')
				chain = pdb_id[18]
				domains = int(pdb_id[7] + pdb_id[8])

				for r in req_chains:
					if r[:4]==pdb_id[:4].lower() and chain.lower()==r[4].lower():					
						if frags==0:
							visited_list.append(pdb_file)
							domain_boundary = pdb_id[14:].strip()

							cords_list, realId_list = getCordsList(var_1,chain)

							x = np.asarray(cords_list)

							file_counter+=1

							simulated_domains = 1

							try:
								radius = radius_of_gyration.radius_of_gyration(var_2, chain)
							except:
									print "Error hai isme ", pdb_id
							length = len(cords_list)
							val, segmented = getCathDict(domain_boundary, domains)

							F_values = []
							k_values = []
							S_values = {}
							alpha_values = {}
							i = 1

							print pdb_id[:4] + ", " + chain +  ", " + str(domains) + ", " + str(length),
							while simulated_domains!=7:
								km = KMeans(n_clusters=simulated_domains).fit(x)
								labels_km = km.labels_
								centers_km = km.cluster_centers_

								F = 0.0

								S = 0.0
								

								for s in range(0,simulated_domains,1):
									S = S + calculateDistortion(centers_km, labels_km, s, cords_list)

								S_values[i]=S		
								simulated_domains+=1

								i+=1

							for k in range(2, 7):
								if k==2:
									alpha_values[k]=0.75

								else:
									alpha_values[k]=alpha_values[k-1] + (1-alpha_values[k-1])/6	

							for k in range(1, 7):
								if k==1:
									F_values.append(1)

								else:
									F_values.append((S_values[k]/(alpha_values[k]*S_values[k-1]*1.0)))
							

							# print "Alpha Values ", alpha_values		
							# print "S Values ", S_values
							# print "F values", F_values

							k_values=[]

							for k in range(1, 7):
								k_values.append(k)



							found_k = F_values.index(min(F_values)) + 1

							if found_k==2 and min(F_values) < 0.75:
								found_k = 2

							if found_k==2 and min(F_values) > 0.75:
								found_k = 1


							# print "Actual No. of Domains ", domains, " Suggested Number of domains ", found_k, " F value ", min(F_values)

							if (pdb_id[:4].lower() + chain.lower()) in chains_attributes:
								print ", " + str(chains_attributes[pdb_id[:4].lower() + chain.lower()][1]) + ", " + str('{0:.3f}'.format(min(F_values))).strip(),

								if chains_attributes[pdb_id[:4].lower() + chain.lower()][0] >= 165 and chains_attributes[pdb_id[:4].lower() + chain.lower()][1] <= 0.2:
									print ", " + "Multi", 

								else:
									print ", " + "Single", 
									

								print ", " + str(found_k) + ", "

								# if domains==1:
								# 	histogram_list.append(100*F_values[1])


								plt.plot(k_values,F_values)
								file_name = pdb_id[:4].lower() + chain.lower() + "_2.png"
								plt.savefig(file_name)
								plt.close()
							# plt.show()

# plt.hist(histogram_list)
# plt.show()

				# 	break
				# break








						

