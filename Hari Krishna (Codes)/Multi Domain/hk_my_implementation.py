from igraph import *
from operator import itemgetter

cutoff = 7.0

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


def dist(a,b):
	# print a, b
	for x in range(3):
		distance = math.pow((math.pow((a[0]-b[0]),2) + math.pow((a[1]-b[1]),2) + math.pow((a[2]-b[2]),2)), 0.5)
		return distance


def assignWeights(graph, clusters, alpha_atoms_data):
	# print len(alpha_atoms_data)
	weight_list = []
	for key in sorted(clusters):
		temp = []
		for key2 in sorted(clusters):
			weight = 0
			if key!=key2:
				for res_a in clusters[key]:
					for res_b in clusters[key2]:
						# print key, key2, res_a, res_b
						A = [alpha_atoms_data[res_a].coordinate_x, alpha_atoms_data[res_a].coordinate_y, alpha_atoms_data[res_a].coordinate_z]
						B = [alpha_atoms_data[res_b].coordinate_x, alpha_atoms_data[res_b].coordinate_y, alpha_atoms_data[res_b].coordinate_z]
						distance = dist(A,B)

						if distance <= 7.0:
							weight+=1

				if graph:
					graph[int(key), int(key2)]=100*weight/(len(clusters[key]) + len(clusters[key2]))
				temp.append(100*weight/(len(clusters[key]) + len(clusters[key2])))
				# weight_list.append(weight)
			else:
				temp.append(0)
				# weight_list.append(0)
				if graph:
					graph[int(key), int(key2)]=0


		weight_list.append(temp)


	return graph, weight_list

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

def calculateEnergy(atoms_data, clusters):
	
	energy_dict = {}

	for base_cluster in sorted(clusters):

		# for target_cluster in range(int(base_cluster)+1, len(clusters)+1):

		for target_cluster in sorted(clusters):
			# if int(target_cluster) > int(base_cluster):
			if target_cluster!=base_cluster:

			# if int(target_cluster) > int(base_cluster):


				# print clusters[base_cluster]
				# print
				# print clusters[str(target_cluster)]

				energy = 0

				for res_a in clusters[base_cluster]:
					for res_b in clusters[target_cluster]:
						try:
							distance = dist(atoms_data[res_a],atoms_data[res_b])

						except KeyError:
							continue

						if distance <= 7.0:
							energy+=1

				base_length = len(clusters[base_cluster])
				target_length = len(clusters[int(target_cluster)])

				# final_energy = energy/( base_length + target_length )
				final_energy = energy

				# print base_cluster, target_cluster, "{0:.2f}".format(final_energy)
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
			new_value.append(x+offset)

		clusters[key] = new_value

	return clusters

def convertListToDict(newman_dict, weight_list):
	answer = {}
	cluster = 0

	for key in sorted(newman_dict):
		answer[key] = weight_list[cluster]
		cluster+=1

	return answer


# input_file_name = "sample_input_hk_thesis_2"
input_file_name = "new_multidomain_set"

# input_file_name = "clauset_dry_run_dataset"

cath_entries = []

with open("../../Input Files/CathDomall") as f:
	cath_entries = f.readlines()


with open(input_file_name) as f:
	data = f.readlines()

