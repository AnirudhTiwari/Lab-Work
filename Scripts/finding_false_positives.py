single_energy = []
multi_energy = []

single_length = []
multi_length = []
multi_name = []

with open("../Output Data/energy_single_radius_7.csv") as f1:
	single = f1.readlines()

with open("../Output Data/energy_multi_radius_7.csv") as f2:
	multi = f2.readlines()

for x in multi:
	multi_length.append(x.split(",")[3].strip())
	multi_energy.append(x.split(",")[4].strip())
	multi_name.append(x.split(",")[0].strip() + x.split(",")[1].strip())

for x in range(0,len(multi_length)):
	if int(multi_length[x]) < 150 or float(multi_energy[x]) > 0.2:
		print multi_name[x]