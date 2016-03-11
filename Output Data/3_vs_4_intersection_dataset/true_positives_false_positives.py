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


length_a = domain_string_a + "_domain_length"
rg_a = domain_string_a + "_domain_rg"
interaction_energy_a  = domain_string_a + "_domain_interaction_energy"

fp1 = open(length_a, 'rb')
list_length_a = pickle.load(fp1)

fp2 = open(rg_a, 'rb')
list_rg_a = pickle.load(fp2)

fp3 = open(interaction_energy_a, 'rb')
list_interaction_energy_a = pickle.load(fp3)

domain_string_b=""

if(b==2):
	domain_string_b="two"
if(b==3):
	domain_string_b="three"

if(b==4):
	domain_string_b="four"

if(b==5):
	domain_string_b="five"

length_b_contiguous = domain_string_b + "_domain_length_contiguous"
rg_b_contiguous = domain_string_b + "_domain_rg_contiguous"
interaction_energy_b_contiguous = domain_string_b + "_domain_interaction_energy_contiguous"

length_b_non_contiguous = domain_string_b + "_domain_length_non_contiguous"
rg_b_non_contiguous = domain_string_b + "_domain_rg_non_contiguous"
interaction_energy_b_non_contiguous =  domain_string_b + "_domain_interaction_energy_non_contiguous"




fp4 = open(length_b_contiguous, 'rb')
list_length_b_contiguous = pickle.load(fp4)

fp5 = open(rg_b_contiguous, 'rb')
list_rg_b_contiguous = pickle.load(fp5)

fp6 = open(interaction_energy_b_contiguous, 'rb')
list_interaction_energy_b_contiguous = pickle.load(fp6)

fp7 = open(length_b_non_contiguous, 'rb')
list_length_b_non_contiguous = pickle.load(fp7)

fp8 = open(rg_b_non_contiguous, 'rb')
list_rg_b_non_contiguous = pickle.load(fp8)

fp9 = open(interaction_energy_b_non_contiguous, 'rb')
list_interaction_energy_b_non_contiguous = pickle.load(fp9)

val = -500000

max_rg = max(max(list_rg_a), max(list_rg_b_non_contiguous), max(list_rg_b_contiguous))
max_length = max(max(list_length_a), max(list_length_b_contiguous), max(list_length_b_non_contiguous))
max_energy = max(max(list_interaction_energy_a), max(list_interaction_energy_b_contiguous), max(list_interaction_energy_b_non_contiguous))

if c=='C':
	list_length_b = list_length_b_contiguous
	list_rg_b = list_rg_b_contiguous
	list_interaction_energy_b = list_interaction_energy_b_contiguous

if c=='N':
	list_length_b = list_length_b_non_contiguous
	list_rg_b = list_rg_b_non_contiguous
	list_interaction_energy_b = list_interaction_energy_b_non_contiguous

if c=='B':
	list_length_b = list_length_b_non_contiguous + list_length_b_contiguous
	list_rg_b = list_rg_b_non_contiguous + list_rg_b_contiguous
	list_interaction_energy_b = list_interaction_energy_b_non_contiguous + list_interaction_energy_b_contiguous


# ans = [0,0,0,0]

# for i in range(0, max_length, 5):
# 	j=0.0
# 	while(j <= max_energy):
# 		fp=0		
# 		tp=0
# 		for k in range(len(list_length_b)):
# 			if int(list_length_b[k]) >= i and float(list_interaction_energy_b[k]) <= j:
# 				tp+=1

# 		for k in range(len(list_length_a)):
# 			if int(list_length_a[k]) >=i and float(list_interaction_energy_a[k]) <= j:
# 				# print list_length_a[k], list_interaction_energy_a[k]
# 				fp+=1

# 		if tp-fp >= val:
# 			val = tp-fp
# 			ans[0] = i
# 			ans[1] = j
# 			ans[2] = tp
# 			ans[3] = fp

# 		j = j + 0.02

# print "For length >= " + str(ans[0]) + " And interacton energy <= " + str(ans[1]) + " True positives " + str(ans[2]) + "/" + str(len(list_length_b)) + " False positives " + str(ans[3]) + "/" + str(len(list_length_a))


# val = -500000

# ans = [0,0,0,0]

# for i in range(0, int(max_rg), 2):
# 	j=0.0
# 	while(j <= max_energy):
# 		fp=0		
# 		tp=0
# 		# print "initial tp and fp ", tp, fp
# 		for k in range(len(list_rg_b)):
# 			if float(list_rg_b[k]) >= i and float(list_interaction_energy_b[k]) <= j:
# 				# print two_domain_rg[a], two_domain_interaction_energy[a], j
# 				tp+=1

# 		for k in range(len(list_rg_a)):
# 			if float(list_rg_a[k]) >= i and float(list_interaction_energy_a[k]) <= j:
# 				# print rg_a[a], interaction_energy_a[a], j
# 				fp+=1

		
# 		if tp-fp >= val:
# 			val = tp-fp
# 			ans[0] = i
# 			ans[1] = j
# 			ans[2] = tp
# 			ans[3] = fp


