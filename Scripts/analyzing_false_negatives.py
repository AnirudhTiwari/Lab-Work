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

with open('../Output Data/false_negatives_entries', 'r') as f1:
	neg_entries = f1.readlines()


with open('../Input Files/CathDomall', 'r') as f2:
	cath_entries = f2.readlines()


for x in neg_entries:
	neg_pdb = x[:4].strip()
	neg_chain = x[4].lower().strip()

	for y in cath_entries:
		if y[0]!='#':
			cath_pdb = y[:4].lower().strip()

			cath_chain = y[18].lower().strip()

			cath_domains = int(y[7] + y[8])

			if cath_pdb==neg_pdb and cath_chain==neg_chain:
				print y,
				if isContiguous(y[15:], cath_domains):
					print "Contiguous"
				else:
					print "Non Contiguous"
				print


