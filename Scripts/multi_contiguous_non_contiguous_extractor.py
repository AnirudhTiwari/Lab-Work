def isContiguous(cath_boundaries, domains):
	# print cath_boundaries
	cath_boundaries = cath_boundaries.split(" ")
	cath_boundaries = filter(None, cath_boundaries)
	cathDict = {}
	key = 0
	numOFSegments = 1
	x = 0
	while 1:
		if x >= len(cath_boundaries):
			break
		else:
			numOFSegments = int(cath_boundaries[x])
			if numOFSegments > 1:
				return False
			dom = cath_boundaries[x:x+6*numOFSegments+1]
			cathDict[key] = dom
			key+=1
			x+=6*numOFSegments+1
	return True

with open("multi_length_energy_density_radius_correct.csv") as f:
	multi_data = f.readlines()

with open('../Input Files/CathDomall', 'r') as f:
	cath_data = f.readlines()

for line in multi_data:
	pdb = line.split(",")[0].strip()
	chain = line.split(",")[1].strip()
	domains = int(line.split(",")[2].strip())

	
	for pdb_data in cath_data:
		# print pdb_data
		if pdb_data[:4]==pdb and pdb_data[4]==chain and isContiguous(pdb_data[14:].strip(),domains):
			print line.strip()





