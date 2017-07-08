# This is the main program which calculates the features which will be used to train the SVM.
# It takes as an input a list of chains in the format pdb+chain all in lower form in a file and 
# in turn returns a .csv file which has length, energy, density and radius of gyration of that chain
# along with other CATH data like the number of domains. This should be the final code that is to be 
# used in calculating the feature vectors.

from sklearn.cluster import *
import numpy as np
import radius_of_gyration
import common_functions as utils
import re
from collections import defaultdict

with open('multi_domain_balanced_classes_chains.txt', 'r') as f:
	input_chains = f.readlines()

with open('../Input Files/CathDomall', 'r') as f:
	cath_data = f.readlines()

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
path_to_pdb_files = 'trainingDataset_balanced/'
cath_dict = {} # A dictionary to hold cath pdb+chain and corresponding number of domains

def calculateDensity(coordinates):
	
	centroid_x=0
	centroid_y=0
	centroid_z=0

	for x in coordinates:
		centroid_x=x[0]+centroid_x
		centroid_y=x[1]+centroid_y
		centroid_z=x[2]+centroid_z

	try:
		centroid_x = 1.0*centroid_x/len(coordinates)
		centroid_y = 1.0*centroid_y/len(coordinates)
		centroid_z = 1.0*centroid_z/len(coordinates)
	except Exception, e:
		print "behold Null pointer", e,

	centroid = [centroid_x, centroid_y, centroid_z]		

	radius = 0.0

	for a in coordinates:
		radius = radius + utils.dist(a, centroid)	



	radius = radius/len(coordinates)

	density = 1.0*len(coordinates)/(radius*radius*radius)
	return density

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
						distance = utils.dist(cords_list[a],cords_list[b])
						if distance < 7.0:
							energy+=1
	return (1.0*energy/2)/len(matrix)

for x in cath_data:
	if x[0]!='#':
		cath_dict[x[:5].lower()] = int(x[7]+x[8])


for input_chain in input_chains:
	pdb = input_chain[:4]
	chain = input_chain[4]
	domains = cath_dict[pdb+chain]

	open_pdb = open(path_to_pdb_files+pdb+'.pdb','r')
	open_pdb_v2 = open(path_to_pdb_files+pdb+'.pdb','r') #Separate instances for calculating radiugs of gyration and coordinates

	cords_list, realId_list = getCordsList(open_pdb,chain.upper())

	x = np.asarray(cords_list)

	try:
		radius_gy = radius_of_gyration.radius_of_gyration(open_pdb_v2, chain.upper())
	except Exception, e:
			print "Unable to calculte Radius of gyration", pdb+chain, e
	length = len(cords_list)

	density = calculateDensity(cords_list)

	km = KMeans(n_clusters=2).fit(x) #Only splitting into two to find the interaction energy between two portions
	labels_km = km.labels_
		
	interaction_energy = getInteractionEnergy(labels_km, 2, cords_list)
	print pdb, ",", chain.upper(), "," ,domains, "," ,length, ", ", '{0:.3f}'.format(interaction_energy),", ", '{0:.3f}'.format(density),", ", '{0:.3f}'.format(radius_gy)

















