'''Program to read the output file after 
   applying Hari Krishna's method of Newman's modularity and then Clauset's  
   agglomeration method. The first part of the input file(*.txt) has all the nodes of 
   the pdb and their cluster number(as per Newman). Then intented line having "***" character
   is introduced followed by Clauset's merged clusters and the cluster numbers
'''


import fnmatch
import os





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




print "**************************************************************"

file_names = []
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, '*.txt'):
    	file_names.append(file)
        


for output in file_names:
	with open(output) as f:
		data = f.readlines()

	print output.split('.')[0]
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

		
	# for key in sorted(newman_clusters):		
	# 	print key, "====> ",newman_clusters[key]
	# 	print

	# print 

	# print "MERGED CLUSTERS"
	# for key in sorted(clauset_clusters):		
	# 	print key, "====> ",clauset_clusters[key]

 # 	print 
 	print "Total number of Domains ", len(clauset_clusters)
 	print
	domain_num = 1
	for key in sorted(clauset_clusters):
		resultant = []
		for clusters in clauset_clusters[key]:
			resultant = resultant + newman_clusters[clusters]

		resultant.sort()
		print "Domain #"+ str(domain_num)
		makeReadable(resultant)
		print
		print
		domain_num+=1

	print "**************************************************************"