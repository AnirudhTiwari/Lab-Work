cath_file = "../Input Files/CathDomall"
scop_file = "../Input Files/dir.cla.scope.2.05-stable.txt"

with open(cath_file, 'r') as f:
	cath_domains = f.readlines()

with open(scop_file, 'r') as f:
	scop_domains = f.readlines()


for cath in cath_domains:
	if cath[0]!='#':
		pdb = cath[:5].lower()
		doms = int(cath[7] + cath[8])
		# print pdb, doms
		counter = 0
		for scop in scop_domains:
			search_val = scop[1:6]
			if search_val==pdb:
				counter+=1

		if counter==doms:
			print pdb, doms

