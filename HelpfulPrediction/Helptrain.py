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
print "Done!"
		
theta = [0]*(m + 3)	
theta[0] = 0.4587
theta[1] = 0.0001422 	
theta[2] = 0.05971
# theta = numpy.array(theta)
# theta = []
# fs = open('Weight', 'r')
# while True:
	# l = fs.readline()
	# ld = l.split()
	# if len(ld) < 1:
		# break
	# theta.append(float(ld[0]))
# fs.close()
# for i in range(3, 2003):
	# theta[i] += random.uniform(-0.01,  0.01) 
theta = numpy.array(theta)
# x1 = numpy.array(x[:25000])
# x2 = numpy.array(x[25001:])
# y1 = numpy.array(y[:25000])
# y2 = numpy.array(y[25001:])
# error = 0
# sample = 0
# for i in range(0, 10000):
	# predict = numpy.dot(theta, x[i])
	# error += abs(y[i] - predict)
	# sample += 1 
# print "Train error:", error/sample, "\tSample:", sample
# raw_input()
# inv = numpy.linalg.inv(numpy.dot(x.T, x))
# theta = numpy.dot(numpy.dot(inv, x.T), y) 
for t in range(0, 3):
	for i in range(0, n):
		x1 = numpy.array(x[i])
		p = numpy.dot(theta, x1)
		if p > 1:
			p = 1
		if p < 0:
			p = 0
		for j in range(3, m + 3):
			theta[j] += 0.001*(y[i] - p)*x1[j]
	error = 0
	sample = 0
	print t	
	for i in range(0, n):
		x1 = numpy.array(x[i])
		predict = numpy.dot(theta, x1)
		error += abs(y[i] - predict)
		sample += 1 
	print "Train error:", error/sample, "\tSample:", sample

print len(theta)
		
print 'Finish Train'
fs = open("Weight1", 'w')
for i in range(0, m + 3):
	fs.write(str(theta[i]))
	fs.write('\n')
fs.close()
	
# t = 0
# terror = 0
# tsample = 0
# verror = 0
# vsample = 0
# for l in readGz("train.json.gz"):
	# help = l['helpful']
	# if help['outOf'] == 0:
		# continue
	# Text = l['reviewText']
	# Text = Text.upper()
	# t += 1
	# print t
	# if t <= 10000:	
		# x0 = [1]
		# x0.append(l['rating'])
		# x0.append(len(Text.split()))
		# for j in feature:
			# if Text.find(j) == -1:
				# x0.append(0)
			# else:
				# x0.append(1)
		# x0 = numpy.array(x0)
		# print x0
		# predict = numpy.dot(theta, x0)
		# print predict
		# raw_input()
		# terror += abs(help['nHelpful']/float(help['outOf']) - predict)
		# tsample += 1 
	# else:
		# if help['outOf'] > 0:
			# x0 = numpy.array([1, len(Text), rate])
			# verror += abs(help['nHelpful']/float(help['outOf']) - numpy.dot(theta, x0))
			# vsample += 1 
		# break;

# print "Test error:", terror/tsample, "\tSample:", tsample 
# print "Valid error:", verror/vsample, "\tSample:", vsample
		