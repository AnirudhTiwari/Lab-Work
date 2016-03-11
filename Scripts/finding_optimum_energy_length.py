single_energy = []
multi_energy = []

single_length = []
multi_length = []

with open("energy_single_radius_7.csv") as f1:
	single = f1.readlines()

with open("energy_multi_radius_7.csv") as f2:
	multi = f2.readlines()


for x in single:
	single_length.append(x.split(",")[3].strip())
	single_energy.append(x.split(",")[4].strip())

for x in multi:
	multi_length.append(x.split(",")[3].strip())
	multi_energy.append(x.split(",")[4].strip())



ans = [0, 0.0, 0, 0, 0, 0, 0]

best_val = -5000000.0

for length in range(0, 800, 5):
	energy = 0.0
	while(energy <= 0.6):

		single_correct = 0
		single_wrong = 0

		multi_correct = 0
		multi_wrong = 0

		for a,b in zip(single_length, single_energy):
			
			if int(a) >= length and float(b) <= float(energy):
				single_wrong+=1

			else:
				single_correct+=1



		for a,b in zip(multi_length, multi_energy):
			if int(a) >= length and float(b) <= float(energy):
				multi_correct+=1
			else:
				multi_wrong+=1


		print "For length " + str(length) + " and energy " + str(energy) + " Single correct " + str(single_correct) + " and Single Wrong " + str(single_wrong)
		print "For length " + str(length) + " and energy " + str(energy) + " Multi correct " + str(multi_correct) + " and Multi Wrong " + str(multi_wrong)


		accuracy = (single_correct+multi_correct)*100/(len(single_length) + len(multi_length))
		print accuracy
		print

		if accuracy > best_val:
			best_val = accuracy
		
			ans[0] = length
			ans[1] = energy

			ans[2] = (single_correct*100)/len(single_length)
			ans[3] = (single_wrong*100)/len(single_length)

			ans[4] = (multi_correct*100)/len(multi_length)
			ans[5] = (multi_wrong*100)/len(multi_length)

			ans[6] = best_val


		energy = energy + 0.05

print ans[0], ans[1], ans[2], ans[3], ans[4], ans[5], ans[6]









