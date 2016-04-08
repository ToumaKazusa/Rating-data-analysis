import random
import gzip
import unicodedata
import sys
import re
from collections import defaultdict
from string import punctuation
 
		
fs = open('Word1.txt', 'r')
Text = []
Time = []
while True:
	l = fs.readline()
	ld = l.split()
	if len(ld) <= 1:
		break
	Text.append(ld[0])
	Time.append(int(ld[1]))
fs.close()
print len(Text)

i = 0
while i < len(Text):
	if Time[i] < 30 or  Time[i] > 300:
		del Time[i]
		del Text[i]
	else:
		i += 1

i = 0		
while i < len(Text) - 1:
	if Text[i]+'S' == Text[i + 1]:
		del Time[i + 1]
		del Text[i + 1]
	elif Text[i].rstrip('E')+'ED' == Text[i + 1]:
		del Time[i + 1]
		del Text[i + 1]
	elif Text[i].rstrip('E')+'ES' == Text[i + 1]:
		del Time[i + 1]
		del Text[i + 1]
	elif Text[i].rstrip('E')+'ING' == Text[i + 1]:
		del Time[i + 1]
		del Text[i + 1]
	elif Text[i].rstrip('E')+'ION' == Text[i + 1]:
		del Time[i + 1]
		del Text[i + 1]
	elif Text[i]+'LY' == Text[i + 1]:
		del Time[i + 1]
		del Text[i + 1]
	else:
		i += 1		

random.shuffle(Text)
print len(Text)
		
fs = open("Feature", 'w')
for l in Text:
	fs.write(l)
	fs.write('\n')
fs.close()	