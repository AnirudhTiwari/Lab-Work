with open('ASTRAL_SCOP30_CHAINS', 'r') as f:
	original_list = f.readlines()
with open('ASTRAL_SCOP30_CHAINS_NOT_IN_CATH', 'r') as f:
	absentees_in_cath = f.readlines()


print len(original_list)
print len(absentees_in_cath)


for x in absentees_in_cath:
	original_list.remove(x.upper())

for x in original_list:
	print x.lower().strip()