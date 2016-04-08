import gzip
import unicodedata
import sys
import re
from collections import defaultdict
from string import punctuation
 

def parseData(fname):
  for l in open(fname):
    yield eval(l)

Wordlist = []		
Timelist = []
t = 0
num = 0
for l in parseData("beer_50000.json"):
	t += 1
	print t
	if(t > 5000):
		break
	Text = l['review/text']
	for i in punctuation:
		Text = Text.replace(i, ' ')
	Text = Text.split()
	for i in Text:
		s = i.lower()
		print s
		try:
			j = Wordlist.index(s)
			Timelist[j] += 1
		except:
			Wordlist.append(s)
			Timelist.append(1)

print len(Wordlist)			
fs = open('Wordlist.txt', 'w')
for i in range(0, len(Wordlist)):
	fs.write(Wordlist[i] + '\t' + str(Timelist[i]) + '\n')
fs.close()

print 