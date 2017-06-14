# Finding the RSA of a pdb file and establishing 
# relation between k(no. of clusters)
# and no. of buried residues
import re
import common_functions as utils
from sklearn.cluster import *
import numpy as np

max_ASA = {
'ALA' : 121.0,
'ARG' : 265.0,
'ASN' : 187.0,
'CYS' : 148.0,
'ASP' : 187.0,
'GLU' : 214.0,
'GLN' : 214.0,
'GLY' : 97.0,
'HIS' : 216.0,
'ILE' : 195.0,
'LEU' : 191.0,
'LYS' : 230.0,
'MET' : 203.0,
'PHE' : 228.0,
'PRO' : 154.0,
'SER' : 143.0,
'THR' : 163.0,
'TRP' : 264.0,
'TYR' : 255.0,
'VAL' : 165.0,
'ASX' : 187.0 #As ASX can be either of ASN or ASP, so I have taken the mean of it.
} 

core_threshold = 15.0
RSA_cutoff = 20

with open('../Input Files/CathDomall', 'r') as f:
	cath_data = f.readlines()

with open('Final_dataset.txt', 'r') as f:
	input_pdb = f.readlines()

# with open('test_dataset.txt', 'r') as f:
# 	input_pdb = f.readlines()


def getDomainsFromCATH(pdb, chain):
	for x in cath_data:
		if pdb == x[:4] and chain == x[4]:
			domains = int(x[7] + x[8])
			return domains

def getDomainBoundary(pdb, chain):
	for x in cath_data:
		if pdb == x[:4] and chain == x[4]:
			return x[14:].strip()

def getResidueData(fileRead, chain):
	cords_list = []
	realId_list = []
	aminoAcid_list = []

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

				aminoAcid_list.append(data[17]+data[18]+data[19])
				cords_list.append(coordinates)
				realId_list.append(real_id)

	return cords_list,realId_list, aminoAcid_list

def getHydrophobicCoreDict(centroid_list, cords_list, realId_list, buried_residues_list, k):
	hydrophobicCoreDict = dict.fromkeys(list(xrange(k)))

	for coordinates in centroid_list:
		for buried_residue in buried_residues_list:
			buried_residue_coordinates = cords_list[realId_list.index(buried_residue)]
			distance = utils.dist(coordinates, buried_residue_coordinates)

			if distance <= core_threshold:
				cluster = centroid_list.index(coordinates)
				if hydrophobicCoreDict[cluster] == None:
					hydrophobicCoreDict[cluster] = set()

				hydrophobicCoreDict[cluster].add(buried_residue)

	return hydrophobicCoreDict



print "PDB", ", ", "Chain", ", ", "Domains", ", ", "Length", ", ", "No. of buried residues", ", ","Pairwise intersection with k=1", ", ", "k=2", ", ", "k=3", ", ", "k=4"
for entry in input_pdb:
	pdb = entry[:4].strip()
	chain = entry[4].strip().upper()
	domains = int(getDomainsFromCATH(pdb, chain))
	cath_boundary = getDomainBoundary(pdb, chain)
	if utils.isContiguous(cath_boundary, domains) and pdb=='1m70':
	# if 1:

		buried_residues_id = []

		path_to_pdb_file = "Second Dataset/" + pdb + ".pdb"
		# path_to_pdb_file = "Test Dataset/" + pdb + ".pdb"

		path_to_dssp_file = "DSSP/" + pdb + ".dssp"

		pdb_data = open(path_to_pdb_file, 'r');

		with open(path_to_dssp_file, 'r') as f:
			dssp_data = f.readlines()


		cords_list, realId_list, aminoAcid_list = getResidueData(pdb_data,chain) #Just to maintain legacy getCordsList from k_means_final.py

		print pdb,",", chain,",", domains,",", len(cords_list),", ",
		# print pdb,chain,domains


		for data in dssp_data:
			data = list(data)
			if data[-2]!='.' and data[2]!='#' and data[11]==chain:
				
				ACC = float(utils.value_finder(35, 40, data))
				residue_number = int(utils.value_finder(7,10,data))
				try:
					aminoAcid = aminoAcid_list[realId_list.index(residue_number)]
					RSA = ACC*100/max_ASA[aminoAcid]
				
					if RSA < RSA_cutoff:
						buried_residues_id.append(residue_number)
				except ValueError as e:
					pass
		print len(buried_residues_id),", ",
		# print
		# print sorted(buried_residues_id)
 		for k in range(1,5):
		# for k in range(1,2):
			intersection_set = set ()
			common_residues = 0
			x = np.asarray(cords_list)
			km = KMeans(n_clusters = k).fit(x)

			labels_km = km.labels_
			clusters_km = km.cluster_centers_

			hydrophobic_core_dict = getHydrophobicCoreDict(clusters_km.tolist()
				, cords_list, realId_list, buried_residues_id, k)
			
			for key, value in hydrophobic_core_dict.iteritems():
				print key, sorted(value)
				# print key, value
				print
			print

			for key, value in hydrophobic_core_dict.iteritems():
				# print key, sorted(value)
				# print len(value)
				for key_1, value_1 in hydrophobic_core_dict.iteritems():
					if key_1!=key:
						# print key_1, sorted(value_1)
						# print len(value_1)
						try:
							temp = set.intersection(value, value_1)
							# print temp,
							# print len(temp)
						except TypeError as e:
							pass

						common_residues+=len(temp)
			if k<4:
				print common_residues/2, ", ",
			else:
				print common_residues/2

			# boundaries = utils.domainBoundaries(labels_km, realId_list, k)

			# for key,value in boundaries.iteritems():
			# 	temp_buried_list = []
			# 	buried_residues = 0
			# 	for x in value:
			# 		if x in buried_residues_id:
			# 			# temp_buried_list.append(x)
			# 			buried_residues+=1
				
			# 	# print '+'.join(str(i) for i in temp_buried_list)
			# 	# print


			# 	print "{0:.2f}".format(buried_residues*100.0/len(value)),"(", buried_residues,"/",len(value),")"," ",
				# print "{0:.2f}".format(buried_residues*100.0/len(value))," ",


			# if k<=3:
			# 	print ",",

			# else:
			# 	print
