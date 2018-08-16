import math
import sys

path_to_pdb_files = 'All PDBs/'

def calculateRadiusOfGyration(pdb, chain):
	pdb_file = open(path_to_pdb_files+pdb+'.pdb','r')
	return radius_of_gyration(pdb_file, chain)


def value_finder(start_value, end_value, array):

	coordinate = ''

	while(array[start_value]==' '):
		start_value = start_value+1



	while(int(start_value)!=int(end_value)):
		coordinate = coordinate + array[start_value];
		start_value = start_value + 1

	return coordinate

class pdb_atom:

	def __init__(self,coord_x,coord_y,coord_z):
		self.coordinate_x = coord_x
		self.coordinate_y = coord_y
		self.coordinate_z = coord_z



def radius_of_gyration(file_read, chain):
	# print "PDB ID:", var,

	protein_length = 0
	totalAtoms = 0
	com_x = 0.0
	com_y = 0.0
	com_z = 0.0
	atoms_list = []

	while 1:
		data = file_read.readline()

		if not data:
			break

		if(data[0]=='E' and data[1]=='N' and data[2]=='D'):
			break

		if(data[0]=='A' and data[1]=='T' and data[2]=='O' and data[21]==chain):


			totalAtoms = totalAtoms + 1

			coord_x = float(value_finder(31, 38, data))
			coord_y = float(value_finder(39, 46, data))
			coord_z = float(value_finder(47, 54, data))

			atom = pdb_atom(coord_x,coord_y,coord_z)

			atoms_list.append(atom)

			if(data[77]=='C'):

				com_x = com_x + (coord_x*12)
				com_y = com_y + (coord_y*12)
				com_z = com_z + (coord_z*12)

				if(data[13]=='C' and data[14]=='A'):
					protein_length = protein_length + 1


			elif(data[77]=='N'):

				com_x = com_x + (coord_x*14)
				com_y = com_y + (coord_y*14)
				com_z = com_z + (coord_z*14)

			elif(data[77]=='O'):

				com_x = com_x + (coord_x*16)
				com_y = com_y + (coord_y*16)
				com_z = com_z + (coord_z*16)



			elif(data[77]=='S'):

				com_x = com_x + (coord_x*32)
				com_y = com_y + (coord_y*32)
				com_z = com_z + (coord_z*32)

			else:

				com_x = com_x + coord_x*32
				com_y = com_y + coord_y*32
				com_z = com_z + coord_z*32

	com_x = com_x/(totalAtoms*12)
	com_y = com_y/(totalAtoms*12)
	com_z = com_z/(totalAtoms*12)

	radius_gyration = 0.0
	for alpha in atoms_list:

		radius_gyration = radius_gyration + math.pow((alpha.coordinate_x-com_x),2) + math.pow((alpha.coordinate_y-com_y),2) + math.pow((alpha.coordinate_z-com_z),2)
		#print radius_gyration

	radius_gyration = radius_gyration/totalAtoms
	# print  "Length of protein: ",protein_length,"Radius of Gyration: ", math.sqrt(radius_gyration)
	return math.sqrt(radius_gyration)


# var = str(sys.argv[1])

# file_read=open(var,'r')

# radius_of_gyration(file_read)



