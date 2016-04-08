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
for l in parseData('trainwithcata.json'):
	print l
	raw_input()

		
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
