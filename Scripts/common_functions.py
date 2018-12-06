import math
import re

path_to_pdb_files = 'All PDBs/'

CONTIGUOUS = "Contiguous"
NON_CONTIGUOUS = "Non-Contiguous"
TOTAL = "Total"
CORRECT_CHAINS = "Correct Chains"
TOTAL_CHAINS = "Total Chains"

# This map is very tightly coupled to feature file which has pdb, chain, domains, length, energy, density, radius 
# and it takes that as an input. Example feature file: BenchmarkTwo_Features.csv. This function only returns the index of a
# particular value of interest.
def feature_parser(x):
	return {
		"PDB" : 0,
		"Chain" : 1,
		"Domain" : 2,
		"Length" : 3,
		"Interaction_Energy" : 4,
		"Density" : 5,
		"Radius_Of_Gyration" : 6,
	}[x]

'''
This method opens a given PDB file, reads coordinates for a given chain and returns the coordinates in a list format as follows
[coordinate_residue_1, coordinate_residue_2.....]
where cooredinate_residue_1 is itself a list of x, y & z coordinates as follows: [coordinates_x, coordinates_y, coordinates_z]
'''
def getCoordinatesListFromPDB(pdb, chain):
	pdb_file = open(path_to_pdb_files+pdb+'.pdb','r')
	coordinates_list = []


	while 1:
		data = pdb_file.readline()

		if not data:
			break

		if(data[0]=='E' and data[1]=='N' and data[2]=='D'):
			break

		if(data[0]=='A' and data[1]=='T' and data[2]=='O' and data[21].lower()==chain.lower() and data[13]=='C' and data[14]=='A'):

			val = value_finder(22, 26, data)	
						
			coord_x = float(value_finder(30, 38, data))

			coord_y = float(value_finder(38, 46, data))

			coord_z = float(value_finder(46, 54, data))
		
			if not re.search('[a-zA-Z]+', val):
				coordinates = [coord_x,coord_y,coord_z]
				coordinates_list.append(coordinates)

	return coordinates_list


def value_finder(start_value, end_value, array):

	coordinate = ''

	while array[start_value]==' ':
		start_value = start_value+1



	while int(start_value)!=int(end_value):
		coordinate = coordinate + array[start_value];
		start_value = start_value + 1

	return coordinate

def domainBoundaries(matrix, realId_list, domains):
	new_dict = {}
	for y in range(len(matrix)):
		if matrix[y] in new_dict:
			new_dict[matrix[y]].append(realId_list[y])

		else:
			new_dict[matrix[y]] = [realId_list[y]]

	return new_dict


def isContiguous(cath_boundaries, domains):
	# print cath_boundaries
	cath_boundaries = cath_boundaries.split(" ")
	cath_boundaries = filter(None, cath_boundaries)
	cathDict = {}
	key = 0
	numOFSegments = 1
	x = 0
	counter=0

	while 1:
		if x >= len(cath_boundaries):
			break
		else:
			if counter==domains:
				break
			numOFSegments = int(cath_boundaries[x])
			if numOFSegments > 1:
				return False
			dom = cath_boundaries[x:x+6*numOFSegments+1]
			cathDict[key] = dom
			key+=1
			x+=6*numOFSegments+1
			counter+=1
	return True

def dist(a,b):
	# print a, b
	for x in range(3):
		distance = math.pow((math.pow((a[0]-b[0]),2) + math.pow((a[1]-b[1]),2) + math.pow((a[2]-b[2]),2)), 0.5)
		return distance

def findNumberOfDomains(pdb, chain=None):
	with open('CathDomall', 'r') as f:
		cath_data = f.readlines()
	for x in cath_data:
		if chain!=None:
			if x[0]!='#' and x[:5].lower()==(pdb+chain).lower():
				return int(x[7]+x[8])
		else:
			if x[0]!='#' and x[:5].lower()==pdb.lower():
				return int(x[7]+x[8])


with open("is_Chain_Contiguous_NonContiguous.csv") as f:
	chain_contiguous_or_not_data = f.readlines()

chain_contiguous_or_not_dict = {}

for x in chain_contiguous_or_not_data:
	x = x.split(",")
	chain_contiguous_or_not_dict[x[0].strip()] = x[1].strip();

