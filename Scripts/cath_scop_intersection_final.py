with open("../Output Data/cath_scop_intersection/cath_scop_intersection.txt") as f12:
	req_chains = f12.readlines()

with open("../Input Files/CathDomainList") as f2:
	cath_chains = f2.readlines()


cath_dict = {}

for x in cath_chains:
	if x[0]!='#':
		data = x.split(" ")
		temp = []
		for y in data:
			if y!="":
				temp.append(y)
		
		cath_dict[temp[0].lower()] = [temp[1], temp[2], temp[3], temp[4]]
		# print temp[0],cath_dict[temp[0]]

ans_chains = []

CATH = []
for chains in req_chains:
	chain = chains.split(" ")[0].strip()
 	domains = int(chains.split(" ")[1].strip())

 	for x in range(0,domains+1):
 		key = chain + "0" + str(x)
 		if key in cath_dict:
 			if cath_dict[key] not in CATH:
 				CATH.append(cath_dict[key])
 				if chain not in ans_chains:
 					ans_chains.append(chain)


dom_counter = {}

for x in ans_chains:
	for y in req_chains:
		if x == y.split(" ")[0]:
			# print x,y.split(" ")[1].strip()
			doms =  int(chains.split(" ")[1].strip())
			if doms in dom_counter:
				dom_counter[doms]+=1
			else:
				dom_counter[doms]=1


print dom_counter


# print ans_chains
# print len(ans_chains)

# for x in ans_chains:
# 	for y in ans_chains:
# 		if x[:4]==y[:4] and x[4]!=y[4]:
# 			ans_chains.remove(y)

# print len(ans_chains)