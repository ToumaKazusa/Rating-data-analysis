import gzip
import random
import unicodedata
import sys
import re
import numpy
from numpy import dot
from numpy.linalg import inv
from math import exp
from math import log
from collections import defaultdict
from string import punctuation

r = []
for i in range(0, 10):
	r.append(i)
print r
random.shuffle(r)
print r
for i in r:
	print i

def readGz(f):
	for l in gzip.open(f):
		yield eval(l)

t = 0
y = []
x = []
for l in readGz("train.json.gz"):
	help = l['helpful']
	t += 1
	if help['outOf'] == 0:
		continue
	if t > 100000:
		break
	Text = l['reviewText']
	Sum = l['summary']
	Cat = l['category']
	Time = l['unixReviewTime']/100000000.0 - 10
	x.append([1])
	x[-1].append(len(Text.split()))
	x[-1].append(len(Sum.split()))
	x[-1].append(len(Cat))
	x[-1].append(Time)
	x[-1].append(l['rating'])
	y.append(help['nHelpful']/float(help['outOf']))

x = numpy.array(x)
y = numpy.array(y)
theta = dot(dot(inv(dot(x.T, x)), x.T), y)	
print theta
	
# t = 0
# e1 = 0
# e2 = 0
# s = 0
# for l in readGz("train.json.gz"):
	# help = l['helpful']
	# t += 1
	# if help['outOf'] == 0:
		# continue
	# if t <= 100000:
		# continue
	# if t > 200000:
		# break
	# Text = l['reviewText']
	# Sum = l['summary']
	# Cat = l['category']
	# Time = l['unixReviewTime']/100000000.0 - 10
	# x1 = numpy.array([1, len(Text.split()), len(Sum), l['rating']])
	# a = dot(theta, x1)
	# e1 += abs(help['nHelpful'] - help['outOf']*a)
	# e2 += abs(help['nHelpful']/float(help['outOf']) - a)
	# s += 1
	
predictions = open("predictions_Helpful.txt", 'w')
for l in readGz("helpful.json.gz"):
  	help = l['helpful']
	Text = l['reviewText']
	Sum = l['summary']
	Cat = l['category']
	Time = l['unixReviewTime']/100000000.0 - 10
	if help['outOf'] == 0 :
		predictions.write(l["reviewerID"] + '-' + l["itemID"]  + '-' + '0' + ',' + '0' + '\n')
		continue
	x = [1, len(Text.split()), len(Sum), len(Cat), Time, l['rating']]
	x = numpy.array(x)
	predict = dot(theta, x)*help['outOf']
	if predict > help['outOf']:
		predict = help['outOf']
	predictions.write(l["reviewerID"] + '-' + l["itemID"]  + '-' + str(help['outOf']) + ',' + str(predict) + '\n')