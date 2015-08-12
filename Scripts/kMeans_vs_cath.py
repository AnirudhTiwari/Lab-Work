import os
import math
from igraph import *
from sklearn.cluster import *
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import re

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
			val = value_finder(23, data)
		
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


path = "../Output Data/Two Domain Proteins/"
counter = 0
correct = 0

for pdb_file in os.listdir(path):

	if counter==100:
		break

	pdb_path = pdb_file
	pdb_file = pdb_file.split(".")[0].lower()

	flag = 0


	var = open('../Input Files/CathDomall', 'r')

	while 1:

		# print "path", path+pdb_path		

		pdb_id = var.readline()

		if not pdb_id:
			break

		else:

			if pdb_id[:4].lower()==pdb_file[:4].lower() and pdb_file!="1aak" and pdb_file!="1fnr" and pdb_file!="1ace" and pdb_file!="1adh":
				flag = 1

				var_1 = open(path+pdb_path, 'r')

				chain = pdb_id[18]

				domains = int(pdb_id[7] + pdb_id[8])

				frags = int(pdb_id[11] + pdb_id[12])



				if domains==2 and frags==0:
					domain_boundary = pdb_id[14:].strip()

					print str(counter + 1) + "," + pdb_id[:4] + ", " + str(domains) + ", " + domain_boundary, "," ,


					cords_list, realId_list = getCordsList(var_1,chain)

					# print "====================================="+pdb_id[:4]+"==============================="


					# print "Domains: " + str(domains)

					# print domain_boundary

					x = np.asarray(cords_list)
					counter+=1

					# print "==============K-Means================"

					
					km = KMeans(n_clusters=domains).fit(x)

					labels_km = km.labels_

					# print len(labels_km)

					boundaries = domainBoundaries(labels_km, realId_list,domains)
					for key, value in boundaries.iteritems():
						makeReadable(value)
					print
