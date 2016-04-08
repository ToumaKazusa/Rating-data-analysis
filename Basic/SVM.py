import gzip
import unicodedata
import sys
import re
from collections import defaultdict
from string import punctuation

fi = open("Itemlist", "r")
fu = open("Userlist", "r")
item = []
user = []
while True:
	l = fi.readline()
	l = l.split('\n')
	if len(l[0]) > 0:
		item.append(l[0])
	else: 
		break
while True:
	l = fu.readline()
	l = l.split('\n')
	if len(l[0]) > 0:
		user.append(l[0])
	else: 
		break
fi.close()
fu.close()


rank_user = []
rank_item = []
for i in range(0, len(user)):
	rank_user.append([])
for i in range(0, len(item)):
	rank_item.append([])
	
def readGz(f):
	for l in gzip.open(f):
		yield eval(l) 

t = 0	
for l in readGz("train.json.gz"):
	r = l['rating']
	reviewer = l['reviewerID']
	itemid = l['itemID']
	p = user.index(reviewer)
	q = item.index(itemid)
	rank_user[p].append(r)
	rank_item[q].append(r)
	t += 1
	print t

fp = open('Rank_user', 'w')	
for i in rank_user:
	for j in i:
		fp.write(str(j))
		fp.write('\t')
	fp.write('\n')
fp.close()

fp = open('Rank_item', 'w')	
for i in rank_item:
	for j in i:
		fp.write(str(j))
		fp.write('\t')
	fp.write('\n')
fp.close()



