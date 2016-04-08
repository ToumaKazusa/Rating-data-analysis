import gzip
import random
import unicodedata
import sys
import re
import numpy
from math import exp
from math import log
from collections import defaultdict
from string import punctuation
from sklearn.decomposition import PCA
from collections import defaultdict
from numpy.linalg import eig as eigenValuesAndVectors
from numpy import dot


fs = open('Feature', 'r')
feature = []
while True:
	l = fs.readline()
	ld = l.split()
	if len(ld) < 1:
		break
	feature.append(ld[0])
fs.close()
print len(feature)

def readGz(f):
	for l in gzip.open(f):
		yield eval(l)
		
t = 0
k = -1
y = []
x = []
for l in readGz("train.json.gz"):
	help = l['helpful']
	Text = l['reviewText']
	t += 1
	if t == 100000:		
		break
	if help['outOf'] == 0:
		continue
	k += 1
	y.append(help['nHelpful']/float(help['outOf']))
	x.append([1])
	x[k].append(len(Text.split()))
	x[k].append(l['rating'])
	Text = Text.upper()
	for j in feature:
		if Text.find(j) == -1:
			x[k].append(0)
		else:
			x[k].append(1)
n = len(x)
m = len(feature)
x = numpy.array(x)
pca = PCA(n_components = 50)
pca.fit(x)
print pca.components_
print pca.explained_variance_ratio_
print "Done!"