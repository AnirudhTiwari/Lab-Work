# This program classifies single from multi domain chains by cross validation. Cross validation is used as the 
# number of single domain proteins is almost the same as multi domain proteins. Thus it takes the original Testing dataset
# of around 1300 chains as an input and performs predictions.

# Update: Instead of cross validation, I have created a training dataset consisting of 1500 chains to be used multi-domain
# training dataset consisting of 1500 chains.

#Uncomment the relevant sections to train/test.
from sklearn import svm
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import StratifiedKFold
import common_functions as utils

data_dict = {} # A dictionary to hold (PDB,chain,domains)  => [length, energy, density, radius] mapping


#Using the test dataset as training dataset and Benchmark_2/Benchmark_3 as testing dataset.
# with open("single_test_length_energy_density_radius.csv") as f:
# 	single_train_data = f.readlines()

#Using the newly constructed balanced training dataset consisting of 1500(1498) single chains
with open("single_training_features.csv") as f:
	single_train_data = f.readlines()

#Using the newly constructed balanced training dataset consisting of 1500(1499) multi domain chains
with open("multi_balanced_training_dataset_length_energy_density_radius.csv") as f:
	multi_train_data = f.readlines()

# with open("multi_test_length_energy_density_radius.csv") as f:
# 	multi_train_data = f.readlines()

# Testing on BenchmarkTwo Dataset
# with open("BenchmarkTwo_Features.csv") as f:
# 	final_test_data = f.readlines()

# Testing on BenchmarkThree Dataset
# with open("BenchmarkThree_Features.csv") as f:
# 	final_test_data = f.readlines()

# Testing on self created dataset
with open("single_test_length_energy_density_radius.csv") as f:
	single_test_data = f.readlines()

with open("multi_test_length_energy_density_radius.csv") as f:
	multi_test_data = f.readlines()

final_test_data = single_test_data + multi_test_data

# with open("multi_non_contiguous_length_energy_density_radius_correct.csv") as f:
# 	multi_test_data_non_contiguous = f.readlines()

# with open("multi_contiguous_length_energy_density_radius_correct.csv") as f:
# 	multi_test_data_contiguous = f.readlines()


single_chains_total = 0
multi_chains_total = 0
single_correct = 0
multi_correct = 0
total_correct = 0

def prepareData(final_data, data_type):

	X = []
	Y = []

	single_chains=0
	two_chains=0
	three_chains=0
	four_chains=0
	five_chains=0
	six_chains=0

	two_contiguous = 0
	three_contiguous = 0
	four_contiguous = 0

	two_non_contiguous = 0
	three_non_contiguous = 0
	four_non_contiguous = 0

	training_contiguous_counter = 0

	global single_chains_total
	global multi_chains_total
	
	for x in final_data:
		x = x.split(",")
		pdb = x[0].strip()
		chain = x[1].strip()
		domains = int(x[2].strip())
		length = int(x[3].strip())
		energy = float(x[4].strip())
		density = float(x[5].strip())
		radius = float(x[6].strip())

		value = [length,energy,density,radius]

		if data_type=="test":
			data_dict[(pdb,chain,domains)] = value
			if domains==1:
				single_chains+=1
			if domains==2:
				two_chains+=1
			if domains==3:
				three_chains+=1
			if domains==4:
				four_chains+=1
			if domains==5:
				# print pdb+chain
				five_chains+=1
			if domains==6:
				# print pdb+chain
				six_chains+=1



		# data_dict[(pdb,chain,domains)] = value

		X.append(value)

		if domains==1:
			Y.append('Single')
			if data_type=="test":
				single_chains_total+=1
			
		else:
			Y.append('Multi')
			if data_type=="test":
				if domains == 2:
					if utils.isChainContigous(pdb+chain):
						two_contiguous+=1
					else:
						two_non_contiguous+=1

				if domains == 3:
					if utils.isChainContigous(pdb+chain):
						three_contiguous+=1
					else:
						three_non_contiguous+=1

				if domains == 4:
					if utils.isChainContigous(pdb+chain):
						four_contiguous+=1
					else:
						four_non_contiguous+=1

				multi_chains_total+=1
			else:
				if utils.isChainContigous(pdb+chain):
					training_contiguous_counter+=1
				

	print "Total Chains", single_chains, two_chains, three_chains, four_chains, five_chains, six_chains
	print "Contiguous Chains", two_contiguous, three_contiguous, four_contiguous
	print "NonContigu Chains", two_non_contiguous, three_non_contiguous, four_non_contiguous
	print "Contiguous training chains", training_contiguous_counter
	return X,Y

