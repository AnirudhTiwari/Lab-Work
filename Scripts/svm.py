from sklearn import svm
import numpy as np
from random import randint

single_data = []
multi_data = []
desired_chains = 60

with open("single_length_energy_density_radius_correct.csv") as f:
	single_data = f.readlines()

with open("multi_length_energy_density_radius_correct.csv") as f:
	multi_data = f.readlines()


X = []

two_domains = []
three_domains = []
four_domains = []

single_chains = []
two_chains = []
three_chains = []
four_chains = []

chain_counter = 1


for x in multi_data:
	y = x.split(",")
	domains = int(y[2].strip())

	if domains==2:
		two_domains.append(x)

	if domains==3:
		three_domains.append(x)

	if domains==4:
		four_domains.append(x)


while len(single_chains)!=desired_chains:
	num = randint(0, len(single_data)-1)
	if num not in single_chains:
		single_chains.append(num)

while len(two_chains)!=desired_chains:
	num = randint(0, len(two_domains)-1)
	if num not in two_chains:
		two_chains.append(num)

while len(three_chains)!=desired_chains:
	num = randint(0, len(three_domains)-1)
	if num not in three_chains:
		three_chains.append(num)

while len(four_chains)!=desired_chains:
	num = randint(0, len(four_domains)-1)
	if num not in four_chains:
		four_chains.append(num)


for chain in range(0, len(single_chains)):

	x = single_data[single_chains[chain]]
	x = x.split(",")

	length = int(x[3].strip())
	energy = float(x[4].strip())
	density = float(x[5].strip())
	radius = float(x[6].strip())

	X.append([length, energy, density, radius])

for chain in range(0, len(two_chains)):

	x = two_domains[two_chains[chain]]
	x = x.split(",")

	length = int(x[3].strip())
	energy = float(x[4].strip())
	density = float(x[5].strip())
	radius = float(x[6].strip())

	X.append([length, energy, density, radius])

for chain in range(0, len(three_chains)):

	x = three_domains[three_chains[chain]]
	x = x.split(",")

	length = int(x[3].strip())
	energy = float(x[4].strip())
	density = float(x[5].strip())
	radius = float(x[6].strip())

	X.append([length, energy, density, radius])


for chain in range(0, len(four_chains)):

	x = four_domains[four_chains[chain]]
	x = x.split(",")

	length = int(x[3].strip())
	energy = float(x[4].strip())
	density = float(x[5].strip())
	radius = float(x[6].strip())

	X.append([length, energy, density, radius])

Y = ["Single"]*desired_chains + ["Two"]*desired_chains + ["Three"]*desired_chains + ["Four"]*desired_chains


clf = svm.SVC()
clf.fit(X,Y)


single_correct = 0
multi_correct = 0

single_wrong = 0
multi_wrong = 0

two_correct = 0
three_correct = 0
four_correct = 0

two_wrong = 0
three_wrong = 0
four_wrong = 0


test_single = []
test_two = []
test_three = []
test_four = []

for x in single_data:
	x = x.split(",")
	length = int(x[3].strip())
	energy = float(x[4].strip())
	density = float(x[5].strip())
	radius = float(x[6].strip())
	test_single.append([length, energy, density, radius])


for x in clf.predict(test_single):
	if x=="Single":
		single_correct+=1
	else:
		single_wrong+=1

print "single_correct", "{0:.2f}".format(single_correct*100.0/len(single_data))

for x in two_domains:
	x = x.split(",")
	length = int(x[3].strip())
	energy = float(x[4].strip())
	density = float(x[5].strip())
	radius = float(x[6].strip())
	test_two.append([length, energy, density, radius])

for x in clf.predict(test_two):
	if x=="Two":
		two_correct+=1
	else:
		two_wrong+=1


print "Two_correct", two_correct, len(two_domains), "{0:.2f}".format(two_correct*100.0/len(two_domains))


for x in three_domains:
	x = x.split(",")
	length = int(x[3].strip())
	energy = float(x[4].strip())
	density = float(x[5].strip())
	radius = float(x[6].strip())
	test_three.append([length, energy, density, radius])

for x in clf.predict(test_three):
	if x=="Three":
		three_correct+=1
	else:
		three_wrong+=1

print "Three_correct", three_correct, len(three_domains), "{0:.2f}".format(three_correct*100.0/len(three_domains))


for x in four_domains:
	x = x.split(",")
	length = int(x[3].strip())
	energy = float(x[4].strip())
	density = float(x[5].strip())
	radius = float(x[6].strip())
	test_four.append([length, energy, density, radius])

for x in clf.predict(test_four):
	if x=="Four":
		four_correct+=1
	else:
		four_wrong+=1

print "Four_correct", four_correct, len(four_domains),"{0:.2f}".format(four_correct*100.0/len(four_domains))

# for x in multi_data:
# 	x = x.split(",")

# 	domains = int(x[2].strip())
# 	length = int(x[3].strip())
# 	energy = float(x[4].strip())
# 	density = float(x[5].strip())
# 	radius = float(x[6].strip())

# 	prediction = clf.predict([length, energy, density, radius])[0]

# # 	# if prediction=="Multi":
# # 	# 	multi_correct+=1


# 	if domains==2 and prediction=="Two":
# 		two_correct+=1
	
# 	elif domains==3 and prediction=="Three":
# 		three_correct+=1

# 	elif domains==4 and prediction=="Four":
# 		four_correct+=1

# 	else:
# 		multi_wrong+=1

# multi_correct = two_correct + three_correct + four_correct

# print single_correct, single_wrong, multi_correct, multi_wrong

# print two_correct, three_correct, four_correct

# print "ACCURACY", 100.0*(single_correct+multi_correct)/(len(single_data)+len(multi_data))


