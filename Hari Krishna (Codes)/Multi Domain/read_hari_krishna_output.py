'''Program to read the output file after 
   applying Hari Krishna's method of Newman's modularity and then Clauset's  
   agglomeration method. The first part of the input file(*.txt) has all the nodes of 
   the pdb and their cluster number(as per Newman). Then intented line having "***" character
   is introduced followed by Clauset's merged clusters and the cluster numbers
'''


import fnmatch
import os
from operator import itemgetter
import math

class pdb_atom:	
	def __init__(self,residue_name,chain,residue_no,coord_x,coord_y,coord_z,hydro):
		self.name = residue_name
		self.chain = chain
		self.residue_no = residue_no
		self.coordinate_x = coord_x
		self.coordinate_y = coord_y
		self.coordinate_z = coord_z
		self.hydrophobic = hydro


def value_finder(start_value, end_value, array):

	coordinate = ''

	while array[start_value]==' ':
		start_value = start_value+1



	while int(start_value)!=int(end_value):
		coordinate = coordinate + array[start_value];
		start_value = start_value + 1

	return coordinate


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

def stitchPatches(k_means, patch_length):
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

	# print "After internal Stitch"
	# print k_means
	# print "ISLANDS"
	# print island


	mean_list = []
	for key, value in k_means.iteritems():
		for patches in island:
			for x in patches:
				if x in value:
					value.remove(x)

	# print "Before sequence stitch"

	# print k_means

	k_means = sequenceStitch(k_means, island)

	return k_means

def sequenceStitch(k_means, island):
	minimum = 100000000
	for key, values in k_means.iteritems():
		if len(values)==0:
			return k_means
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


def mapGraphToCATH(cath_entry, clusters): # cath_entry => Exact cath entry from colmun 13(CATHDOMALL), and clusters is newman's clusters(dict format) 
	cath_entry = cath_entry.split(" ")
	cath_entry = filter(None, cath_entry)

	offset = 80000000

	x = 0
	numOFSegments = 1

	while 1:
		if x >= len(cath_entry):
			break
		else:
			numOFSegments = int(cath_entry[x])
			
			dom = cath_entry[x+1:x+6*numOFSegments+1]
			# print dom

			for y in dom:
				try:
					y = int(y)

					if y < offset:
						offset = y
				except:
					continue
			x+=6*numOFSegments+1

	for key, value in clusters.iteritems():
		new_value = []
		for x in value:
			new_value.append(x+offset-1)

		clusters[key] = new_value

	return clusters

def dist(a,b):
	# print a, b
	for x in range(3):
		distance = math.pow((math.pow((a[0]-b[0]),2) + math.pow((a[1]-b[1]),2) + math.pow((a[2]-b[2]),2)), 0.5)
		return distance
	
def calculateEnergy(atoms_data, clusters):
	
	energy_dict = {}

	for base_cluster in sorted(clusters):

		# for target_cluster in range(int(base_cluster)+1, len(clusters)+1):

		for target_cluster in sorted(clusters):
			if int(target_cluster) > int(base_cluster):

				energy = 0.0

				# print clusters[base_cluster]
				# print
				# print clusters[str(target_cluster)]


				for res_a in clusters[base_cluster]:
					for res_b in clusters[str(target_cluster)]:
						try:
							distance = dist(atoms_data[res_a],atoms_data[res_b])

						except KeyError:
							continue

						if distance < 7.0:
							energy = energy + 1/distance

				base_length = len(clusters[base_cluster])
				target_length = len(clusters[str(target_cluster)])

				final_energy = energy/( base_length + target_length )
				# final_energy = energy

				# print base_cluster, target_cluster, "{0:.2f}".format(final_energy),

				# print base_length, target_length

				# print

				if base_cluster in energy_dict:
					energy_dict[base_cluster].append(final_energy)

				else:
					energy_dict[base_cluster] = []
					energy_dict[base_cluster].append(final_energy)

	return energy_dict




# print "**************************************************************"

correct = 0
cath_entries = []

with open("../../Input Files/CathDomall") as f:
	cath_entries = f.readlines()


file_names = []
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, '*.txt'):
    	file_names.append(file)

for output in file_names:
	with open(output) as f:
		data = f.readlines()

	input_pdb = str(output.split('.')[0])[:4]
	input_chain = str(output.split('.')[0])[5]

