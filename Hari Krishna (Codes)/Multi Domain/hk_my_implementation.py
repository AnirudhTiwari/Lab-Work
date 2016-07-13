from igraph import *
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



input_file_name = "2hbw_a_input"

with open(input_file_name) as f:
	data = f.readlines()

for x in data:
	x = x.strip()
	x = x.split(" ")
	pdb_name = x[0].lower()
	pdb_chain = x[1]

	print pdb_name, pdb_chain
	

	output_file_name = pdb_name + "_" + pdb_chain +"_"+ "edge_list"


	file_write = open(output_file_name, 'w')

	file_read = open("Second Dataset Multi/" + pdb_name + ".pdb",'r')

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

	