import os
from compiler.ast import flatten

def getCathDict(cath_boundaries, domains):
	cath_boundaries = cath_boundaries.split(" ")
	cath_boundaries = filter(None, cath_boundaries)
	cathDict = {}
	key = 0
	numOFSegments = 1
	x = 0
	flag=0

	while 1:
		if x >= len(cath_boundaries):
			break
		else:
			numOFSegments = int(cath_boundaries[x])

			if numOFSegments > 1:
				flag=1
				# temp = cath_boundaries[x:x+6*numOFSegments+1]
	
				# print temp
				# print "size", len(temp)
				# for y in range(numOFSegments):
				# 	# print 6*y+5
				# 	# print int(temp[6*y+5])-int(temp[6*y+2])
				# 	if((int(temp[6*y+5])-int(temp[6*y+2])) <= 10):
				# 		return cathDict, False

					
				
				# return cathDict, False
			dom = cath_boundaries[x:x+6*numOFSegments+1]
			cathDict[key] = dom
			key+=1
			x+=6*numOFSegments+1

	if flag==0:
		return cathDict, False

	else:
		return cathDict, True

input_fileNames = "../Output Data/500_proteins/nonContiguousProteins.txt"
input_cathData = "../Input Files/CathDomall"
input_chainData = "../Input Files/CathDomainList"

print "PDB, Chain, Domain Number, Class, CATH"
with open(input_fileNames, 'r') as f:
	lines = f.readlines()
	for pdb in lines:
		pdb=pdb.strip()
		with open(input_cathData, 'r') as f1:
			lines1 = f1.readlines()
			for entries in lines1:
				entries=entries.strip()
				if entries[:4]==pdb and entries[12]=='0':
					chain = entries[18]
					# if((pdb=="1nen" and chain=='D') or (pdb=="1djy" and chain=='A') or (pdb=="1nji" and chain=='C') or (pdb=="1nji" and chain=='M') or (pdb=="1e79")):
						# continue
					
					domains = int(entries[7] + entries[8])
					domain_boundary = entries[14:]

					# if int(domains)!=2:
					# 	continue

					cathDict, contiguous = getCathDict(domain_boundary, domains)
					if contiguous==False:
						continue

					
					

					for key, value in cathDict.iteritems():
						# print value
						print str(pdb) + ", ",
						print str(chain) + ", ",

						if domains==1:
							searchString = pdb+chain+"00"
						else:
							searchString = pdb+chain+"0"+str(key+1)

						with open(input_chainData, 'r') as f2:
							print str(key+1) + ", ",

							val="N/A"

							lines2 = f2.readlines()
							for classes in lines2:
								classes=classes.strip()

								if classes[:7]==searchString:
									if int(classes[12])==1:
										val = "a"

									if int(classes[12])==2:
										val = "b"

									if int(classes[12])==3:
										val = "a+b"

									if int(classes[12])==4:
										val = "a/b"

								
							ans = ''
							for x in value:
								ans= ans + x + " "
							print val + ", " + ans

								
								# print val + ", " + str(min(value)) + " - " + str(max(value))





					

