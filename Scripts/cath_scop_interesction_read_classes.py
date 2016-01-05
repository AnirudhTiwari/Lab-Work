import json
from pprint import pprint

with open('classes.json') as data_file:    
    data = json.load(data_file)

# pprint(data)

# print len(data)

with open('../Input Files/CathDomall') as f:
	doms = f.readlines()

cath  = {}

for x in doms:
	if x[0]!='#':
		y = int(x[7] + x[8])
		cath[x[:5].lower()]=y



dom_list = []


for key,value in data.items():
	for pdb in value:
		if pdb not in dom_list:
			if cath[pdb]==5:
				dom_list.append(pdb)
				print key, pdb
				break



print len(dom_list)
# pprint(data)