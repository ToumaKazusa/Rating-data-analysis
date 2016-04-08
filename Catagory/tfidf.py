import numpy
import urllib
import scipy.optimize
import random
from collections import defaultdict
import nltk
import string
import math
from nltk.stem.porter import *
from sklearn import linear_model
from numpy import dot
from scipy import spatial

def parseData(fname):
	for l in open(fname):
		yield eval(l)


print "Reading data..."
data = list(parseData("beer_50000.json"))[:5000]
print "done"

wordCount = defaultdict(int)
punctuation = set(string.punctuation)
for d in data:
	r = ''.join([c for c in d['review/text'].lower() if not c in punctuation])
	for w in r.split():
		wordCount[w] += 1
		
words = [(w) for w in wordCount]
# words = ["foam", "smell", "banana", "lactic", "tart"]
wordId = dict(zip(words, range(len(words))))


def feature(datum):
	feat = [0]*len(words)
	r = ''.join([c for c in datum['review/text'].lower() if not c in punctuation])
	for w in r.split():
		if w in words:
			feat[wordId[w]] += 1
	print sum(feat)
	return feat

def idf(datum):
	n = len(datum)
	d = [0] * n
	for i in range(n):
		if datum[i] > 0:
			d[i] = 1
	d1 = numpy.log10(n/float(sum(d)))
	return d1

f = [feature(d) for d in data]
print "Done!"
	
idfs = map(idf,zip(*f))	
x = f[0][:]
for i in range(len(idfs)):
	x[i] *= idfs[i]
print x[:1000]
	
max = 0
maxId = 0
for i in range(1, 5000):
	y = f[i][:]
	if sum(y) == 0:
		continue
	for j in range(len(y)):
		y[j] *= idfs[j]
	c = 1 - spatial.distance.cosine(x, y)	
	print i
	if i == 1:
		print c
		raw_input()
	if i == 2343:
		print c
		raw_input()
	if c > max:
		max = c
		maxId = i
		
print max, maxId
print data[0]['review/text']
print data[maxId]['review/text']
# print "Similarity 0 & 1:", cossim(tfidf[0], tfidf[1])
	
# max = 0
# maxId = 0
# for i in range(1, 5000):
	# c = cossim(tfidf[0], tfidf[i])
	# if c > max:
		# max = c
		# maxId = i