#This method just takes the chain as input as outputs whether it is contiguous or not. It takes its values from is_Chain_Contiguous_NonContiguous.csv
#chain should be in the format pdb+chain, for example 1norA as input would return 1.
def isChainContigous(chain):
	if chain_contiguous_or_not_dict[chain]=="Contiguous":
		return True
	else:
		return False


'''
This method parses a feature file in JSON format and extract the required features (X) and its corresponding label (Y) which can
be used by a SVM to train/test on. 
features_dictionary => A dictionary which is obtained by reading from a JSON file. 
feature_set => Feature set to be used for training/testing SVM
classification_type => two_class: Single vs multiDomain, multi_class: multiDomain 
'''

def extractFeaturesAndLabelsForSVMFromJson(features_dictionary, feature_set, classification_type):
	X = []
	Y = []

	for key, value in features_dictionary.iteritems():
		pdb = key
		
		label = features_dictionary[key]["Domains"]

		data = []

		for feature in feature_set:
			data.append(features_dictionary[key][feature])

		# print pdb, label, data

		X.append(data)
		Y.append(label)

	return X, Y





'''
This method parses a feature file and extracts the required features (X) and its corresponding label (Y) which can be used
by a SVM to train/test on. 
input_features_list => List of all the features which are calculated and stored in a .csv file. Eg: Benchmark2_features.csv
feature_set => Feature set to be used for training/testing SVM
classification_type => two_class: Single vs multiDomain, multi_class: multiDomain
'''
def extractFeaturesAndLabelsForSVM(input_features_list, feature_set, classification_type):
	X = []
	Y = []

	for input_features in input_features_list:
		input_features = input_features.split(",")
		domains = int(input_features[feature_parser("Domain")].strip())

		if classification_type=="single vs multi-domain":
			if domains > 1:
				label = "multi"
			else:
				label = "single"

		else:
			label = domains

		data = []
		for feature in feature_set:
			data.append(input_features[feature_parser(feature)].strip())

		X.append(data)
		Y.append(label)

	return X, Y

'''
This method takes in a dataset in the format .csv as input. For example, Benchmark2_features.csv and parses the pdb, domain and the 
number of chains to identify the total number of contiguous and non-contiguous chains for each given domain.
dataset => List of all the features which are calculated and stored in a .csv file. Eg: Benchmark2_features.csv
'''
def datasetAnalyser(dataset):
	domains_dictionary = {"Total":{"Contiguous":0, "Non-Contiguous":0, "Total":0}}

	for data in dataset:
		data = data.split(",")
		
		domains = int(data[feature_parser("Domain")].strip())
		PDB = data[feature_parser("PDB")].strip()
		Chain = data[feature_parser("Chain")].strip()

		#Explicitly setting single domain proteins as contiguous to avoid chains with fragments.
		if domains!=1:
			is_chain_contigous = isChainContigous(PDB+Chain)
		else:
			is_chain_contigous = True

		total_dict = domains_dictionary.get("Total")
		total_dict["Total"]+=1

		if is_chain_contigous:
			total_dict["Contiguous"]+=1
		else:
			total_dict["Non-Contiguous"]+=1

		if domains in domains_dictionary:
			domain_dict = domains_dictionary.get(domains)
			domain_dict["Total"]+=1
			if is_chain_contigous:
				domain_dict["Contiguous"]+=1
			else:
				domain_dict["Non-Contiguous"]+=1
			
		else:
			if is_chain_contigous:
				domains_dictionary[domains] = {"Contiguous":1, "Non-Contiguous":0, "Total":1}
			else:
				domains_dictionary[domains] = {"Contiguous":0, "Non-Contiguous":1, "Total":1}

	return domains_dictionary

