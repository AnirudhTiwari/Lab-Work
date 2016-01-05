intersection_file = "../Output Data/cath_scop_intersection/cath_scop_intersection.txt"

with open(intersection_file, 'r') as f:
	domains = f.readlines()

doms = {}


for x in domains:
	x = x.split()
	if x[1] in doms:
		doms[x[1]]+=1
	else:
		doms[x[1]]=1

for key,value in doms.items():
	print key, value
