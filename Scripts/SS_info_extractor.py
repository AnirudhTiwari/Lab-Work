input_chains = []

with open("Second Dataset Chains/four_domains") as f:
	single_data = f.readlines()

for x in single_data:
	x = x.strip()
	input_chains.append(x)

for x in input_chains:
	ss_file = "DSSP/" + str(x[:4]) + ".dssp"

	ss = ""
	with open(ss_file) as f1:
		ss_data = f1.readlines()



	for lines in ss_data:
		lines = list(lines)
		if lines[-2]!='.' and lines[2]!='#' and lines[11].lower()==str(x[4]):
			ss += lines[16]
	
	print x[:4] + "," + x[4].upper()+ ",4" + "," + ss