def printDictionaryData(key):
	list_A = list(key)
	list_B = list(data_dict[key])
	list_C = list_A + list_B
	print ', '.join(str(o) for o in list_C)

# final_data = single_test_data + multi_test_data_contiguous + multi_test_data_non_contiguous
final_train_data = single_train_data+multi_train_data

X_train, y_train = prepareData(final_train_data, "train")
X_test, y_test = prepareData(final_test_data, "test")
kernel = 'linear'
clf = svm.SVC(kernel=kernel, class_weight='balanced')

print "Training data => ", len(X_train), len(y_train)
print "Testing data => ", len(X_test), len(y_test)
clf = svm.SVC().fit(X_train,y_train)

#Please uncomment the following code snippet when using cross validation on our created dataset. Else, use the below for benchmark 2 and 3.
# final_data = single_test_data + multi_test_data
# X, Y = prepareData(final_data)

# skf = StratifiedKFold(n_splits=10)
# clf = svm.SVC(kernel='linear', class_weight='balanced')

# predicted_data = cross_val_predict(clf, X, Y, cv=skf)

# for x in range(0, len(X)):
	
# 	value = X[x]
# 	predicted_label = predicted_data[x]
# 	actual_label = Y[x]
	
# 	dict_key = data_dict.keys()[data_dict.values().index(value)]

multi_contiguous_correct = 0
multi_non_contiguous_correct = 0

multi_contiguous_total = 0
multi_non_contiguous_total = 0

for x in range(0, len(X_test)):

	value = X_test[x]
	predicted_label = clf.predict([value])[0]
	actual_label = y_test[x]
	dict_key = data_dict.keys()[data_dict.values().index(value)]
	
	pdb = dict_key[0]
	chain = dict_key[1]

	if actual_label=='Multi':
		if utils.isChainContigous(pdb+chain):
			multi_contiguous_total+=1
		else:
			multi_non_contiguous_total+=1

	if predicted_label==actual_label:
		if actual_label=='Single':
			single_correct+=1
		else:
			if utils.isChainContigous(pdb+chain):
				multi_contiguous_correct+=1
			else:
				multi_non_contiguous_correct+=1
			# printDictionaryData(dict_key)
			multi_correct+=1
		total_correct+=1
	else:
		if actual_label=='Single':
			printDictionaryData(dict_key)
			# print pdb, chain, value



print "Single Correct => ", single_correct, "Total => ", single_chains_total, "Accuracy => ", '{0:.2f}'.format(single_correct*100.0/single_chains_total)+"%"
print "Multi Correct => ", multi_correct, "Total => ", multi_chains_total, "Accuracy => ", '{0:.2f}'.format(multi_correct*100.0/multi_chains_total)+"%"

print "Multi Contiguous Correct => ", multi_contiguous_correct, "Total Multi Contiguous => ", multi_contiguous_total, "Accuracy => ", '{0:.2f}'.format(multi_contiguous_correct*100.0/multi_contiguous_total)+"%"
print "Multi Non Contiguous Correct => ", multi_non_contiguous_correct, "Total Multi Non Contiguous => ", multi_non_contiguous_total, "Accuracy => ", '{0:.2f}'.format(multi_non_contiguous_correct*100.0/multi_non_contiguous_total)+"%"

# print "Total Correct => ", total_correct, "Total => ", len(X_test), "Accuracy => ",  '{0:.2f}'.format(total_correct*100.0/len(X_test))+"%"







