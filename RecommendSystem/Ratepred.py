import gzip
import unicodedata
import sys
import re
import numpy
from collections import defaultdict
from string import punctuation
from math import pow

Userlist = []
Itemlist = []
Buy = []
Sell = []
Rate_User = []
Rate_Item = []
Valid = []

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
fs.close()


print "Done!"
		
n = len(Userlist)
m = len(Itemlist)

predictions = open("predictions_Rating.txt", 'w')
for l in open("pairs_Rating.txt"):
	if l.startswith("userID"):
		#header
		predictions.write(l)
		continue
	User,Item = l.strip().split('-')
	try:
		i = Itemlist.index(Item)
		predict = sum(Rate_Item[i]) / len(Rate_Item[i])
	except:
		u = Userlist.index(User)
		predict = sum(Rate_User[u]) / len(Rate_User[u])
	predictions.write(User + '-' + Item + ',' + str(predict) + '\n')

predictions.close()

