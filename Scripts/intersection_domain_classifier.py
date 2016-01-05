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

domain_file = "5"
cath_dom_file = "../Input Files/CathDomall"

with open(domain_file, 'r') as f:
	domains = f.readlines()

with open(cath_dom_file, 'r') as f:
	cath_doms = f.readlines()



non_contig = []
contig = []

for pdb in domains:
	pdb = pdb.split(" ")
	pdb = pdb[3].strip()
	for cath in cath_doms:
		if pdb==cath[:5].lower() and int(cath[11] + cath[12])==0:
			domain_boundary = cath[14:].strip()
			doms = int(cath[7] + cath[8])
			# print pdb, cath[:5].lower(), doms, domain_boundary
			if isContiguous(domain_boundary, doms):
				contig.append(pdb)

			else:
				non_contig.append(pdb)


# print len(contig)
# print len(non_contig)
# print non_contig

for x in non_contig:
	print x