import os
from random import randint

path1 = "../Input Files"
path3 = "CathDomall"

file_path = os.path.join(path1, path3)

var = open(file_path, 'r')

inputDomains = raw_input("Enter the number of domains: ")

DomainsList = []

while 1:

	pdb = var.readline()

	if not pdb:
		break

	else:
		if pdb[0]!='#':

			domains = int(pdb[7] + pdb[8])
			frags = int(pdb[11] + pdb[12])

			if domains==int(inputDomains) and frags==0:
				DomainsList.append(pdb[:4])
DomainsList = list(set(DomainsList))
for x in DomainsList:
	print x