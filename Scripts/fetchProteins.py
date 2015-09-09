import os
import math
from igraph import *
from sklearn.cluster import *
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import re
from compiler.ast import flatten
from operator import itemgetter
from shutil import copy

file_1D = "../Output Data/oneDomainProteins.txt"
file_2D = "../Output Data/twoDomainProteins.txt"
file_3D = "../Output Data/threeDomainProteins.txt"
file_4D = "../Output Data/fourDomainProteins.txt"
file_5D = "../Output Data/fiveDomainProteins.txt"

files = [file_1D, file_2D, file_3D, file_4D, file_5D]

for pdb_lists in files:
	var = open(pdb_lists, 'r')
	
	temp_list = []

	while 1:
		pdb_id = var.readline().strip()
		if not pdb_id:
			break
		else:
			temp_list.append(pdb_id)

	counter = 0

	for pdb in temp_list:

		if counter==100:
			break

		else:
			print pdb
			src = "/run/media/tiwari/Storage/pdb/data/structures/divided/"+str(pdb[1:3])+"/"+"pdb"+str(pdb)+".ent"
			dest = "/home/tiwari/Documents/Work@Sem9/Thesis Work/Output Data/500_proteins/"+str(pdb)+".pdb"
			try:
				copy(src,dest)
				counter+=1
			except IOError, e:
				print "I/O error({0}): {1}".format(e.errno, e.strerror)
