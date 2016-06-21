'''Program to read the output file after 
   applying Hari Krishna's method of Newman's modularity and then Clauset's  
   agglomeration method. The first part of the input file(*.txt) has all the nodes of 
   the pdb and their cluster number(as per Newman). Then intented line having "***" character
   is introduced followed by Clauset's merged clusters and the cluster numbers
'''


import fnmatch
import os
from operator import itemgetter

def makeReadable(boundaries):
	# print boundaries
	temp_list = []
	flag = 0

	for x in range(0,len(boundaries)-1):
		if boundaries[x+1] - boundaries[x]==1:
			temp_list.append(boundaries[x])

		else:
			if len(temp_list)!=0:
				temp_list.append(boundaries[x])
				# print temp_list
				print min(temp_list), "-", max(temp_list),
				temp_list = []

	if flag==0 and len(temp_list)!=0:
		# print temp_list
		print  min(temp_list), "-", max(temp_list)+1,

	print "--",

def stitchPatches(k_means, patch_length):
	island = []
	for key, value in k_means.iteritems():
		x=0
		while x!=len(value):
			counter=0
			for y in range(x+1,len(value)-1,1):
				if value[y]-value[y-1]!=1:
					if len(value[x:y])<= patch_length:
						patch = value[x:y]
						island.append(patch)
					break

				elif y==len(value)-2:
					if len(value[x:y+2])<=patch_length:
						patch = value[x:y+2]
						island.append(patch)
					break
				counter+=1
			x+=(counter+1)

	island = internalStitch(island, patch_length)

	# print "After internal Stitch"
	# print k_means
	# print "ISLANDS"
	# print island


	mean_list = []
	for key, value in k_means.iteritems():
		for patches in island:
			for x in patches:
				if x in value:
					value.remove(x)

	# print "Before sequence stitch"

	# print k_means

	k_means = sequenceStitch(k_means, island)

	return k_means

def sequenceStitch(k_means, island):
	minimum = 100000000
	for key, values in k_means.iteritems():
		if len(values)==0:
			return k_means
		if minimum > min(values):
			minimum = min(values)

	for patches in island:
		low = patches[0] - 1
		high = patches[-1] + 1
		for key, value in k_means.iteritems():
			if low < minimum:
				if high in value:
					k_means[key] = sorted(list(set(k_means[key]  + patches)))

			if low in value and high in value:
				k_means[key] = sorted(list(set(k_means[key]  + patches)))

			if low in value and high not in value:
				k_means[key] = sorted(list(set(k_means[key]  + patches)))
	return k_means

def internalStitch(island, patch_length):
	remove = []
	for x in range(len(island)-1):
		island.sort(key=itemgetter(0))
		high = max(island[x])+1

		if high==island[x+1][0] and (len(island[x]) + len(island[x+1]) <= patch_length):
			remove.append(x)
			island[x+1] = sorted(island[x] + island[x+1])

	final = []
	for x in range(len(island)):
		if x not in remove:
			final.append(island[x])

	return final


# print "**************************************************************"

correct = 0
cath_entries = []

with open("../../Input Files/CathDomall") as f:
	cath_entries = f.readlines()

file_names = []
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, '*.txt'):
    	file_names.append(file)

for output in file_names:
	with open(output) as f:
		data = f.readlines()

	input_pdb = str(output.split('.')[0])[:4]
	input_chain = str(output.split('.')[0])[5]
	# print input_pdb, input_chain.upper(),

	newman_clusters = {}
	clauset_clusters = {}
	clauset_flag = 0

	for nodes in data:
		nodes = nodes.strip()

		if nodes=="***":
			clauset_flag = 1
			continue

		elif clauset_flag == 0:
			nodes = nodes.split('\t')

			if nodes[1] not in newman_clusters:
				newman_clusters[nodes[1]] = []
				newman_clusters[nodes[1]].append(int(nodes[0]))
			else:
				newman_clusters[nodes[1]].append(int(nodes[0]))

		elif clauset_flag == 1:
			nodes = nodes.split('\t')

			if nodes[1] not in clauset_clusters:
				clauset_clusters[nodes[1]] = []
				clauset_clusters[nodes[1]].append(nodes[0])
			else:
				clauset_clusters[nodes[1]].append(nodes[0])

		

 	# print len(clauset_clusters),
 	# print

 	for entries in cath_entries:
 		if entries[0]!='#':
			pdb_name = str(entries)[:4].strip()
			pdb_chain = str(entries)[18].strip().lower()
			domains = int(entries[7]+entries[8])

			# print "CAth", pdb_name, pdb_chain, domains
			if pdb_name==input_pdb and pdb_chain==input_chain:
				if int(domains) == int(len(clauset_clusters)) and int(domains)==3:
					correct+=1




	for key in sorted(clauset_clusters):
		resultant = []
		for clusters in clauset_clusters[key]:
			resultant = resultant + newman_clusters[clusters]

		resultant.sort()
		clauset_clusters[key] = resultant


	clauset_clusters = stitchPatches(clauset_clusters, 10)

	domain_num = 1

	# for key in sorted(clauset_clusters):

	# 	print "Domain #"+ str(domain_num)

	# 	makeReadable(clauset_clusters[key])

	# 	print
	# 	print
	# 	domain_num+=1

	# print "**************************************************************"

print correct