'''
This method analyses the performance of the SVM by calling datasetAnalyser on the set of correctly labelled chains
and on the entire input test dataset.
correctly_labelled_chains => List of all the CORRECTLY IDENTIFIED CHAINS and their features which are calculated and stored in a .csv file.
test_dataset => Complete test dataset which was given as an input to the SVM. Eg. Benchmark2_features.csv
classification_type => two_class: Single vs multiDomain, multi_class: multiDomain
'''
def SVM_Performance_Analyser(correctly_labelled_chains, test_dataset, classification_type):
	correctly_labelled_chains_dictionary = datasetAnalyser(correctly_labelled_chains)
	test_dataset_dictionary = datasetAnalyser(test_dataset)

	SVM_performance_dictionary = {"Total":{}, "Contiguous":{}, "Non-Contiguous":{}}

	# if classification_type=="single vs multi-domain":
	# 	SVM_performance_dictionary.get("Total") = {"Single":{"Correct":0, "Total":0, "Accuracy":0.00}, "Multi":{"Correct":0, "Total":0, "Accuracy":0.00}}

	for key, correct_value in correctly_labelled_chains_dictionary.iteritems():

		#Evaluating the overall performance for a particular key(Domain)
		total_performance_dict = SVM_performance_dictionary["Total"]
		total_performance_dict[key] = {} 
		total_performance_dict[key]["Correct"] = correctly_labelled_chains_dictionary[key]["Total"]
		total_performance_dict[key]["Total"] = test_dataset_dictionary[key]["Total"]
		if total_performance_dict[key]["Total"]!=0:
			total_performance_dict[key]["Accuracy"] = "{0:.2f}".format((total_performance_dict[key]["Correct"]*100)/total_performance_dict[key]["Total"])

		#Evaluating the performance on Contiguous chains for a particular key(Domain)
		contiguous_performance_dict = SVM_performance_dictionary["Contiguous"]
		contiguous_performance_dict[key] = {}
		contiguous_performance_dict[key]["Correct"] = correctly_labelled_chains_dictionary[key]["Contiguous"]
		contiguous_performance_dict[key]["Total"] = test_dataset_dictionary[key]["Contiguous"]
		if contiguous_performance_dict[key]["Total"]!=0:
			contiguous_performance_dict[key]["Accuracy"] = "{0:.2f}".format((contiguous_performance_dict[key]["Correct"]*100)/contiguous_performance_dict[key]["Total"])


		#Evaluating the performance on Non-Contiguous chains for a particular key(Domain)
		non_contiguous_performance_dict = SVM_performance_dictionary["Non-Contiguous"]
		non_contiguous_performance_dict[key] = {}
		non_contiguous_performance_dict[key]["Correct"] = correctly_labelled_chains_dictionary[key]["Non-Contiguous"]
		non_contiguous_performance_dict[key]["Total"] = test_dataset_dictionary[key]["Non-Contiguous"]
		if non_contiguous_performance_dict[key]["Total"]!=0:
			non_contiguous_performance_dict[key]["Accuracy"] = "{0:.2f}".format((non_contiguous_performance_dict[key]["Correct"]*100)/non_contiguous_performance_dict[key]["Total"])

	if classification_type=="single vs multi-domain":
		new_dict = {"Contiguous":{}, "Non-Contiguous":{}, "Total":{}}
		for key, value in SVM_performance_dictionary.iteritems():

			new_dict[key]["Single"] = {"Correct":0, "Total":0}
			new_dict[key]["Multi"] = {"Correct":0, "Total":0}
			new_dict[key]["Total"] = {"Correct":0, "Total":0}

			for key1, value1 in value.iteritems():
				if key1==1:
					new_dict[key]["Single"]["Correct"]+=SVM_performance_dictionary[key][key1]["Correct"]
					new_dict[key]["Single"]["Total"]+=SVM_performance_dictionary[key][key1]["Total"]
					if new_dict[key]["Single"]["Total"]!=0:
						new_dict[key]["Single"]["Accuracy"] = "{0:.2f}".format((new_dict[key]["Single"]["Correct"]*100.0)/new_dict[key]["Single"]["Total"])

				elif key1!="Total":
					new_dict[key]["Multi"]["Correct"]+=SVM_performance_dictionary[key][key1]["Correct"]
					new_dict[key]["Multi"]["Total"]+=SVM_performance_dictionary[key][key1]["Total"]
					if new_dict[key]["Multi"]["Total"]!=0:
						new_dict[key]["Multi"]["Accuracy"] = "{0:.2f}".format((new_dict[key]["Multi"]["Correct"]*100.0)/new_dict[key]["Multi"]["Total"])

				elif key1=="Total":
					new_dict[key]["Total"]["Correct"]+=SVM_performance_dictionary[key][key1]["Correct"]
					new_dict[key]["Total"]["Total"]+=SVM_performance_dictionary[key][key1]["Total"]
					if new_dict[key]["Total"]["Total"]!=0:
						new_dict[key]["Total"]["Accuracy"] = "{0:.2f}".format((new_dict[key]["Total"]["Correct"]*100.0)/new_dict[key]["Total"]["Total"])



	print
	for key, value in sorted(new_dict.iteritems()):
		print key
		for a, b in sorted(value.iteritems()):
			print a, b
		print
	print

