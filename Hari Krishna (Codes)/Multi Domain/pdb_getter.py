import shutil


# with open("sample_input_hk_thesis.txt") as f1:
with open("multi_domain_second_dataset") as f1:
	pdb = f1.readlines()

src = "/run/media/Tiwari/Storage/pdb/data/structures/divided/"

for x in pdb:
	x = x.lower()
	try:
		x = x.strip()
		name = "pdb" + x[:4] + ".ent"
		folder = x[1]+x[2] + "/"
		s = src + folder + name

		dest = x[:4] + ".pdb"
		shutil.copy2(s, dest)
		
	except IOError, e:
		print " Remove this pdb ", x


