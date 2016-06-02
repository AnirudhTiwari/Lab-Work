# import matplotlib as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

single_length = []
single_density = []
single_energy = []

multi_length = []
multi_density = []
multi_energy = []

with open("single_length_energy_density.csv") as f1:
	single = f1.readlines()

with open("multi_length_energy_density.csv") as f2:
	multi = f2.readlines()

for x in single:
	single_length.append(int(x.split(",")[3].strip()))
	single_energy.append(float(x.split(",")[4].strip()))
	single_density.append(float(x.split(",")[5].strip()))

for x in multi:
	multi_length.append(int(x.split(",")[3].strip()))
	multi_energy.append(float(x.split(",")[4].strip()))
	multi_density.append(float(x.split(",")[5].strip()))


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(single_length,single_energy,single_density, c='r')
ax.scatter(multi_length,multi_energy,multi_density, c='b')

ax.set_xlabel('Length')
ax.set_ylabel('Interaction Energy')
ax.set_zlabel('Density')

plt.show()


ans = [0, 0.0, 0.0, 0, 0, 0, 0, 0]

best_val = -5000000.0

density = 0.0

while(density <= 0.08):

	single_correct = 0
	single_wrong = 0

	multi_correct = 0
	multi_wrong = 0

	for a,b,c in zip(single_length, single_energy,single_density):
		
		if int(a) >= 150 and float(b) <= 0.25 and float(c) <= density:
			single_wrong+=1

		else:
			single_correct+=1



	for a,b,c in zip(multi_length, multi_energy, multi_density):
		if int(a) >= 150 and float(b) <= 0.25 and float(c) <= density:
			multi_correct+=1
		else:
			multi_wrong+=1


	print "For length " + str(150) + " and energy " + str(0.2) + " and density " + str(density) + " Single correct " + str(single_correct) + " and Single Wrong " + str(single_wrong)
	print "For length " + str(150) + " and energy " + str(0.2) + " and density " + str(density) + " Multi correct " + str(multi_correct) + " and Multi Wrong " + str(multi_wrong)


	accuracy = (single_correct+multi_correct)*100/(len(single_length) + len(multi_length))
	print accuracy
	print

	if accuracy > best_val:
		best_val = accuracy
	
		ans[0] = 150
		ans[1] = 0.25
		ans[2] = density
		ans[3] = (single_correct*100)/len(single_length)
		ans[4] = (single_wrong*100)/len(single_length)

		ans[5] = (multi_correct*100)/len(multi_length)
		ans[6] = (multi_wrong*100)/len(multi_length)

		ans[7] = best_val


	density = density + 0.02

print ans[0], ans[1], ans[2], ans[3], ans[4], ans[5], ans[6], ans[7]