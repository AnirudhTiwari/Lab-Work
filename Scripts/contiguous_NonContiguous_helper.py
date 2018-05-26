#This program outputs a .csv with the first entry being the pdb+chain and the next entry being Contiguous/NonContiguous. This output
#file is to be used everytime to judge whether a given chain is contigous or not.

import common_functions as utils

with open("CathDomall") as f:
	cath_data = f.readlines()

for x in cath_data:
	if x[0]!='#':
		pdb = x[:4]
		chain = x[4]
		domains = int(x[7]+x[8])
		boundaries = x[14:]
		print pdb+chain, 
		print ", ",
		if utils.isContiguous(boundaries, domains):
			print "Contiguous"
		else:
			print "NonContiguous"


