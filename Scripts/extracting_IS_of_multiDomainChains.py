import json
import common_functions as utils

with open('benchmark_3_multi_domain_incorrect_chains_features.json', 'r') as f:
    SVM_multi_train_data = json.load(f)

for key, value in SVM_multi_train_data.iteritems():
	print key, ",", value["Domains"], ",", value["Length"], ",", value["IS-Sum_2"], ",", value["IS-Sum_3"], ",", value["IS-Sum_4"]