#This script is meant to read chains like output_incorrect_Benchmark_3_multi-domain.txt and parse out information of length and CATH annotation. 
#It doesn't give out information as to what was the incorrect annotation. That needs to be parsed from a different script.

import K_means_experimental as km
import json

with open("output_incorrect_Benchmark_2_multi-domain.txt") as f:
	chains = f.readlines()

with open('benchmark_2_multi_domain_incorrect_chains_features.json', 'r') as f:
    feature_dict = json.load(f)

for chain in chains:
	chain = chain.strip()
	km.applyKMeans(chain)
	print "IS-Sum_2: ", feature_dict[chain]["IS-Sum_2"], ",", "IS-Sum_3: " , feature_dict[chain]["IS-Sum_3"], ",", "IS-Sum_4: ", feature_dict[chain]["IS-Sum_4"]



