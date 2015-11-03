import pickle
import matplotlib.pyplot as plt

max_rg = 45
max_length = 610
max_energy = 0.15


fp1 = open('single_domain_length', 'rb')
single_domain_length = pickle.load(fp1)

fp2 = open('single_domain_rg', 'rb')
single_domain_rg = pickle.load(fp2)

fp3 = open('single_domain_interaction_energy', 'rb')
single_domain_interaction_energy = pickle.load(fp3)

fp4 = open('two_domain_length', 'rb')
two_domain_length = pickle.load(fp4)

fp5 = open('two_domain_rg', 'rb')
two_domain_rg = pickle.load(fp5)

fp6 = open('two_domain_interaction_energy', 'rb')
two_domain_interaction_energy = pickle.load(fp6)

val = -500000

ans = [0,0,0,0]

for i in range(0, max_length, 5):
	j=0.0
	while(j <= max_energy):
		fp=0		
		tp=0
		for a in range(len(two_domain_length)):
			if int(two_domain_length[a]) >= i and float(two_domain_interaction_energy[a]) <= j:
				tp+=1

		for a in range(len(single_domain_length)):
			if int(single_domain_length[a]) >=i and float(single_domain_interaction_energy[a]) <= j:
				fp+=1

		if tp-fp >= val:
			val = tp-fp
			ans[0] = i
			ans[1] = j
			ans[2] = tp
			ans[3] = fp

		j = j + 0.02

print "For length >= " + str(ans[0]) + " And interacton energy <= " + str(ans[1]) + " True positives " + str(ans[2]) + "/" + str(len(two_domain_length)) + " False positives " + str(ans[3]) + "/" + str(len(single_domain_length))


val = -500000

ans = [0,0,0,0]

for i in range(0, max_rg, 2):
	j=0.0
	while(j <= max_energy):
		fp=0		
		tp=0
		# print "initial tp and fp ", tp, fp
		for a in range(len(two_domain_rg)):
			if float(two_domain_rg[a]) >= i and float(two_domain_interaction_energy[a]) <= j:
				# print two_domain_rg[a], two_domain_interaction_energy[a], j
				tp+=1

		for a in range(len(single_domain_rg)):
			if float(single_domain_rg[a]) >= i and float(single_domain_interaction_energy[a]) <= j:
				# print single_domain_rg[a], single_domain_interaction_energy[a], j
				fp+=1

		
		if tp-fp >= val:
			val = tp-fp
			ans[0] = i
			ans[1] = j
			ans[2] = tp
			ans[3] = fp


		j = j + 0.02


print "For rg >= " + str(ans[0]) + " And interacton energy <= " + str(float(ans[1])) + " True positives " + str(ans[2]) + "/" + str(len(two_domain_length)) + " False positives " + str(ans[3]) + "/" + str(len(single_domain_length))


val = -500000

ans = [0,0,0,0,0]

for i in range(0, max_length, 5):

	for j in range(0, max_rg, 2):

		k=0.0

		while(k <= max_energy):
			fp=0		
			tp=0
			for a in range(len(two_domain_rg)):
				if two_domain_length[a] >= i and float(two_domain_rg[a]) >= j and float(two_domain_interaction_energy[a]) <= k:
					tp+=1

			for a in range(len(single_domain_rg)):
				if single_domain_length[a] >= i and float(single_domain_rg[a]) >= j and float(single_domain_interaction_energy[a]) <= k:
					fp+=1

			# print tp, fp
			if tp-fp >= val:
				# print i, j, k, tp, fp
				val = tp-fp
				ans[0] = i
				ans[1] = j
				ans[2] = k
				ans[3] = tp
				ans[4] = fp


			k = k + 0.02


print "For length >= " + str(ans[0]) + " And Rg >= " + str(float(ans[1]))+ " And interacton energy <= " + str(float(ans[2])) + " True positives " + str(ans[3]) + "/" + str(len(two_domain_length)) + " False positives " + str(ans[4]) + "/" + str(len(single_domain_length))

y_line_interaction_energy = [ans[2] for x in range(7)]
x_line_length = [ans[0] for x in range(7)]
x_line_rg  = [ans[1] for x in range(7)]

# plt.plot(single_domain_length, single_domain_interaction_energy,'ro')
# plt.plot(two_domain_length, two_domain_interaction_energy, 'bo')
# plt.plot([0,100,200,300,400,500,600], y_line_interaction_energy)
# plt.plot(x_line_length, [0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12])
# plt.xlabel('Length')

# y_line_interaction_energy = [ans[2] for x in range(10)]

plt.plot(single_domain_rg, single_domain_interaction_energy, 'ro')
plt.plot(two_domain_rg, two_domain_interaction_energy, 'bo')
plt.plot([10,15,20,25,30,35,40], y_line_interaction_energy)
plt.plot(x_line_rg, [0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12])


plt.xlabel('Radius of Gyration')
plt.ylabel('Interaction Energy')

plt.show()