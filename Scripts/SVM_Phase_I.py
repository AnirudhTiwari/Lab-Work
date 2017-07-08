# This program classifies single from multi domain chains by cross validation. Cross validation is used as the 
# number of single domain proteins is almost the same as multi domain proteins. Thus it takes the original Testing dataset
# of around 1300 chains as an input and performs predictions.

from sklearn import svm
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import StratifiedKFold

data_dict = {} # A dictionary to hold (PDB,chain,domains)  => [length, energy, density, radius] mapping

with open("single_length_energy_density_radius_correct.csv") as f:
	single_test_data = f.readlines()

with open("multi_non_contiguous_length_energy_density_radius_correct.csv") as f:
	multi_test_data_non_contiguous = f.readlines()

with open("multi_contiguous_length_energy_density_radius_correct.csv") as f:
	multi_test_data_contiguous = f.readlines()

single_chains_total = 0
multi_chains_total = 0
single_correct = 0
multi_correct = 0
total_correct = 0

def prepareData(final_data):

	X = []
	Y = []

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
		data_dict[(pdb,chain,domains)] = value

		X.append(value)

		if domains==1:
			Y.append('Single')
			single_chains_total+=1
			
		else:
			Y.append('Multi')
			multi_chains_total+=1

	return X,Y

def printDictionaryData(key):
	list_A = list(key)
	list_B = list(data_dict[key])
	list_C = list_A + list_B
	print ', '.join(str(o) for o in list_C)

final_data = single_test_data + multi_test_data_contiguous + multi_test_data_non_contiguous

X, Y = prepareData(final_data)

skf = StratifiedKFold(n_splits=10)
clf = svm.SVC(kernel='linear', class_weight='balanced')

predicted_data = cross_val_predict(clf, X, Y, cv=skf)

for x in range(0, len(X)):
	
	value = X[x]
	predicted_label = predicted_data[x]
	actual_label = Y[x]
	
	dict_key = data_dict.keys()[data_dict.values().index(value)]


	if predicted_label==actual_label:
		if actual_label=='Single':
			single_correct+=1
		else:
			printDictionaryData(dict_key)
			multi_correct+=1
		total_correct+=1

# print "Accuracy => ", '{0:.2f}'.format(total_correct*100.0/len(X))

# print "Single Correct", single_correct, single_chains_total, '{0:.2f}'.format(single_correct*100.0/single_chains_total)
# print "Multi Correct", multi_correct, multi_chains_total, '{0:.2f}'.format(multi_correct*100.0/multi_chains_total)