'''
This method evaluates the performance of multi-domain classification done by the SVM. 
This method invokes the underlying method multi_domain_dataset_analyzer which creates a dictionary in the following format
{
	{1} : {
		{Contiguous}" : <no. of contiguous chains>
		{Non-Contiguous} : <no. of non-contiguous chains>
		{Total} : <no. of total chanis>
	}
	{2} : {
		{Contiguous}" : <no. of contiguous chains>
		{Non-Contiguous} : <no. of non-contiguous chains>
		{Total} : <no. of total chanis>
	}
	.
	.
	.
}
The same is done for both test dataset and correctly labelled chains to get the overall accuracy 
for each n-domain protein across all contiguous/non-contiguous/total factors.
'''
def SVM_Multi_Domain_Performance_Analyser(correctly_labelled_chains, test_dataset_chains):
	analyzed_test_dataset =  multi_domain_dataset_analyzer(test_dataset_chains)
	analyzed_correctly_labelled_chains = multi_domain_dataset_analyzer(correctly_labelled_chains)


	print
	print


	print "Analyzed Test Dataset"
	print analyzed_test_dataset
	print
	print

	print "Analyzed Correctly Predicted Data"
	print analyzed_correctly_labelled_chains

	print
	print

	results_dict = {}
	overall_results_dict = {CORRECT_CHAINS : {CONTIGUOUS : 0, NON_CONTIGUOUS : 0, TOTAL : 0}, TOTAL_CHAINS : {CONTIGUOUS : 0, NON_CONTIGUOUS : 0, TOTAL : 0}}




	for key, value in analyzed_correctly_labelled_chains.iteritems():
		results_dict[key] = {}

		for key_1, value_1 in value.iteritems():
			data_test = analyzed_test_dataset[key][key_1]
			data_correctly_labelled =  analyzed_correctly_labelled_chains[key][key_1]

			if (data_test) != 0:
				accuracy = "{0:.2f}".format((100.0*data_correctly_labelled)/data_test)

				results_dict[key][key_1] = "(" + str(data_correctly_labelled) + "/" + str(data_test) + ")" + " " + accuracy + "%"

				overall_results_dict[CORRECT_CHAINS][key_1]+=data_correctly_labelled
				overall_results_dict[TOTAL_CHAINS][key_1]+=data_test


	for key, value in sorted(results_dict.iteritems()):
		print key
		for key_1, value_1 in sorted(value.iteritems()):
			print key_1, value_1
		print

	print 
	print "Overall Results"

	for value_1 in overall_results_dict.values():
		for key, value in value_1.iteritems():
			print key,
			data_correctly_labelled = overall_results_dict[CORRECT_CHAINS][key]
			data_test = overall_results_dict[TOTAL_CHAINS][key]
			accuracy = "{0:.2f}".format((100.0*data_correctly_labelled)/data_test)

			print "(" + str(data_correctly_labelled) + "/" + str(data_test) + ")" + " " + accuracy + "%"

		break





def multi_domain_dataset_analyzer(dataset):
	analyzed_data_dict = {}

	for chain in dataset:
		domains = findNumberOfDomains(chain)

		if domains not in analyzed_data_dict:
			analyzed_data_dict[domains] = {CONTIGUOUS : 0, NON_CONTIGUOUS : 0, TOTAL : 0}

		isContiguous = isChainContigous(chain)

		if isContiguous:
			# if CONTIGUOUS not in analyzed_data_dict[domains]:
				# analyzed_data_dict[domains][CONTIGUOUS] = 1
			# else:
			analyzed_data_dict[domains][CONTIGUOUS]+=1
		else:
			# if NON_CONTIGUOUS not in analyzed_data_dict[domains]:
				# analyzed_data_dict[domains][NON_CONTIGUOUS] = 1
			# else:
			analyzed_data_dict[domains][NON_CONTIGUOUS]+=1

		# if TOTAL not in analyzed_data_dict[domains]:
			# analyzed_data_dict[domains][TOTAL] = 1
		# else:
		analyzed_data_dict[domains][TOTAL]+=1

	return analyzed_data_dict









