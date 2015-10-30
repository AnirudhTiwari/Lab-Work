import os

directory = "../Output Data/500_proteins/Non Contiguous/"
protein_list = []

for pdb in os.listdir(directory):
	name = pdb.split('.')[0]
	protein_list.append(name)

for x in protein_list:
	print x
