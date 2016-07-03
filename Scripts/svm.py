from sklearn import svm
import numpy as np

single_data = []
multi_data = []

with open("single_length_energy_density_radius_correct.csv") as f:
	single_data = f.readlines()

with open("multi_length_energy_density_radius_correct.csv") as f:
	multi_data = f.readlines()


X = []

for x in single_data:
	x = x.split(",")
	length = int(x[3].strip())
	energy = float(x[4].strip())
	density = float(x[5].strip())
	radius = float(x[6].strip())

	X.append([length, energy, density, radius])
	# X.append([length, energy, density])



for x in multi_data:
	x = x.split(",")
	length = int(x[3].strip())
	energy = float(x[4].strip())
	density = float(x[5].strip())
	radius = float(x[6].strip())

	X.append([length, energy, density, radius])
	# X.append([length, energy, density])



# Y = ["Single"]*len(single_data) + ["Multi"]*len(multi_data)

Y = ["Single"]*len(single_data)

for x in multi_data:
	x = x.split(",")
	domains = int(x[2].strip())

	if domains==2:
		Y.append("Two")
	elif domains==3:
		Y.append("Three")
	else:
		Y.append("Four")

clf = svm.SVC()
clf.fit(X,Y)


single_correct = 0
multi_correct = 0

single_wrong = 0
multi_wrong = 0

for x in single_data:
	x = x.split(",")
	length = int(x[3].strip())
	energy = float(x[4].strip())
	density = float(x[5].strip())
	radius = float(x[6].strip())

	if clf.predict([length, energy, density, radius])[0]=="Single":
		single_correct+=1
	else:
		single_wrong+=1



two_correct = 0
three_correct = 0
four_correct = 0

for x in multi_data:
	x = x.split(",")

	domains = int(x[2].strip())
	length = int(x[3].strip())
	energy = float(x[4].strip())
	density = float(x[5].strip())
	radius = float(x[6].strip())

	prediction = clf.predict([length, energy, density, radius])[0]

	# if prediction=="Multi":
	# 	multi_correct+=1


	if domains==2 and prediction=="Two":
		two_correct+=1
	
	elif domains==3 and prediction=="Three":
		three_correct+=1

	elif domains==4 and prediction=="Four":
		four_correct+=1

	else:
		multi_wrong+=1

multi_correct = two_correct + three_correct + four_correct

print single_correct, single_wrong, multi_correct, multi_wrong

print two_correct, three_correct, four_correct

print "ACCURACY", 100.0*(single_correct+multi_correct)/(len(single_data)+len(multi_data))


