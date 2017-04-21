#Program to add Number of buried residues as an added feature to already existing L,Rg,Density,IE

with open('single_length_energy_density_radius_correct.csv', 'r') as f:
	single_data = f.readlines()

with open('RSA_KMeans_contiguous_out.csv', 'r') as f:
	contiguous_RSA = f.readlines()

with open('RSA_KMeans_non_contiguous_out.csv', 'r') as f:
	non_contiguous_RSA = f.readlines()


for buried_residues in contiguous_RSA:
	buried_residues = buried_residues.split(",")
	pdb = buried_residues[0].strip()
	chain = buried_residues[1].strip()
	domains = int(buried_residues[2].strip())

	if domains==1:
		for single_data in single_data:
			


