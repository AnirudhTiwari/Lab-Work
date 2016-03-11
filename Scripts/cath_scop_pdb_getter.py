import shutil


with open("cath_scop_final_pdb") as f1:
	pdb = f1.readlines()

src = "/run/media/Tiwari/Storage/pdb/data/structures/divided/"

for x in pdb:
	x = x.strip()
	name = "pdb" + x + ".ent"
	folder = x[1]+x[2] + "/"
	s = src + folder + name
	dest = "temp2/" + x + ".pdb"
	shutil.copy2(s, dest)