# 		j = j + 0.02


# print "For rg >= " + str(ans[0]) + " And interacton energy <= " + str(float(ans[1])) + " True positives " + str(ans[2]) + "/" + str(len(list_rg_b)) + " False positives " + str(ans[3]) + "/" + str(len(list_rg_a))


# val = -500000

# ans = [0,0,0,0,0]

# for i in range(0, max_length, 5):

# 	for j in range(0, int(max_rg), 2):

# 		k=0.0

# 		while(k <= max_energy):
# 			fp=0		
# 			tp=0
# 			for l in range(len(list_length_b)):
# 				if list_length_b[l] >= i and float(list_rg_b[l]) >= j and float(list_interaction_energy_b[l]) <= k:
# 					tp+=1

# 			for m in range(len(list_rg_a)):
# 				if list_length_a[m] >= i and float(list_rg_a[m]) >= j and float(list_interaction_energy_a[m]) <= k:
# 					fp+=1

# 			# print tp, fp
# 			if tp-fp >= val:
# 				# print i, j, k, tp, fp
# 				val = tp-fp
# 				ans[0] = i
# 				ans[1] = j
# 				ans[2] = k
# 				ans[3] = tp
# 				ans[4] = fp


# 			k = k + 0.02


# print "For length >= " + str(ans[0]) + " And Rg >= " + str(float(ans[1]))+ " And interacton energy <= " + str(float(ans[2])) + " True positives " + str(ans[3]) + "/" + str(len(list_length_b)) + " False positives " + str(ans[4]) + "/" + str(len(list_length_a))

# y_line_interaction_energy = [ans[2] for x in range(7)]
# x_line_length = [ans[0] for x in range(7)]
# x_line_rg  = [ans[1] for x in range(7)]


# ans = 0

# for (a,b) in zip(list_length_a, list_interaction_energy_a):
# 	if a < 250 or b > 0.06:
# 		ans+=1

# 	else:
# 		print a,b

# print ans
# print len(list_length_a)
# # plt.plot(list_length_a, list_interaction_energy_a,'ro')
# plt.plot(list_length_b_contiguous, list_interaction_energy_b_contiguous, 'bo')
# plt.xlabel('Length')
# plt.ylabel('Interaction Energy')
# plt.show()



# plt.plot(list_rg_a, list_interaction_energy_a, 'ro')
# plt.plot(list_rg_b_contiguous, list_interaction_energy_b_contiguous, 'bo')
# plt.plot([10,15,20,25,30,35,40], y_line_interaction_energy)
# plt.plot(x_line_rg, [0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12])
# plt.xlabel('Radius of Gyration')
# plt.ylabel('Interaction Energy')
# plt.show()



for (a,b) in zip(list_length_a, list_interaction_energy_a):
	print a,",", '{0:.3f}'.format(b)
# plt.plot(list_length_a, list_interaction_energy_a,'ro')
# plt.plot(list_length_b_non_contiguous, list_interaction_energy_b_non_contiguous, 'go')
# plt.plot([0,100,200,300,400,500,600], y_line_interaction_energy)
# plt.plot(x_line_length, [0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12])
# plt.xlabel('Length')
# plt.ylabel('Interaction Energy')
# plt.show()



# plt.plot(list_rg_a, list_interaction_energy_a, 'ro')
# plt.plot(list_rg_b_non_contiguous, list_interaction_energy_b_non_contiguous, 'go')
# plt.plot([10,15,20,25,30,35,40], y_line_interaction_energy)
# plt.plot(x_line_rg, [0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12])
# plt.xlabel('Radius of Gyration')
# plt.ylabel('Interaction Energy')
# plt.show()


# x_line_length = [250 for x in range(7)]
# y_line_interaction_energy = [0.06 for x in range (7)]
# plt.plot(list_length_a, list_interaction_energy_a,'ro')
# plt.plot(list_length_b_contiguous, list_interaction_energy_b_contiguous, 'bo')
# plt.plot(list_length_b_non_contiguous, list_interaction_energy_b_non_contiguous, 'go')
# plt.plot([0,400,600,800,1200,1400,1600], y_line_interaction_energy)
# plt.plot(x_line_length, [0.0, 0.02, 0.04, 0.06, 0.08, 0.14, 0.20])
# plt.xlabel('Length')
# plt.ylabel('Interaction Energy')
# plt.show()



# plt.plot(list_rg_a, list_interaction_energy_a, 'ro')
# plt.plot(list_rg_b_contiguous, list_interaction_energy_b_contiguous, 'bo')
# plt.plot(list_rg_b_non_contiguous, list_interaction_energy_b_non_contiguous, 'go')
# plt.plot([10,15,20,25,30,40,50], y_line_interaction_energy)
# plt.plot(x_line_rg, [0.0, 0.02, 0.04, 0.06, 0.08, 0.14, 0.20])
# plt.xlabel('Radius of Gyration')
# plt.ylabel('Interaction Energy')
# plt.show()
