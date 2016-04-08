import gzip
import unicodedata
import sys
import re
from collections import defaultdict
from string import punctuation
 

def readGz(f):
	for l in gzip.open(f):
		yield eval(l)
	
# Wordlist = []
# Timelist = []
fs = open('Wordlist.txt', 'w')
t = 0
num = 0
for l in readGz("train.json.gz"):
	Text = l['reviewText']
	for i in punctuation:
		Text = Text.replace(i, ' ')
	Text = Text.split()
	for i in Text:
		if len(i) < 3:
			continue
		str = i.upper()
		fs.write(str)
		fs.write('\n')
		num += 1
	t += 1
	print t
	if(t > 100000):
		break
print num
fs.close()

