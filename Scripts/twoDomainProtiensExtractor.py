import os
from random import randint

path1 = "../Input Files"
path3 = "CathDomall"

file_path = os.path.join(path1, path3)

var = open(file_path, 'r')

twoDomainsList = []

while 1:

	pdb = var.readline()

	if not pdb:
		break

	else:
		if pdb[0]!='#':

			domains = int(pdb[7] + pdb[8])
			frags = int(pdb[11] + pdb[12])

			if domains==2 and frags==0:
				twoDomainsList.append(pdb[:4])

for x in twoDomainsList:
	print x