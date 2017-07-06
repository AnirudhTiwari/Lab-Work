# The idea is to cover each and every class(C,A,T) for each of 2,3 and 4 domain protein but also to ensure that
# these chains are not present in the testing dataset. Also, the number of 2,3 and 4 domain proteins should be equal
# Steps:
# 1. Load the CATH classes file
# 2. for each given class, find a 2,3 and 4 domain chain which doesn't belong to the testing dataset.
# 

import ast
import random

with open('../Input Files/CathDomall', 'r') as f:
	cath_entries = f.readlines()

with open('cath_classes_copy.txt', 'r') as f:
	cath_classes = f.readlines()

with open('multi_length_energy_density_radius_correct.csv', 'r') as f:
	multi_data = f.readlines()

testing_data = []

cath_dict = {}
for x in cath_entries:
	if x[0]!='#':
		pdb = x[:4]
		chain = x[4].strip().lower()
		domains = int(x[7]+x[8])
		cath_dict[pdb+chain]=domains

# def getNumberOfDomains(chain):


for x in multi_data:
	x = x.split(",")
	pdb = x[0].strip()
	chain = x[1].strip().lower()
	testing_data.append(pdb+chain)

regenerated_cath_dict = {}

for x in cath_classes:
	y = x.partition("=")
	cath_class = ast.literal_eval(y[0])
	cath_domains = ast.literal_eval(y[2])
	regenerated_cath_dict[cath_class] = cath_domains

two_domain_training = []
three_domain_training = []
four_domain_training = []

for key, value in regenerated_cath_dict.iteritems():
	two_flag=0
	three_flag=0
	four_flag=0
	for x in value:
		entry = x[:5] #pdb+chain
		if entry not in testing_data:
			domains = cath_dict[entry]
			
			if domains==2 and entry not in two_domain_training and two_flag==0:
				two_domain_training.append(entry)
				two_flag=1
				continue

			elif domains==3 and entry not in three_domain_training and three_flag==0:
				three_domain_training.append(entry)
				three_flag=1
				continue

			elif domains==4 and entry not in four_domain_training and four_flag==0:
				four_domain_training.append(entry)
				four_flag=1
				continue

while len(three_domain_training)!=500:
	key = random.choice(regenerated_cath_dict.keys())
	value = regenerated_cath_dict[key]
	for x in value:
		entry = x[:5]
		domains = cath_dict[entry]
		if entry not in three_domain_training and domains==3:
			three_domain_training.append(entry)
			break

while len(four_domain_training)!=500:
	key = random.choice(regenerated_cath_dict.keys())
	value = regenerated_cath_dict[key]
	for x in value:
		entry = x[:5]
		domains = cath_dict[entry]
		if entry not in four_domain_training and domains==4:
			four_domain_training.append(entry)
			break


two_domain_training.pop()
two_domain_training.pop()
two_domain_training.pop()
two_domain_training.pop()
two_domain_training.pop()

for x in four_domain_training:
	print x
# print len(three_domain_training)
# print len(four_domain_training)


