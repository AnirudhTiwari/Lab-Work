import ast
with open('two_domain_unrepresented_classes_and_chains_in_training_dataset.txt') as f:
	two_domain_unrep_chains = f.readlines()

with open('three_domain_unrepresented_classes_and_chains_in_training_dataset.txt') as f:
	three_domain_unrep_chains = f.readlines()

with open('four_domain_unrepresented_classes_and_chains_in_training_dataset.txt') as f:
	four_domain_unrep_chains = f.readlines()

with open('svm_labels_hydrophobic_resdiues_contiguous_v3.csv') as f:
	contiguous_data = f.readlines()

with open('svm_labels_hydrophobic_resdiues_non_contiguous_v3.csv') as f:
	non_contiguous_data = f.readlines()

multi_data = contiguous_data + non_contiguous_data


def findSVMPredictionForGivenChain(unrep_chain):
	for x in multi_data:
		x = x.split(",")
		pdb = x[0].strip()
		chain = x[1].strip().lower()
		pdb, chain, unrep_chain
		if pdb+chain==unrep_chain:
			correct_domains = int(x[2])
			svm_prediction = int(x[3])
			if correct_domains==svm_prediction:
				return 1
			else:
				return 0


two_incorrect = 0
three_incorrect = 0
four_incorrect = 0

for x in two_domain_unrep_chains:
	y = x.partition("=")
	cath_class = ast.literal_eval(y[0])
	cath_chains = ast.literal_eval(y[2])
	for a in cath_chains:
		if findSVMPredictionForGivenChain(a.strip())==0:
			two_incorrect+=1

for x in three_domain_unrep_chains:
	y = x.partition("=")
	cath_class = ast.literal_eval(y[0])
	cath_chains = ast.literal_eval(y[2])
	for a in cath_chains:
		if findSVMPredictionForGivenChain(a.strip())==0:
			three_incorrect+=1	
	

for x in four_domain_unrep_chains:
	y = x.partition("=")
	cath_class = ast.literal_eval(y[0])
	cath_chains = ast.literal_eval(y[2])
	for a in cath_chains:
		if findSVMPredictionForGivenChain(a.strip())==0:
			four_incorrect+=1

print "Incorrect two domain proteins -> ", two_incorrect, "Total unrepresented two domain chains -> ", len(two_domain_unrep_chains)
print "Incorrect three domain proteins -> ", three_incorrect, "Total unrepresented three domain chains -> ", len(three_domain_unrep_chains)
print "Incorrect four domain proteins -> ", four_incorrect, "Total unrepresented four domain chains -> ", len(four_domain_unrep_chains)

