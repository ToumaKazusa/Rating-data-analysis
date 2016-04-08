import gzip
import unicodedata
import sys
import re
from collections import defaultdict
from string import punctuation
 


t = 0	
Item = []
User = []
for l in readGz("train.json.gz"):
	It = l['itemID']
	U = l['reviewerID']
	try:
		Item.index(It)
	except:
		Item.append(It)
		fi.write(It+'\n')
	try:
		User.index(U)
	except:
		User.append(U)
		fu.write(U+'\n')	
	t += 1
	print t
