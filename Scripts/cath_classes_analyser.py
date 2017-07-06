import ast

with open('cath_classes_copy.txt') as f:
	cath_classes = f.readlines()

with open('training_multi_domain_dataset.csv') as f:
	training_dataset = f.readlines()

with open('multi_contiguous_length_energy_density_radius_correct.csv') as f:
	testing_dataset_contiguous = f.readlines()

with open('multi_non_contiguous_length_energy_density_radius_correct.csv') as f:
	testing_dataset_non_contiguous = f.readlines()

testing_dataset = testing_dataset_contiguous + testing_dataset_non_contiguous

regenerated_cath_dict = {}

def getPdbChainAndDomainFromData(data):
	temp = []
	for x in data:
		x = x.split(',')
		pdb = x[0].strip()
		chain = x[1].strip().lower()
		domain = x[2].strip()
		temp.append(pdb+chain+domain)
	return temp

def getCathClassFromCathValue(cath_value):
	for key, values in regenerated_cath_dict.iteritems():
		if cath_value in values:
			return key


def getClassesForGivenChain(chain):

	classes = []
	for key,values in regenerated_cath_dict.iteritems():
		for x in values:
			if chain in x:
				classes.append(key)

	return classes

#For say training dataset, it creates a map of the class and how many times it is represented for given 2 domain proteins.
# # def getClassRepresentationForGivenDomainsAndDataset(dataset, domains):

# 	if domains==2:
# 		domains="two"
# 	elif domains==3:
# 		domains="three"
# 	else:
# 		domains=="four"








for x in cath_classes:
	y = x.partition("=")
	cath_class = ast.literal_eval(y[0])
	cath_domains = ast.literal_eval(y[2])
	regenerated_cath_dict[cath_class]=cath_domains

training_dataset_final = getPdbChainAndDomainFromData(training_dataset)
testing_dataset_final = getPdbChainAndDomainFromData(testing_dataset)

two_domain_training_classes_represented = {}
three_domain_training_classes_represented = {}
four_domain_training_classes_represented = {}


two_domain_testing_classes_represented = {}
three_domain_testing_classes_represented = {}
four_domain_testing_classes_represented = {}


for x in testing_dataset_final:
	chain = x[:5]
	domains = int(x[5])
	classes = getClassesForGivenChain(chain)
	# print chain, domains, classes

	if domains==2:
		for x in classes:
			if x not in two_domain_testing_classes_represented:
				two_domain_testing_classes_represented[x]=[chain]
			else:
				if chain not in two_domain_testing_classes_represented[x]:
					two_domain_testing_classes_represented[x].append(chain)


	elif domains==3:
		for x in classes:
			if x not in three_domain_testing_classes_represented:
				three_domain_testing_classes_represented[x]=[chain]
			else:
				if chain not in three_domain_testing_classes_represented[x]:
					three_domain_testing_classes_represented[x].append(chain)

	else:
		for x in classes:
			if x not in four_domain_testing_classes_represented:
				four_domain_testing_classes_represented[x]=[chain]
			else:
				if chain not in four_domain_testing_classes_represented[x]:
					four_domain_testing_classes_represented[x].append(chain)


# two_domain_testing_classes_represented = set(two_domain_testing_classes_represented)
# three_domain_testing_classes_represented = set(three_domain_testing_classes_represented)
# four_domain_testing_classes_represented = set(four_domain_testing_classes_represented)

for x in training_dataset_final:
	chain = x[:5]
	domains = int(x[5])
	classes = getClassesForGivenChain(chain)
	# print chain, domains, classes

	if domains==2:
		for x in classes:
			if x not in two_domain_training_classes_represented:
				two_domain_training_classes_represented[x]=[chain]
			else:
				if chain not in two_domain_training_classes_represented[x]:
					two_domain_training_classes_represented[x].append(chain)


	elif domains==3:
		for x in classes:
			if x not in three_domain_training_classes_represented:
				three_domain_training_classes_represented[x]=[chain]
			else:
				if chain not in three_domain_training_classes_represented[x]:
					three_domain_training_classes_represented[x].append(chain)

	else:
		for x in classes:
			if x not in four_domain_training_classes_represented:
				four_domain_training_classes_represented[x]=[chain]
			else:
				if chain not in four_domain_training_classes_represented[x]:
					four_domain_training_classes_represented[x].append(chain)

