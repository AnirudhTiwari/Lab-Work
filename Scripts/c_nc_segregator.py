from shutil import copy

def isContiguous(cath_boundaries):
	cath_boundaries = cath_boundaries.split(" ")
	cath_boundaries = filter(None, cath_boundaries)
	if cath_boundaries[2]=="F00":
		x = 3
		while 1:
			if x >= len(cath_boundaries):
				break
			else:
				numOFSegments = int(cath_boundaries[x])
				if numOFSegments > 1:
					return False
				else:
					x+=6*numOFSegments+1
		return True


file_500_proteins = "../Output Data/500_proteinsName.txt"
file_cathDomall = "../Input Files/CathDomall"

src = "/home/Tiwari/Documents/Work@Sem9/Thesis Work/Output Data/500_proteins/"
dest_contiguous = "/home/Tiwari/Documents/Work@Sem9/Thesis Work/Output Data/500_proteins/Contiguous/"
dest_nonContiguous = "/home/Tiwari/Documents/Work@Sem9/Thesis Work/Output Data/500_proteins/Non Contiguous/"

cath_entries = []
contiguous = []
non_contiguous = []

with open(file_cathDomall) as cath:
	for entries in cath:
		cath_entries.append(entries)


with open(file_500_proteins) as fp:
	for line in fp:
		pdb = str(line).strip()

		for entries in cath_entries:
			if entries[:4]==pdb:
				path = src + str(pdb) +".pdb"

				if isContiguous(entries):
					contiguous.append(pdb)
					try:
						copy(path,dest_contiguous)
					except IOError, e:
						print "I/O error({0}): {1}".format(e.errno, e.strerror)
				else:
					non_contiguous.append(pdb)
					try:
						copy(path,dest_nonContiguous)
					except IOError, e:
						print "I/O error({0}): {1}".format(e.errno, e.strerror)

a = set(contiguous).intersection(set(non_contiguous))
a = list(a)
print a
print len(a)