#	From here till line 258, the program is to get the coordinates
 #   and set the class pdb_atom for the given input pdb

 	print input_pdb,
 	print input_chain


	file_pdb = open("Second Dataset Multi/" + input_pdb + ".pdb",'r')

	alpha_atoms_data = []

	while 1:	
		data_pdb = file_pdb.readline()

		if not data_pdb:
			break

		if data_pdb[0]=='A' and data_pdb[1]=='T':
			if data_pdb[13]=='C' and data_pdb[14]=='A':

				chain = data_pdb[21]

				if chain.lower()==input_chain.lower().strip():

					residue_name = data_pdb[17] + data_pdb[18] + data_pdb[19]
					

					residue_no = value_finder(22, 26, data_pdb)	
						
					coord_x = float(value_finder(30, 38, data_pdb))

					coord_y = float(value_finder(38, 46, data_pdb))

					coord_z = float(value_finder(46, 54, data_pdb))

					

					if(residue_name=='ALA' or residue_name=='ILE' or residue_name=='LEU' or residue_name=='PHE' or residue_name=='VAL' or residue_name=='PRO' or residue_name=='GLY'):
						hydrophobic = True
					else:
						hydrophobic = False	

					alpha = pdb_atom(residue_name, chain, int(residue_no), float(coord_x), float(coord_y), float(coord_z), hydrophobic)

					# write_coordinates =  str(residue_no) + ' ' + coord_x + ' ' + coord_y + ' ' + coord_z + ' ' + str(hydrophobic) + '\n'

					add_flag = 0

					for x in alpha_atoms_data:
						if int(residue_no)==x.residue_no:
							add_flag=1
							break

					if add_flag == 0:
						alpha_atoms_data.append(alpha)		

					# print residue_no, coord_x, coord_y, coord_z			
	file_pdb.close()
	# print len(alpha_atoms_data)

	# print input_pdb, input_chain.upper(),

	newman_clusters = {}
	clauset_clusters = {}
	clauset_flag = 0

	for nodes in data:
		
		nodes = nodes.strip()

		if nodes=="***":
			clauset_flag = 1
			continue

		elif clauset_flag == 0:
			nodes = nodes.split('\t')

			if nodes[1] not in newman_clusters:
				newman_clusters[nodes[1]] = []
				newman_clusters[nodes[1]].append(int(nodes[0]))
			else:
				newman_clusters[nodes[1]].append(int(nodes[0]))

		elif clauset_flag == 1:
			nodes = nodes.split('\t')

			if nodes[1] not in clauset_clusters:
				clauset_clusters[nodes[1]] = []
				clauset_clusters[nodes[1]].append(nodes[0])
			else:
				clauset_clusters[nodes[1]].append(nodes[0])

	
	for entries in cath_entries:
		if entries[0]!='#':
			
			pdb_name = str(entries)[:4].strip()
			pdb_chain = str(entries)[18].strip()
			
			# print pdb_name, pdb_chain, input_pdb, input_chain

			if pdb_name==input_pdb.strip() and pdb_chain.lower()==input_chain.strip().lower():
				newman_clusters = mapGraphToCATH(entries[13:].strip(), newman_clusters)

	# for key in sorted(newman_clusters):
	# 	print key, newman_clusters[key]
		# makeReadable(newman_clusters[key])
 	# print len(clauset_clusters),
 	# print
# '''
# 	Using IE to merge Newman's cluster and not using clauset's algorithm.
	# Step 1: Calculate pairwise interaction energy of each cluster
	# Step 2: Merge all those clusters whose IE <= 0.25 and frag-length <= 30
	# Step 3: If there is nothing to be merged, then stop.
# '''
	

	clusters_energy = {}
	atoms_coordinates_dict = {}


	# for key in sorted(newman_clusters):
	# 	print key, newman_clusters[key]
	# 	print


	for atom in alpha_atoms_data:
		atoms_coordinates_dict[atom.residue_no]=[atom.coordinate_x, atom.coordinate_y, atom.coordinate_z]

	steps = 1

	while 1:

		print "************************************** STEP #", steps, "****************************"

		print "BEFORE MERGE"

		for key in sorted(newman_clusters):
			print key,
			makeReadable(newman_clusters[key])
		 	print
		 	print

		clusters_energy = calculateEnergy(atoms_coordinates_dict, newman_clusters)

		print

		for key in sorted(clusters_energy):
			
			print key, 
			for energy in clusters_energy[key]:
				print "{0:.3f}".format(energy),

			print


		max_energy = -10000000.0

		merge_1 = "NULL"
		merge_2 = "NULL"


		print

		for key in sorted(clusters_energy):
			for energy in clusters_energy[key]:
				if energy >= max_energy:# and energy <= 0.25:
					merge_1 = key
					merge_2 = str(int(clusters_energy[key].index(energy)) + 1 + int(key))
					max_energy = energy

		print "Merge Cluster", merge_1,"& Cluster", merge_2

		print 
		
		newman_clusters[merge_1] = sorted(newman_clusters[merge_1] + newman_clusters[merge_2])

		try:
			for key in sorted(newman_clusters):
				if int(key) > int(merge_2):
					temp = newman_clusters[key]
					del newman_clusters[key]
					newman_clusters[str(int(key)-1)] = temp

				elif int(merge_2) == len(newman_clusters):
					del newman_clusters[merge_2]

		
		except KeyError:
			print "SOMETHING WRONG"


		print "AFTER MERGE"
		for key in sorted(newman_clusters):
			print key,
			makeReadable(newman_clusters[key])
		 	print
		 	print


	 	print "************************************ END OF STEP ***************************"

	 	steps+=1
		if len(newman_clusters) == 2 or merge_1=="NULL" or merge_2=="NULL":
			break

 	# for entries in cath_entries:
 	# 	if entries[0]!='#':
		# 	pdb_name = str(entries)[:4].strip()
		# 	pdb_chain = str(entries)[18].strip().lower()
		# 	domains = int(entries[7]+entries[8])

		# 	# print "CAth", pdb_name, pdb_chain, domains
		# 	if pdb_name==input_pdb and pdb_chain==input_chain:
		# 		if int(domains) == int(len(clauset_clusters)) and int(domains)==3:
		# 			correct+=1




	# for key in sorted(clauset_clusters):
	# 	resultant = []
	# 	for clusters in clauset_clusters[key]:
	# 		resultant = resultant + newman_clusters[clusters]

	# 	resultant.sort()
	# 	clauset_clusters[key] = resultant


	# clauset_clusters = stitchPatches(clauset_clusters, 10)

	# domain_num = 1

	# for key in sorted(clauset_clusters):

	# 	print "Domain #"+ str(domain_num)

	# 	makeReadable(clauset_clusters[key])

	# 	print
	# 	print
	# 	domain_num+=1

	# print "**************************************************************"

# print correct