input_fileName = "../Output Data/500_proteinsName.txt"
input_scopData = "../Input Files/dir.cla.scope.2.05-stable.txt"

with open(input_scopData) as fp:
	scop = fp.readlines()

with open(input_fileName) as fp1:
	pdb_id = fp1.readlines()

for pdb in pdb_id:
	pdb = pdb.strip()
	for data in scop:
		if data[0]!='#':
			data = data.split("\t")
			if data[1]==pdb:
				print data[0], "\t", data[1], "\t", data[2], "\t", data[3]
