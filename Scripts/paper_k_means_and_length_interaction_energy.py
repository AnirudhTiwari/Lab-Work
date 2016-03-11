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