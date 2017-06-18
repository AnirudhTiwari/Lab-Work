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

data_dict = {} # A dictionary to hold (PDB,chain,domains)  => [length, energy, density, radius] mapping


def resampleData(final_data):
	
	resampling_factor = 1
	single_data = []
	two_data = []
	three_data = []
	four_data = []

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

		if domains==1:
			single_data.append(value)
		elif domains==2:
			two_data.append(value)
		elif domains==3:
			three_data.append(value)
		else:
			four_data.append(value)

	# print len(single_data), resampling_factor*len(two_data), resampling_factor*len(three_data), resampling_factor*len(four_data)
	X = single_data + resampling_factor*two_data + resampling_factor*three_data + resampling_factor*four_data
	Y = len(single_data)*[1] + resampling_factor*len(two_data)*[2] + resampling_factor*len(three_data)*[3] + resampling_factor*len(four_data)*[4]

	#When resampling factor = 2

	# print len(single_data), resampling_factor*len(two_data), (3+resampling_factor)*len(three_data), (8+resampling_factor)*len(four_data)
	# X = single_data + (resampling_factor)*two_data + (3+resampling_factor)*three_data + (8+resampling_factor)*four_data
	# Y = len(single_data)*[1] + resampling_factor*len(two_data)*[2] + (3+resampling_factor)*len(three_data)*[3] + (8+resampling_factor)*len(four_data)*[4]

	# X = three_data + four_data
	# Y = len(three_data)*[3] + len(four_data)*[4]

	# X = two_data + three_data + four_data		
	# Y = len(two_data)*[2] + len(three_data)*[3] + len(four_data)*[4]

	# X = two_data + three_data
	# Y = len(two_data)*[2] + len(three_data)*[3]

	X = single_data + two_data + three_data + four_data
	Y = len(single_data)*[1] + len(three_data+two_data+four_data)*[2]


	return X,Y







with open("single_length_energy_density_radius_correct.csv") as f:
	single_data = f.readlines()

with open("multi_non_contiguous_length_energy_density_radius_correct.csv") as f:
	multi_data_non_contiguous = f.readlines()

with open("multi_contiguous_length_energy_density_radius_correct.csv") as f:
	multi_data_contiguous = f.readlines()



final_data = single_data + multi_data_contiguous + multi_data_non_contiguous
# final_data = multi_data_non_contiguous + multi_data_contiguous
X, Y = resampleData(final_data)

# print len(X), len(Y)



# for x in final_data:
# 	x = x.split(",")
# 	pdb = x[0].strip()
# 	chain = x[1].strip()
# 	domains = int(x[2].strip())
# 	length = int(x[3].strip())
# 	energy = float(x[4].strip())
# 	density = float(x[5].strip())
# 	radius = float(x[6].strip())
# 	value = [length,energy,density,radius]

	
# 	

# 	if domains >= 2:
# 		X.append(value)
# 		Y.append(domains)

# X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0.25,random_state=0)
# print len(X_train), len(y_train)
# print len(X_test), len(y_test)

skf = StratifiedKFold(n_splits=10)
kernel = 'linear'
# print "Kernel is ", kernel 
# class_weights_dict = {1:1, 2:2, 3:20, 4:11}

# clf = svm.SVC(kernel=kernel, class_weight=class_weights_dict)
clf = svm.SVC(kernel=kernel, class_weight='balanced')

predicted = cross_val_predict(clf, X, Y, cv=skf)


X_test = X
y_test = Y
# clf = svm.SVC().fit(X_train,y_train)



# for x in range(0, len(X)):
# print len(y_test)
for y in y_test:
	# print y
	label = int(y)
	if label==1:
		single_chains+=1
	if label==2:
		two_chains+=1
	if label==3:
		three_chains+=1
	if label==4:
		four_chains+=1

print single_chains, two_chains, three_chains, four_chains

for x in range(0, len(X_test)):
	# value = X[x]
	# actual_label = int(Y[x])
	# predicted_label = clf.predict([value])[0]

	value = X_test[x]
	predicted_label = int(predicted[x])
	actual_label = int(y_test[x])
	dict_key = data_dict.keys()[data_dict.values().index(value)]

	# print dict_key[0],",",dict_key[1],",",predicted_label, ",", actual_label
	# if predicted_label==3:
		# print predicted_label, actual_label
	if predicted_label==actual_label:
		
		# print
		if actual_label==1:
			single_correct+=1
		elif actual_label==2:
			two_correct+=1
		elif actual_label==3:
			three_correct+=1
		else:
			four_correct+=1

		total_correct+=1
	# else:
		# print "INCORRECT"


# print "FINAL ACCURACY", total_correct*100/len(X)
print "Accuracy of test dataset", total_correct*100/len(X_test)

print "Single Correct", single_correct, single_chains, single_correct*100/single_chains
print "Two Correct", two_correct, two_chains, two_correct*100/two_chains
# print "Three Correct", three_correct, three_chains, three_correct*100/three_chains
# print "Four Correct", four_correct, four_chains, four_correct*100/four_chains

