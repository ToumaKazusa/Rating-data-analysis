import gzip
import unicodedata
import sys
import re
import numpy
from collections import defaultdict
from string import punctuation

def readGz(f):
	for l in gzip.open(f):
		yield eval(l) 
		
Userlist = []
Itemlist = []
Buy = []
Sell = []
Rate_User = []
Rate_Item = []
Valid = []

t = 0
for l in readGz("train.json.gz"):
	t += 1
	print t
	Item = l["itemID"]
	User = l["reviewerID"]
	Rate = l["rating"]
	if t > 900000:
		Valid.append([Item, User, Rate])
	else:
		Item = l["itemID"]
		User = l["reviewerID"]
		Rate = l["rating"]
		try:
			i = Itemlist.index(Item)
		except:
			i = len(Itemlist)
			Itemlist.append(Item)
			Sell.append([])
			Rate_Item.append([])
		try:
			u = Userlist.index(User)
		except:
			u = len(Userlist)
			Userlist.append(User)
			Buy.append([])
			Rate_User.append([])
		Buy[u].append(i)
		Sell[i].append(u)
		Rate_User[u].append(Rate)
		Rate_Item[i].append(Rate)
		
n = len(Userlist)
m = len(Itemlist)
	
fs = open("Userlist", "w")
for i in range(0, n):
	fs.write(Userlist[i]+"\n")
fs.close()

fs = open("Buy", "w")
for i in range(0, n):
	for j in range(0, len(Buy[i])):
		fs.write(str(Buy[i][j])+"\t")
	fs.write("\n")
fs.close()

fs = open("Rate_User", "w")
for i in range(0, n):
	for j in range(0, len(Rate_User[i])):
		fs.write(str(Rate_User[i][j])+"\t")
	fs.write("\n")
fs.close()

fs = open("Itemlist", "w")
for i in range(0, m):
	fs.write(Itemlist[i]+"\n")
fs.close()	

fs = open("Sell", "w")
for i in range(0, m):
	for j in range(0, len(Sell[i])):
		fs.write(str(Sell[i][j])+"\t")
	fs.write("\n")
fs.close()

fs = open("Rate_Item", "w")
for i in range(0, m):
	for j in range(0, len(Rate_Item[i])):
		fs.write(str(Rate_Item[i][j])+"\t")
	fs.write("\n")
fs.close()

fs = open("Rate_Valid", "w")
for i in range(0, len(Valid)):
	fs.write(Valid[i][0] + "\t" + Valid[i][1]+ "\t" + str(Valid[i][2]) + "\n")
fs.close()

print "User:", n
print "Item:", m
print "Done!"