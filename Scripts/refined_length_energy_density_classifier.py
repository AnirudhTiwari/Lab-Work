''' Program to find the overall accuracy by using the following criteria
	1. All those proteins with length <= 100 are essentially single domain
	2. All those proteins with length >= 300 and interaction energy <= 0.25 are multi domain
	3. All those proteins with 100 < length < 300 and interaction energy <= 0.25 are also multi-domain.
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
	single_length.append(int(x.split(",")[3].strip()))
	single_energy.append(float(x.split(",")[4].strip()))
	single_density.append(10.0*float(x.split(",")[5].strip()))
	single_radius.append(float(x.split(",")[6].strip()))


for x in multi:
	multi_length.append(int(x.split(",")[3].strip()))
	multi_energy.append(float(x.split(",")[4].strip()))
	multi_density.append(10*float(x.split(",")[5].strip()))
	multi_radius.append(float(x.split(",")[6].strip()))


correct_single = 0
correct_multi = 0

wrong_single = 0
wrong_multi = 0


for x in single_length:
	if x <= 100:
		correct_single+=1


for x in multi_length:
	if x <= 100:
		wrong_multi+=1


print "length <= 100 criteria --> ","correct single ->", correct_single, "wrong single ->", wrong_single,"correct multi -> ", correct_multi ,"wrong multi ->",wrong_multi
print

for length, energy in zip(single_length, single_energy):
	
	# if length >=300 and energy > 0.25:
	# 	correct_single+=1

	if length >=300:# and energy <= 0.25:
		wrong_single+=1


for length, energy in zip(multi_length, multi_energy):
	
	# if length >= 300 and energy > 0.25:
	# 	wrong_multi+=1
		

	if length >=300: #and energy <= 0.25:
		correct_multi+=1


print "For length >=300 criteria --> ","correct single ->", correct_single, "wrong single ->", wrong_single,"correct multi -> ", correct_multi ,"wrong multi ->",wrong_multi
print

for length, energy, density in zip(single_length, single_energy, single_density):
	
	if length > 100 and length < 300:
		if energy > 0.25:
			correct_single+=1

		else:
			if density >= 0.4:
				correct_single+=1

			else:
				wrong_single+=1
			# wrong_single+=1

for length, energy, density in zip(multi_length, multi_energy, multi_density):

	if length > 100 and length < 300:

		if energy < 0.25:
			correct_multi+=1

		else:
			if density < 0.4:
				correct_multi+=1
			else:
				wrong_multi+=1

			# wrong_multi+=1



print "For 100 < length criteria < 300 --> ","correct single ->", correct_single, "wrong single ->", wrong_single,"correct multi -> ", correct_multi ,"wrong multi ->",wrong_multi
print