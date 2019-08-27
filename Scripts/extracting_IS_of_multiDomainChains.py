import json
import common_functions as utils

with open('self_created_multi_training_dataset_features_v4.json', 'r') as f:
    SVM_multi_train_data = json.load(f)

for key, value in SVM_multi_train_data.iteritems():
	print key, ",", value["Domains"], ",", value["Length"], ",", value["Interaction_Energy"]