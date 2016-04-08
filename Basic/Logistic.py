import gzip
import unicodedata
import sys
import re
import numpy
import random
from math import exp
from math import log
from collections import defaultdict
from string import punctuation


def readGz(f):
	for l in gzip.open(f):
		yield eval(l)

def sigmoid(f):
	try:
		return 1/(1 + exp(-f))
	except:
		return 1
	
def gradient(x, y, w):
	n = len(y)
	m = len(w)
	grad = [0]*m
	for i in range(0, n):
		p = sigmoid(numpy.dot(x[i], w))
		for j in range(0, m):
			grad[j] -= (y[i] - p)*x[i][j]
	for j in range(0, m):
		grad[j] *= 0.001
	
	return grad
	
t = 0
k = -1
y = []
x = []
for l in readGz("train.json.gz"):
	t += 1
	print t
	if t > 10000:		
		break
	help = l['helpful']
	Text = l['reviewText']
	if help['outOf'] == 0:
		continue
	k += 1
	y.append(help['nHelpful']/float(help['outOf']))
	y[k] = 2 * y[k] - 1 
	x.append([1])
	x[k].append(l['rating'])
	x[k].append(len(Text.split()))
	Text = Text.upper()
print "Done!"

theta = [0]*3
while 1:
	grad = gradient(x, y, theta)
	for i in range(0, 3):
		theta[i] += grad[i]
	print grad