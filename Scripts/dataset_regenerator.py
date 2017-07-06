with open("single_length_energy_density_radius_correct.csv") as f:
	single_test_data = f.readlines()

with open("multi_non_contiguous_length_energy_density_radius_correct.csv") as f:
	multi_test_data_non_contiguous = f.readlines()

with open("multi_contiguous_length_energy_density_radius_correct.csv") as f:
	multi_test_data_contiguous = f.readlines()

final_data = single_test_data + multi_test_data_contiguous + multi_test_data_non_contiguous

for x in final_data:
	x = x.split(",")
	pdb = x[0].strip()
	chain = x[1].strip()
	print pdb+chain