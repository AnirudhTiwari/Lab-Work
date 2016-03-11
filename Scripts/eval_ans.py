import pickle
import matplotlib.pyplot as plt


a = int(raw_input("No. of domains(lesser) for protein A: "))
b = int(raw_input("No. of domains(higher) for protein B: "))
c = raw_input("Contiguous(C)/Non-Contiguous(N)/Both(B): ")

domain_string_a=""

if(a==1):
	domain_string_a="single"

if(a==2):
	domain_string_a="two"

if(a==3):
	domain_string_a="three"

if(a==4):
	domain_string_a="four"

if(a==5):
	domain_string_a="five"

if c=='C':
	length_a = domain_string_a + "_domain_length_contiguous"
	rg_a = domain_string_a + "_domain_rg_contiguous"
	interaction_energy_a = domain_string_a + "_domain_interaction_energy_contiguous"

else:
	length_a = domain_string_a + "_domain_length_non_contiguous"
	rg_a = domain_string_a + "_domain_rg_non_contiguous"
	interaction_energy_a = domain_string_a + "_domain_interaction_energy_non_contiguous"



fp1 = open(length_a, 'rb')
list_length_a = pickle.load(fp1)

fp2 = open(rg_a, 'rb')
list_rg_a = pickle.load(fp2)

fp3 = open(interaction_energy_a, 'rb')
list_interaction_energy_a = pickle.load(fp3)


tp = 0
fn = 0

for (length,radius,energy) in zip(list_length_a, list_rg_a, list_interaction_energy_a):
	if (length >=150 and length<=320) and (energy<=0.06 and energy>=0.04):
		tp+=1
		print length, radius, energy
	else:
		fn+=1

print tp, len(list_length_a)
print fn, len(list_length_a)