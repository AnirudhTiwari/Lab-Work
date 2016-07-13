import fnmatch
import os
from operator import itemgetter
import math

cath_entries = []

with open("../../Input Files/CathDomall") as f:
	cath_entries = f.readlines()


file_names = []
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, '*.txt1'):
    	file_names.append(file)

for output in file_names:
	with open(output) as f:
		data = f.readlines()

	input_pdb = str(output.split('.')[0])[:4]
	input_chain = str(output.split('.')[0])[5]

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
			break
			nodes = nodes.split('\t')

			if nodes[1] not in clauset_clusters:
				clauset_clusters[nodes[1]] = []
				clauset_clusters[nodes[1]].append(nodes[0])
			else:
				clauset_clusters[nodes[1]].append(nodes[0])


	for key in sorted(newman_clusters):
		print key, newman_clusters[key]
		print	

