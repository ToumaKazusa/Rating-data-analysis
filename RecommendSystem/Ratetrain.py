import gzip
import random
import numpy
from math import pow
from collections import defaultdict

def readGz(f):
  for l in gzip.open(f):
    yield eval(l)

userlist = []	
user = []
buy = []
itemlist = []
item = []
sell = []
t = 0
for l in readGz("train.json.gz"):
	u = l["reviewerID"]
	i = l["itemID"]
	try:
		j = userlist.index(u)
	except:
		userlist.append(u)
		user.append([])
		buy.append([])
		j = len(userlist) - 1
	try:
		k = itemlist.index(i)
	except:
		itemlist.append(i)
		item.append([])
		sell.append([])
		k = len(itemlist) - 1
	user[j].append(k)
	buy[j].append(float(l["rating"]))
	item[k].append(j)
	sell[k].append(float(l["rating"]))	
	t = t + 1
	if t >= 100000:
		break

a = 0
bu = [0]*len(userlist)
n = len(bu)
bi = [0]*len(item)
m = len(bi)
minerror = 1
for t in range(0, 10):
	rate = 0
	for i in buy:
		rate += sum(i)
	for i in range(0, n):
		rate -= bu[i] * len(buy[i])
	for i in range(0, m):
		rate -= bi[i] * len(sell[i])
	a = rate / 100000
	
	for i in range(0, n):
		bu[i] = sum(buy[i])
		bu[i] -= len(buy[i]) * a  
		for j in user[i]:
			bu[i] -= bi[j]
		bu[i] /= (len(buy[i]) + 10)
	
	for i in range(0, m):
		bi[i] = sum(sell[i])
		bi[i] -= len(sell[i]) * a  
		for j in item[i]:
			bi[i] -= bu[j]
		bi[i] /= (len(sell[i]) + 10)
	
	error = 0
	for i in range(0, n):
		for j in range(0, len(buy[i])):
			error += pow((buy[i][j] - a - bu[i] - bi[user[i][j]]), 2)
	error /= 100000
	print "Train MSE:", error
	# if  error < minerror - 0.000001:
		# minerror = error
	# else:
		# break

bu.append(sum(bu)/len(bu))
bi.append(sum(bi)/len(bi))
error = 0
t = 0		
# for l in readGz("train.json.gz"):
	# t = t + 1
	# if t <= 100000:
		# continue
	# if t > 200000:
		# break
	# try:
		# u = userlist.index(l["reviewerID"])
	# except:
		# u = -1
	# try:
		# i = itemlist.index(l["itemID"])
	# except:
		# i = -1
	# r = float(l['rating'])
	# error += pow((r - a - bi[i] - bu[u]), 2)
# error /= 100000
# print 'MSE:', error

predictions = open("predictions_Rating.txt", 'w')
for l in open("pairs_Rating.txt"):
  if l.startswith("userID"):
    #header
    predictions.write(l)
    continue
  u,i = l.strip().split('-')
  try:
	u1 = userlist.index(u)
  except:
	u1 = -1
  try:
	i1 = itemlist.index(i)
  except:
	i1 = -1
  predictions.write(u + '-' + i + ',' + str(a + bi[i1] + bu[u1]) + '\n')
  
predictions.close()
	
	


# print "max(bu):", userlist[bu.index(max(bu))], max(bu)
# print "min(bu):", userlist[bu.index(min(bu))], min(bu) 
# print "max(bi):", itemlist[bi.index(max(bi))], max(bi) 
# print "min(bi):", itemlist[bi.index(min(bi))], min(bi) 