counter=0
for key, values in two_domain_training_classes_represented.iteritems():
	# print key, values
	counter+=len(values)

print counter

# for key,values in four_domain_testing_classes_represented.iteritems():
# 	if key not in four_domain_training_classes_represented:
# 		print key, values

# two_domain_training_classes_represented = set(two_domain_training_classes_represented)
# three_domain_training_classes_represented = set(three_domain_training_classes_represented)
# four_domain_training_classes_represented = set(four_domain_training_classes_represented)


# two_not_intersected_set = two_domain_testing_classes_represented.symmetric_difference(two_domain_training_classes_represented)
# three_not_intersected_set = three_domain_testing_classes_represented.symmetric_difference(three_domain_training_classes_represented)
# four_not_intersected_set = four_domain_testing_classes_represented.symmetric_difference(four_domain_training_classes_represented)


# testing_dataset_pdb_chain = []

# for z in testing_dataset:
# 	z = z.split(",")
# 	pdb = z[0].strip()
# 	chain = z[1].strip().lower()
# 	testing_dataset_pdb_chain.append(pdb+chain)

# # print testing_dataset_pdb_chain

# not_represented_chains = []

# for x in two_not_intersected_set:
# 	pdbs = regenerated_cath_dict[x]
# 	modified_pdbs = []
# 	for y in pdbs:
# 		modified_pdbs.append(y[:5])

# 	for a in testing_dataset_pdb_chain:
# 		for b in modified_pdbs:
# 			if a==b and a not in not_represented_chains:
# 				not_represented_chains.append(a)

# for x in three_not_intersected_set:
# 	pdbs = regenerated_cath_dict[x]
# 	modified_pdbs = []
# 	for y in pdbs:
# 		modified_pdbs.append(y[:5])

# 	for a in testing_dataset_pdb_chain:
# 		for b in modified_pdbs:
# 			if a==b and a not in not_represented_chains:
# 				not_represented_chains.append(a)


# for x in four_not_intersected_set:
# 	pdbs = regenerated_cath_dict[x]
# 	modified_pdbs = []
# 	for y in pdbs:
# 		modified_pdbs.append(y[:5])

# 	for a in testing_dataset_pdb_chain:
# 		for b in modified_pdbs:
# 			if a==b and a not in not_represented_chains:
# 				not_represented_chains.append(a)




# print two_not_intersected_set
# print 
# print 
# print three_not_intersected_set
# print
# print
# print four_not_intersected_set

# print len(three_domain_testing_classes_represented)
# print len(four_domain_testing_classes_represented)


# print len(two_domain_training_classes_represented)
# print len(three_domain_training_classes_represented)
# print len(four_domain_training_classes_represented)
# 	elif domains==3:
# 		three_domain_testing_classes_represented.add(classes)
# 	else:
# 		four_domain_testing_classes_represented.add(classes)
	

# print two_domain_testing_classes_represented
# 	# domains_testing = x[-2:]

	# testing_cath_class = getCathClassFromCathValue(x)
	
	# flag = 0
	

	# print  int(domains_testing),",",testing_cath_class,",", 

	# if not testing_cath_class:
	# 	print x
	# 	continue

	# num_of_times_represented = 0

	# for y in training_dataset_final:
	# 	domains_training = y[-2:]
	# 	if domains_training==domains_testing:
	# 		trainining_cath_class = getCathClassFromCathValue(y)
	# 		if trainining_cath_class == testing_cath_class:
	# 			num_of_times_represented+=1

	# if num_of_times_represented==0:
	# 	print x, ",", num_of_times_represented

	# else:
	# 	print num_of_times_represented




	# print testing_cath_class


