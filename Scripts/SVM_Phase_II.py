# This is the final file which is used to traing the SVM on the given training dataset. The training dataset needs to be in a .csv format.
# Please look at the file multi_balanced_training_dataset_energy_length_radius_density.csv for the format. Upon learning from the input training
# dataset, it tests on the given input test dataset which is to be in the same format as above.

from sklearn import svm
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import StratifiedKFold


total_correct = 0

single_correct = 0
two_correct = 0
three_correct = 0
four_correct = 0

single_chains = 0
two_chains = 0
three_chains = 0
four_chains = 0

test_data_dict = {} # A dictionary to hold (PDB,chain,domains)  => [length, energy, density, radius] mapping


def resampleData(final_data, data_type):
	resampling_factor = 1
	single_data = []
	two_data = []
	three_data = []
	four_data = []
	X = []
	Y = []
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
			test_data_dict[(pdb,chain,domains)] = value

		if domains==1:
			single_data.append(value)
		elif domains==2:
			two_data.append(value)
		elif domains==3:
			three_data.append(value)
		else:
			four_data.append(value)

		X.append(value)
		Y.append(domains)

	return X,Y

# Self created dataset
with open("self_dataset_multi_non_contiguous.csv") as f:
	final_test_data = f.readlines()


#Benchmark 2 to be used as test
# with open("correct_Benchmark2_Dataset_PostPhaseOne.csv") as f:
# 	final_test_data = f.readlines()
	
#Benchmark 3 to be used as test
# with open("correct_Benchmark3_Dataset_PostPhaseOne.csv") as f:
# 	final_test_data = f.readlines()

with open("multi_balanced_training_dataset_length_energy_density_radius.csv") as f:
	final_train_data = f.readlines()

X_train, y_train = resampleData(final_train_data, "train")
X_test, y_test = resampleData(final_test_data, "test")

kernel = 'linear'
clf = svm.SVC(kernel=kernel, class_weight='balanced')

# print "Training data => ", len(X_train), len(y_train)
# print "Testing data => ", len(X_test), len(y_test)
clf = svm.SVC().fit(X_train,y_train)

for y in y_test:
	label = int(y)
	if label==1:
		single_chains+=1
	if label==2:
		two_chains+=1
	if label==3:
		three_chains+=1
	if label==4:
		four_chains+=1
	if label==5:
		five_chains+=1
	if label==6:
		six_chains+=1

for x in range(0, len(X_test)):

	value = X_test[x]
	predicted_label = clf.predict([value])[0]
	actual_label = int(y_test[x])
	dict_key = test_data_dict.keys()[test_data_dict.values().index(value)]

	if predicted_label==actual_label:
		if actual_label==1:
			single_correct+=1
		elif actual_label==2:
			two_correct+=1
		elif actual_label==3:
			three_correct+=1
		elif actual_label==4:
			four_correct+=1
		total_correct+=1
		print (dict_key[0]+dict_key[1]).lower()

print "Two Correct => ", two_correct, "Total => ", two_chains, "Accuracy => ", '{0:.2f}'.format(two_correct*100.0/two_chains)
print "Three Correct => ", three_correct, "Total => ", three_chains, "Accuracy => ", '{0:.2f}'.format(three_correct*100.0/three_chains)
print "Four Correct => ", four_correct, "Total => ", four_chains, "Accuracy => ", '{0:.2f}'.format(four_correct*100.0/four_chains)
	
print "Total Correct => ", total_correct, "Overall Accuracy =>", '{0:.2f}'.format(total_correct*100.0/len(X_test))
