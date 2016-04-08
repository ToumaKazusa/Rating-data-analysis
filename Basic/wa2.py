import gzip
import unicodedata
import sys
import re
from collections import defaultdict
from string import punctuation
 

def readGz(f):
	for l in gzip.open(f):
		yield eval(l)
	
Wordlist = []
Timelist = []

for l in readGz("train.json.gz"):
	Text = l['reviewText']
	for i in punctuation:
		Text = Text.replace(i, ' ')
	Text = Text.split()
	n = len(Text)
	for i in range(0, n):
		str = Text[i].upper()
		try:
			idx = Wordlist.index(str)
			Timelist[i] += 1
		except:
			Wordlist.append(str)
			Timelist.append(1)


fs = open('Wordlist.txt', 'w')
t = 0
for i in Wordlist:
	fs.write(fs)
	fs.write('\t')
	fs.write(str(Timelist[t]))
	fs.write('\n')
	t = t + 1