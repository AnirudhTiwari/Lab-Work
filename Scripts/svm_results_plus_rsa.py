with open("HydrophobicCore_Kmeans_intersection_contiguous_RSA_20_v2.csv") as f:
	contiguous_data = f.readlines() #This includes single domain proteins.

with open("HydrophobicCore_Kmeans_intersection_non_contiguous_RSA_20_v2.csv") as f:
	non_contiguous_data = f.readlines()

with open("svm_labels_v2.csv") as f:
	svm_data = f.readlines()

# print len(contiguous_data)
# print len(non_contiguous_data)

for x in contiguous_data:
	a = x.split(",")
	for y in  svm_data:
		b = y.split(",")
		if a[0].strip()==b[0].strip() and a[1].strip()==b[1].strip():
			print y.strip(), ",", ','.join(map(str, a[3:])).strip()
			

			# counter = 0
			# for c in a:
			# 	if counter==3:
			# 		print b[2].strip(),",", c.strip(), ",",
			# 	elif counter==8:
			# 		print c.strip()
			# 	else:
			# 		print c.strip(), ",",

			# 	counter+=1

			break
