import gzip
import unicodedata
import sys
import re
import json
from collections import defaultdict
from string import punctuation
 
def readGz(f):
	for l in gzip.open(f):
		yield eval(l)

def parseData(fname):
	for l in open(fname):
		yield eval(l)

t = 0
Data = []
# fs = open('trainwithcata.json', 'w')
# for l in readGz("trainwithcata.json.gz"):
for l in parseData('trainwithcata.json'):
	catagory = l['category']
	t += 1
	print l
	raw_input()
	if len(catagory) > 1:
		json.dump(l, open('trainwithcata.json','a'))
		fs = open('trainwithcata.json','a')
		fs.write('\n')
		fs.close()
	# print l
	# raw_input()
	# print catagory

		
# with open('trainwithcata.json', 'w') as outfile:
	# json.dump(Data, outfile)

	# for i in catagory:
		# for j in i:
			# try:
				# Allcatagory.index(j)
			# except:
				# Allcatagory.append(j)
	# print t	
	
# fs = open("Catagory.txt", 'w')
# for i in Allcatagory:
	# fs.write(i)
	# fs.write('\n')
# fs.close()	
