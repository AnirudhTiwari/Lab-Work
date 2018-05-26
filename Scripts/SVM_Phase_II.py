# This is the final file which is used to traing the SVM on the given training dataset. The training dataset needs to be in a .csv format.
# Please look at the file multi_balanced_training_dataset_energy_length_radius_density.csv for the format. Upon learning from the input training
# dataset, it tests on the given input test dataset which is to be in the same format as above.

from sklearn import svm
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import StratifiedKFold
from sklearn import metrics
import common_functions as utils

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
with open("correct_selfDataset_postPhaseI_v2.csv") as f:
	final_test_data = f.readlines()

#Benchmark 2 to be used as test
# with open("correct_Benchmark2_Dataset_PostPhaseOne.csv") as f:
# 	final_test_data = f.readlines()

# with open("correct_Benchmark2_Dataset_PostPhaseOne_v2.csv") as f:
# 	final_test_data = f.readlines()

#Benchmark 3 to be used as test
# with open("correct_Benchmark3_Dataset_PostPhaseOne.csv") as f:
# 	final_test_data = f.readlines()

# with open("correct_Benchmark3_Dataset_PostPhaseOne_v2.csv") as f:
# 	final_test_data = f.readlines()

with open("multi_balanced_training_dataset_length_energy_density_radius.csv") as f:
	final_train_data = f.readlines()

# X_train, y_train = resampleData(final_train_data, "train")
# X_test, y_test = resampleData(final_test_data, "test")

# Performing cross validation on the training dataset of 1500 multi-domain proteins(500 2-domain, 500 3-domain, 500 4-domain).
X_test, y_test = resampleData(final_train_data, "test")


# kernel = 'linear'
# clf = svm.SVC(kernel=kernel, class_weight='balanced')

# print "Training data => ", len(X_train), len(y_train)
# print "Testing data => ", len(X_test), len(y_test)
# clf = svm.SVC().fit(X_train,y_train)


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

two_contiguous = 0
two_non_contiguous = 0
two_contiguous_correct = 0
two_non_contiguous_correct = 0

three_contiguous = 0
three_non_contiguous = 0
three_contiguous_correct = 0
three_non_contiguous_correct = 0

four_contiguous = 0
four_non_contiguous = 0
four_contiguous_correct = 0
four_non_contiguous_correct = 0


print "Length of X_test", len(X_test)
print "Length of y_test", len(y_test)

skf = StratifiedKFold(n_splits=10)
clf = svm.SVC(kernel='linear', class_weight='balanced')

predicted_data = cross_val_predict(clf, X_test, y_test, cv=skf)


for x in range(0, len(X_test)):

	value = X_test[x]
	# predicted_label = clf.predict([value])[0]
	predicted_label = predicted_data[x]
	
	actual_label = int(y_test[x])
	dict_key = test_data_dict.keys()[test_data_dict.values().index(value)]

	pdb = dict_key[0]
	chain = dict_key[1]

	if actual_label==2:
		if utils.isChainContigous(pdb+chain):
			two_contiguous+=1
		else:
			two_non_contiguous+=1

	elif actual_label==3:
		if utils.isChainContigous(pdb+chain):
			three_contiguous+=1
		else:
			three_non_contiguous+=1

	elif actual_label==4:
		if utils.isChainContigous(pdb+chain):
			four_contiguous+=1
		else:
			four_non_contiguous+=1		
		

	if predicted_label==actual_label:
		if actual_label==1:
			single_correct+=1

		elif actual_label==2:
			two_correct+=1
			if utils.isChainContigous(pdb+chain):
				two_contiguous_correct+=1
			else:
				two_non_contiguous_correct+=1

		elif actual_label==3:
			three_correct+=1
			if utils.isChainContigous(pdb+chain):
				three_contiguous_correct+=1
			else:
				three_non_contiguous_correct+=1

		elif actual_label==4:
			four_correct+=1
			if utils.isChainContigous(pdb+chain):
				four_contiguous_correct+=1
			else:
				four_non_contiguous_correct+=1

		total_correct+=1
		print (dict_key[0]+dict_key[1]).lower()

print "Two Correct => ", two_correct, "Total => ", two_chains, "Accuracy => ", '{0:.2f}'.format(two_correct*100.0/two_chains)
print "Three Correct => ", three_correct, "Total => ", three_chains, "Accuracy => ", '{0:.2f}'.format(three_correct*100.0/three_chains)
print "Four Correct => ", four_correct, "Total => ", four_chains, "Accuracy => ", '{0:.2f}'.format(four_correct*100.0/four_chains)
print	
print "Total Correct => ", total_correct, "Total => ", len(X_test), "Overall Accuracy =>", '{0:.2f}'.format(total_correct*100.0/len(X_test))
print

print "Two Contiguous Correct => ", two_contiguous_correct, "Total Two Contiguous => ", two_contiguous, "Accuracy => ", '{0:.2f}'.format(two_contiguous_correct*100.0/two_contiguous)
print "Three Contiguous Correct => ", three_contiguous_correct, "Total Three Contiguous => ", three_contiguous, "Accuracy => ", '{0:.2f}'.format(three_contiguous_correct*100.0/three_contiguous)
print "Four Contiguous Correct => ", four_contiguous_correct, "Total Four Contiguous => ", four_contiguous, "Accuracy => ", '{0:.2f}'.format(four_contiguous_correct*100.0/four_contiguous)
print
print "Total Contiguous Correct => ", two_contiguous_correct+three_contiguous_correct+four_contiguous_correct, "Total Contiguous", two_contiguous+three_contiguous+four_contiguous, "Accuracy => ", '{0:.2f}'.format((two_contiguous_correct+three_contiguous_correct+four_contiguous_correct)*100.0/(two_contiguous+three_contiguous+four_contiguous))
print
print "Two Non-Contiguous Correct => ", two_non_contiguous_correct, "Total Two Non-Contiguous => ", two_non_contiguous, "Accuracy => ", '{0:.2f}'.format(two_non_contiguous_correct*100.0/two_non_contiguous)
print "Three Non-Contiguous Correct => ", three_non_contiguous_correct, "Total Three Non-Contiguous => ", three_non_contiguous, "Accuracy => ", '{0:.2f}'.format(three_non_contiguous_correct*100.0/three_non_contiguous)
print "Four Non-Contiguous Correct => ", four_non_contiguous_correct, "Total Four Contiguous => ", four_non_contiguous, "Accuracy => ", '{0:.2f}'.format(four_non_contiguous_correct*100.0/four_non_contiguous)
print
print "Total Non-Contiguous Correct => ", two_non_contiguous_correct+three_non_contiguous_correct+four_non_contiguous_correct, "Total Non-Contiguous", two_non_contiguous+three_non_contiguous+four_non_contiguous, "Accuracy => ", '{0:.2f}'.format((two_non_contiguous_correct+three_non_contiguous_correct+four_non_contiguous_correct)*100.0/(two_non_contiguous+three_non_contiguous+four_non_contiguous))
print

















