'''Program to find the optimum parameter, taken two at a time, for which we can get the 
   maximum accuracy in classifying single domain proteins from multi domain proteins.
'''

single_length = []
multi_length = []

single_energy = []
multi_energy = []

single_density = []
multi_density = []

single_radius = []
multi_radius = []

with open("single_length_energy_density_radius.csv") as f1:
	single = f1.readlines()

with open("multi_length_energy_density_radius.csv") as f2:
	multi = f2.readlines()


for x in single:
	single_length.append(x.split(",")[3].strip())
	single_energy.append(x.split(",")[4].strip())
	single_density.append(x.split(",")[5].strip())
	single_radius.append(x.split(",")[6].strip())


for x in multi:
	multi_length.append(x.split(",")[3].strip())
	multi_energy.append(x.split(",")[4].strip())
	multi_density.append(x.split(",")[5].strip())
	multi_radius.append(x.split(",")[6].strip())





ans = [0, 0.0, 0, 0, 0, 0, 0]

best_val = -5000000.0

for length in range(0, 1600, 5):
	energy = 0.0
	density = 0.0
	radius = 0.0
	
	# while(energy <= 0.8):
	# while density <= 0.1:
	while radius <= 180.0:
		single_correct = 0
		single_wrong = 0

		multi_correct = 0
		multi_wrong = 0

		# for a,b in zip(single_length, single_energy):
		# for a,b in zip(single_length, single_density):
		for a,b in zip(single_length, single_radius):

			
			# if int(a) >= length and float(b) <= float(energy):
			# if int(a) >= length and float(b) <= float(density):
			if int(a) >= length and float(b) <= float(radius):

				single_wrong+=1

			else:
				single_correct+=1



		# for a,b in zip(multi_length, multi_energy):
		# for a,b in zip(multi_length, multi_density):
		for a,b in zip(multi_length, multi_radius):


			# if int(a) >= length and float(b) <= float(energy):
			# if int(a) >= length and float(b) <= float(density):
			if int(a) >= length and float(b) <= float(radius):
				multi_correct+=1
			else:
				multi_wrong+=1


		# print "For length " + str(length) + " and energy " + str(energy) + " Single correct " + str(single_correct) + " and Single Wrong " + str(single_wrong) + str(single_wrong) + " Single Accuracy " + str(100*single_correct/(len(single_length)))
		# print "For length " + str(length) + " and energy " + str(energy) + " Multi correct " + str(multi_correct) + " and Multi Wrong " + str(multi_wrong) + " Multi Accuracy " + str(100*multi_correct/(len(multi_length)))

		# print "For length " + str(length) + " and density " + str(density) + " Single correct " + str(single_correct) + " and Single Wrong " + str(single_wrong) + " Single Accuracy " + str(100*single_correct/(len(single_length)))
		# print "For length " + str(length) + " and density " + str(density) + " Multi correct " + str(multi_correct) + " and Multi Wrong " + str(multi_wrong) + " Multi Accuracy " + str(100*multi_correct/(len(multi_length)))

		print "For length " + str(length) + " and radius " + str(radius) + " Single correct " + str(single_correct) + " and Single Wrong " + str(single_wrong) + " Single Accuracy " + str(100*single_correct/(len(single_length)))
		print "For length " + str(length) + " and radius " + str(radius) + " Multi correct " + str(multi_correct) + " and Multi Wrong " + str(multi_wrong) + " Multi Accuracy " + str(100*multi_correct/(len(multi_length)))


		accuracy = (single_correct+multi_correct)*100/(len(single_length) + len(multi_length))
		print accuracy
		print

		if accuracy > best_val:
			best_val = accuracy
		
			ans[0] = length
			# ans[1] = energy
			# ans[1] = density
			ans[1] = radius

			ans[2] = (single_correct*100)/len(single_length)
			ans[3] = (single_wrong*100)/len(single_length)

			ans[4] = (multi_correct*100)/len(multi_length)
			ans[5] = (multi_wrong*100)/len(multi_length)

			ans[6] = best_val


		# energy = energy + 0.05
		# density = density + 0.01
		radius = radius + 1.0

print ans[0], ans[1], ans[2], ans[3], ans[4], ans[5], ans[6]









