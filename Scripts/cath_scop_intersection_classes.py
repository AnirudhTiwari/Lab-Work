import json

def value_finder(start_residue, array):
	coordinate = ''

	while(array[start_residue]==' '):
		start_residue = start_residue+1

	while(array[start_residue]!=' '):
		coordinate = coordinate + array[start_residue];
		start_residue = start_residue + 1

		if(array[start_residue]=='-'):
			break

	return coordinate

intersection_file = "../Output Data/cath_scop_intersection/cath_scop_intersection.txt"
cath_list_file = "../Input Files/CathDomainList"

with open(intersection_file, 'r') as f:
	domains = f.readlines()

with open(cath_list_file, 'r') as f:
	cath_list = f.readlines()

classes = {}

counter = 0
for dom in domains:
	counter+=1
	dom = dom[:5]
	for chains in cath_list:
		if dom==chains[:5].lower():
			C = str(value_finder(12, chains))
			A = str(value_finder(17, chains))
			T = str(value_finder(21, chains))
			key = C + ', ' + A + ', ' + T
			if key in classes:
				classes[key].append(dom)
			else:
				classes[key] = []
				classes[key].append(dom)
	if counter==100:
		break

json.dump(classes, open("classes.json",'w'))
