import gzip
import unicodedata
import sys
import re
import numpy
from random import random
from collections import defaultdict
from string import punctuation
from math import pow
from math import log
from math import exp
from numpy import dot
from numpy.linalg import inv

Userlist = []
Itemlist = []
Buy = []
Sell = []
Rate_User = []
Rate_Item = []
Valid = []

def inlg(f):
	return log(f/(1-f))
	
def logistic(f):
	return 1/(1 + exp(-f))

print "Reading Data..."

fs = open('Userlist', 'r')
while True:
	l = fs.readline()
	ld = l.split()
	if len(ld) < 1:
		break
	Userlist.append(ld[0])
fs.close()

fs = open('Itemlist', 'r')
while True:
	l = fs.readline()
	ld = l.split()
	if len(ld) < 1:
		break
	Itemlist.append(ld[0])
fs.close()

fs = open('Buy', 'r')
while True:
	l = fs.readline()
	ld = l.split()
	if len(ld) < 1:
		break
	Buy.append(ld)
	for i in range(0, len(Buy[-1])):
		Buy[-1][i] = int(Buy[-1][i])
fs.close()

fs = open('Sell', 'r')
while True:
	l = fs.readline()
	ld = l.split()
	if len(ld) < 1:
		break
	Sell.append(ld)
	for i in range(0, len(Sell[-1])):
		Sell[-1][i] = int(Sell[-1][i])
fs.close()

fs = open('Rate_User', 'r')
while True:
	l = fs.readline()
	ld = l.split()
	if len(ld) < 1:
		break
	Rate_User.append(ld)
	for i in range(0, len(Rate_User[-1])):
		Rate_User[-1][i] = float(Rate_User[-1][i])
		# Rate_User[-1][i] = inlg(float(Rate_User[-1][i])/5.1)
fs.close()

fs = open('Rate_Item', 'r')
while True:
	l = fs.readline()
	ld = l.split()
	if len(ld) < 1:
		break
	Rate_Item.append(ld)
	for i in range(0, len(Rate_Item[-1])):
		Rate_Item[-1][i] = float(Rate_Item[-1][i])
		# Rate_Item[-1][i] = inlg(float(Rate_Item[-1][i])/5.1)
fs.close()

fs = open('Rate_Valid', 'r')
while True:
	l = fs.readline()
	ld = l.split()
	if len(ld) < 1:
		break
	Valid.append(ld)
	try:
		i = Itemlist.index(Valid[-1][0])
	except:
		i = -1
	Valid[-1][0] = i	
	try:
		u = Userlist.index(Valid[-1][1])
	except:
		u = -1
	Valid[-1][1] = u	
	Valid[-1][2] = float(Valid[-1][2])
fs.close()

print "Done!"
		
n = len(Userlist)
m = len(Itemlist)

e1 = 1000
a = 0
bu = [0] * (n + 1)
bi = [0] * (m + 1)
lam = 2.4

for loop in range(0, 5):
	num = 0
	a = 0
	for i in range(0, n):
		for j in range(0, len(Buy[i])):
			k = Buy[i][j]
			a += Rate_User[i][j]
			a -= bu[i]
			a -= bi[k]
			num += 1
	a /= num
	
	for i in range(0, n):
		bu[i] = 0
		for j in range(0, len(Buy[i])):
			k = Buy[i][j]
			bu[i] += Rate_User[i][j]
			bu[i] -= a + bi[k]
		bu[i] /= (lam + len(Buy[i]))
	bu[-1] = sum(bu[:-1])/len(bu[:-1]) 
	
	for i in range(0, m):
		bi[i] = 0
		for j in range(0, len(Sell[i])):
			k = Sell[i][j]
			bi[i] += Rate_Item[i][j]
			bi[i] -= a + bu[k]
		bi[i] /= (lam + len(Sell[i]))
	bi[-1] = sum(bi[:-1])/len(bi[:-1]) 
	
	error = 0	
	sample = 0
	for l in Valid:
		predict = a + bi[l[0]] + bu[l[1]]
		if predict > 5:
			predict = 5
		if predict < 0:
			predict = 0
		error += (predict - l[2]) * (predict - l[2])
		sample += 1
	print "MSE:", error/sample
	print "Sample:", sample
	if e1 - error/sample < 0.000001:
	# if e1 < 0.65:
		break
	e1 = error/sample


# Re =[]
# for u in range(0, n):
	# Re.append([])
	# for i in Buy[u]:
		# t = Buy[u].index(i)
		# rate = Rate_User[u][t]
		# for u1 in Sell[i]:
			# t1 = Sell[i].index(u1)
			# rate1 = Rate_Item[i][t1]
			# if rate != rate1:
				# continue
			# if u1 == u:
				# continue
			# Re[-1].append(u1)
		
# error = 0	
# sample = 0
# t = 0
# for l in Valid:
	# t += 1
	# i = l[0]
	# u = l[1]
	# sr = 0
	# su = 0
	# for u1 in Re[u]:
		# try:
			# i1 = Buy[u1].index(i)
			# sr += Rate_User[u1][i1]
			# su += 1
		# except:
			# continue	
	# predict = a + bi[l[0]] + bu[l[1]]
	# if su > 0:
		# print predict, sr/su, su, l[2]
		# raw_input()
	# if su > 1:
		# if predict < sr/su:
			# predict = int(2*predict)/float(2)
		# else:
			# predict = (int(2*predict) + 1)/float(2)
	# if predict > 5:
		# predict = 5
	# if predict < 0:
		# predict = 0
	# error += (predict - l[2]) * (predict - l[2])
	# sample += 1
