# This program simply takes an input file which contains features calculated for a given protein and outputs all the 
# contiguous and non-contiguous chains based on the choice.

import common_functions as utils

with open("multi_test_length_energy_density_radius.csv") as f:
	data = f.readlines()

with open("CathDomall") as f:
	cath_data = f.readlines()

cath_dict = {} #A dict which holds if a given pdb+chain is contiguous or not

for x in cath_data:
	if x[0]!='#':
		pdb = x[:4]
		chain = x[4]
		domains = int(x[7]+x[8])
		boundaries = x[14:]
		cath_dict[pdb+chain] = utils.isContiguous(boundaries, domains)

for x in data:
	y = x.split(",")
	pdb = y[0].strip()
	chain = y[1].strip()
	if not cath_dict[pdb+chain]:
		print x.strip()