for x in data:
	x = x.strip()
	x = x.split(" ")
	pdb_name = x[0].lower()
	pdb_chain = x[1]

	print pdb_name, ",", pdb_chain.upper(),",",
	

	output_file_name = pdb_name + "_" + pdb_chain +"_"+ "edge_list"


	file_write = open(output_file_name, 'w')

	file_read = open("Second Dataset Multi/" + pdb_name + ".pdb",'r')
	# file_read = open("Hari Krishnas Data Set/" + pdb_name + ".pdb", 'r')

	alpha_atoms_data = []

	while 1:	
		data = file_read.readline()

		if not data:
			break

		if data[0]=='A' and data[1]=='T':
			if data[13]=='C' and data[14]=='A':
				chain = data[21]
				if chain.lower()==pdb_chain:

					residue_name = data[17] + data[18] + data[19]
					

					residue_no = value_finder(22, 26, data)	
						
					coord_x = float(value_finder(30, 38, data))

					coord_y = float(value_finder(38, 46, data))

					coord_z = float(value_finder(46, 54, data))

					

					if(residue_name=='ALA' or residue_name=='ILE' or residue_name=='LEU' or residue_name=='PHE' or residue_name=='VAL' or residue_name=='PRO' or residue_name=='GLY'):
						hydrophobic = True
					else:
						hydrophobic = False	

					alpha = pdb_atom(residue_name, chain, int(residue_no), float(coord_x), float(coord_y), float(coord_z), hydrophobic)

					add_flag = 0

					for x in alpha_atoms_data:
						if int(residue_no)==x.residue_no:
							add_flag=1
							break

					if add_flag == 0:
						alpha_atoms_data.append(alpha)		

	file_read.close()

	size = len(alpha_atoms_data)

	adjacency_matrix = [[0 for x in range(size)] for x in range(size)]

	graph = Graph(size)



	edge_list = []

	for a in range(0,size):

		ref_atom = alpha_atoms_data[a]
		ref_x = ref_atom.coordinate_x
		ref_y = ref_atom.coordinate_y
		ref_z = ref_atom.coordinate_z

		for b in range(a+1,size):
			
			target_atom = alpha_atoms_data[b]

			target_x = target_atom.coordinate_x
			target_y = target_atom.coordinate_y
			target_z = target_atom.coordinate_z


			adjacency_matrix[a][b] = math.sqrt(math.pow((target_x-ref_x),2) + math.pow((target_y-ref_y),2) + math.pow((target_z-ref_z),2))
			if adjacency_matrix[a][b] <= cutoff:
				adjacency_matrix[a][b] = 1
				edge_list.append((a,b))



	graph.add_edges(edge_list)

	newman_output = graph.community_leading_eigenvector()

	newman_dict = {}
	cluster = 0

	for x in newman_output:
		newman_dict[cluster] = x
		cluster+=1




	condensed_graph = Graph(len(newman_dict))

	condensed_graph.es[ "weight" ] = 1.0

	condensed_graph, weight_list = assignWeights(condensed_graph, newman_dict, alpha_atoms_data)

	# for weights in weight_list:
	# 	print weights



	clustered_dendrogram = condensed_graph.community_fastgreedy()
	# print clustered_dendrogram

	for entries in cath_entries:
		if entries[0]!='#':
			
			name = str(entries)[:4].strip()
			chain = str(entries)[18].strip()
			
			if name==pdb_name.strip() and chain.lower()==pdb_chain.strip().lower():
				print int(entries[7]+entries[8]),",", entries[19:].strip(), ","
				# newman_dict = mapGraphToCATH(entries[13:].strip(), newman_dict)

	final_clusters = {}

	domain_number = 1

	# print "No. of Domains: ", clustered_dendrogram.optimal_count
	# print

	# for key in sorted(newman_dict):
	# 	print key, 
	# 	makeReadable(newman_dict[key])
	# 	print

	# print
	# print clustered_dendrogram.merges
	# print

	for cluster in clustered_dendrogram.as_clustering():
		resultant_cluster = []
		for node in cluster:
			resultant_cluster+=newman_dict[node]

		final_clusters[domain_number] = resultant_cluster
		domain_number+=1

	# final_clusters  = stitchPatches(final_clusters, 5)

	# for cluster in sorted(final_clusters):
	# 	makeReadable(sorted(final_clusters[cluster]))

	# print
	# print
	# print 

	final_clusters_2 = {}
	count = 1 
	for cluster in clustered_dendrogram.as_clustering(2):
		resultant = []
		for nodes in cluster:
			resultant+=newman_dict[nodes]

		final_clusters_2[count]=sorted(resultant)
		count+=1


	# final_clusters_2 = stitchPatches(final_clusters_2, 10)

	# for x in sorted(final_clusters_2):
	# 	makeReadable(final_clusters_2[x])
	# 	print
	# 	print



	# print
	# print "**************************CLAUSET'S END***************************"
	# print
	# print

# 	print "*****************************IE************************************"
# 	print
# 	print
# 	# '''
# # 	Using IE to merge Newman's cluster and not using clauset's algorithm.
# 	# Step 1: Calculate pairwise interaction energy of each cluster
# 	# Step 2: Merge all those clusters whose IE <= 0.25 and frag-length <= 30
# 	# Step 3: If there is nothing to be merged, then stop.
# # '''
	

	clusters_energy = {}
	atoms_coordinates_dict = {}
	merge_energy = []


	# for key in sorted(newman_clusters):
	# 	print key, newman_clusters[key]
	# 	print


	for atom in alpha_atoms_data:
		atoms_coordinates_dict[atom.residue_no]=[atom.coordinate_x, atom.coordinate_y, atom.coordinate_z]

	steps = 1

	while 1:

		print "************************************** STEP #", steps, "****************************"

		print "BEFORE MERGE"

		for key in sorted(newman_dict):

			print key,
			makeReadable(newman_dict[key])
		 	print
		 	print

		clusters_energy = calculateEnergy(atoms_coordinates_dict, newman_dict)

		garbage, clusters_energy_list = assignWeights(None, newman_dict, alpha_atoms_data)

		
		clusters_energy = convertListToDict(newman_dict, clusters_energy_list)

		print

		# for key in sorted(clusters_energy):
		# 	print key, 
		# 	for energy in clusters_energy[key]:
		# 		print "{0:.3f}".format(energy),
		# 	print
		# break

		max_energy = -10000000.0

		merge_1 = "NULL"
		merge_2 = "NULL"


		print

		for key in sorted(clusters_energy):
			for energy in clusters_energy[key]:
				if energy > max_energy:# and energy <= 0.25:
					merge_1 = key
					merge_2 = sorted(clusters_energy.keys())[clusters_energy[key].index(energy)]
					max_energy = energy

		print "Max Energy:", max_energy

		merge_energy.append(max_energy)

		print "Merge Cluster", merge_1,"& Cluster", merge_2

		print 

		newman_dict[max(clusters_energy.keys(), key=int) + 1] = sorted(newman_dict[merge_1] + newman_dict[merge_2])
		

		try:
			del newman_dict[merge_1]
			del newman_dict[merge_2]
		
		except KeyError:
			print "SOMETHING WRONG"


		print "AFTER MERGE"
		for key in sorted(newman_dict):
			print key,
			makeReadable(newman_dict[key])
		 	print
		 	print


	 	# print "************************************ END OF STEP ***************************"

	 	steps+=1
		if len(newman_dict) == 1 or merge_1=="NULL" or merge_2=="NULL":
			# for x in merge_energy:
			# 	print x,
			# print
			break