# print "MSE:", error/sample
# print "Sample:", sample
		
	
	
predictions = open("predictions_Rating.txt", 'w')
for l in open("pairs_Rating.txt"):
	if l.startswith("userID"):
		#header
		predictions.write(l)
		continue
	User,Item = l.strip().split('-')
	try:
		i = Itemlist.index(Item)
	except:
		i = -1
	try:
		u = Userlist.index(User)
	except:
		u = -1
	predict = a + bu[u] + bi[i]
	if predict > 5:
		predict = 5
	predictions.write(User + '-' + Item + ',' + str(predict) + '\n')

predictions.close()




lu = []
li = []
for i in range(0, n):
	lu.append([0.01*random(), 0.01*random(), 0.01*random(), 0.01*random()])
for i in range(0, m):
	li.append([0.01*random(), 0.01*random(), 0.01*random(), 0.01*random()])
lu = numpy.array(lu)
li = numpy.array(li)
for i in range(0, n):
	for j in range(0, len(Rate_User[i])):
		k = Buy[i][j]
		Rate_User[i][j] -= a + bu[i] + bi[k]
		l = Sell[k].index(i)
		Rate_Item[k][l] -= a + bu[i] + bi[k]

error = 0	
sample = 0
for l in Valid:
	predict = dot(lu[l[1]], li[l[0]])
	error += (predict - l[2]) * (predict - l[2])
	sample += 1
print "MSE(0):", error/sample
print "Sample:", sample
	
	
while True:
	num = 0
	e0 = 0
	for i in range(0, n):
		for j in range(0, len(Buy[i])):
			k = Buy[i][j]
			d = Rate_User[i][j] - dot(lu[i], li[k]) 
			# d = Rate_User[i][j] - lu[i] * li[k] 
			e0 += d * d
			num += 1
	print "Train MSE(Befor):", e0 / num


	for u in range(0, n):
		I = []
		R = []
		for j in range(0, 4):
			I.append([0, 0, 0, 0])
			R.append([0, 0, 0, 0])
		for j in range(0, len(Buy[u])):
			i = Buy[u][j]
			I += dot(li[i].T, li[i])
			R += Rate_User[u][j]*li[i]
		for j in range(0, 4):
			I[j][j] += 100
		lu[u] = dot(inv(I), R.T).T
			
	
	num = 0
	e0 = 0
	for i in range(0, n):
		for j in range(0, len(Buy[i])):
			k = Buy[i][j]
			d = Rate_User[i][j] - dot(lu[i], li[k]) 
			# d = Rate_User[i][j] - a - bu[i] -  bi[k] - lu[i] * li[k] 
			e0 += d * d
			num += 1
	print "Train MSE(After):", e0 / num	
	
	
	for i in range(0, m):
		I = []
		R = []
		for j in range(0, 4):
			I.append([0, 0, 0, 0])
			R.append([0, 0, 0, 0])
		for j in range(0, len(Sell[i])):
			u = Sell[i][j]
			I += dot(lu[u].T, lu[u])
			R += Rate_Item[i][j]*lu[u]
		for j in range(0, 4):
			I[j][j] += 100
		li[i] = dot(inv(I), R.T).T
	
	num = 0
	e0 = 0
	for i in range(0, n):
		for j in range(0, len(Buy[i])):
			k = Buy[i][j]
			d = Rate_User[i][j] - dot(lu[i], li[k]) 
			# d = Rate_User[i][j] - a - bu[i] -  bi[k] - lu[i] * li[k] 
			e0 += d * d
			num += 1
	print "Train MSE(Step2):", e0 / num	
	
	# num = 0
	# e0 = 0	
	# for i in range(0, n):
		# for j in range(0, len(Buy[i])):
			# k = Buy[i][j]
			# d = Rate_User[i][j] - a - bu[i] -  bi[k] - dot(lu[i], li[k])
			# e0 += d * d
			# num += 1
	# print "Train MSE(Step2):", e0 / num	
	# raw_input()
	
	error = 0	
	sample = 0
	for l in Valid:
		predict = a + bi[l[0]] + bu[l[1]] + dot(lu[l[1]], li[l[0]])
		if predict > 5:
			predict = 5
		if predict < 0:
			predict = 0
		error += (predict - l[2]) * (predict - l[2])
		sample += 1
	print "Valid MSE:", error/sample
	print "Sample:", sample
	# if e1 - error/sample < 0.000001:
	if e1 < 0.65:
		break
	e1 = error/sample

# predictions = open("predictions_Rating.txt", 'w')
# for l in open("pairs_Rating.txt"):
	# if l.startswith("userID"):
		# #header
		# predictions.write(l)
		# continue
	# User,Item = l.strip().split('-')
	# try:
		# i = Itemlist.index(Item)
	# except:
		# i = -1
	# try:
		# u = Userlist.index(User)
	# except:
		# u = -1
	# predict = a + bu[u] + bi[i]	+ dot(li[l[0]], lu[l[1]])
	# if predict > 5:
		# predict = 5
	# predictions.write(User + '-' + Item + ',' + str(predict) + '\n')

# predictions.close()