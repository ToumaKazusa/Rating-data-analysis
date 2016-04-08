import numpy
import urllib
import scipy.optimize
import random
from collections import defaultdict
import nltk
import string
from nltk.stem.porter import *
from sklearn import linear_model

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
	
biCount = defaultdict(int)
for d in data:
	r = ''.join([c for c in d['review/text'].lower() if not c in punctuation])
	s = '<st>'
	for w in r.split():
		try:
			biCount[s + ' ' + w] += 1
			s = w
		except:
			print s + ' ' + w
			print len(biCount)
			
item = biCount.items()
item = sorted(item, key = lambda d:d[1], reverse = True)
print item[0:5]
bigrams = [x[0] for x in item[:1000]]
bigramId = dict(zip(bigrams, range(len(bigrams))))
bigramSet = set(bigrams)

def feature(datum):
	feat = [0]*len(bigrams)
	r = ''.join([c for c in datum['review/text'].lower() if not c in punctuation])
	s = '<st>'
	for w in r.split():
		if s + ' ' + w in bigrams:
			feat[bigramId[s + ' ' + w]] += 1
		s = w
	feat.append(1) #offset
	return feat

X = [feature(d) for d in data]
y = [d['review/overall'] for d in data]

clf = linear_model.Ridge(1.0, fit_intercept=False)
clf.fit(X, y)
theta = clf.coef_
predictions = clf.predict(X)

mse = 0
mae = 0
for i in range(len(predictions)):
	mse += (predictions[i] - y[i]) * (predictions[i] - y[i])
	mae += abs(predictions[i] - y[i])
print "Bigram MSE:", mse/5000
print "Bigram MAE:", mae/5000



# t1 = [(theta[w], bigrams[w]) for w in range(1000)]
# t1.sort()
# print "Most negative bigram:", t1[:5]
# print "Most positive bigram:", t1[995:]




counts = [(wordCount[w], w) for w in wordCount]
counts.sort()
counts.reverse()

words = [x[1] for x in counts[:1000]]
wordId = dict(zip(words, range(len(words))))
wordSet = set(words)

def feature1(datum):
	feat = [0]*len(words)
	r = ''.join([c for c in datum['review/text'].lower() if not c in punctuation])
	s = '<st>'
	for w in r.split():
		if w in words:
			feat[wordId[w]] += 1
		s = w
	feat.append(1) #offset
	return feat
	
X1 = [feature1(d) for d in data]

clf1 = linear_model.Ridge(1.0, fit_intercept=False)
clf1.fit(X1, y)
theta1 = clf1.coef_
predictions = clf1.predict(X1)


mse = 0
mae = 0
for i in range(len(predictions)):
	mse += (predictions[i] - y[i]) * (predictions[i] - y[i])
	mae += abs(predictions[i] - y[i])
print "Unigram MSE:", mse/5000
print "Unigram MAE:", mae/5000


# t1 = [(theta1[w], words[w]) for w in range(1000)]
# t1.sort()
# print "Most negative unigram:", t1[:5]
# print "Most positive unigram:", t1[995:]

def feature2(datum):
	feat = [0]*(len(words) + len(bigrams))
	r = ''.join([c for c in datum['review/text'].lower() if not c in punctuation])
	s = '<st>'
	for w in r.split():
		if w in words:
			feat[wordId[w]] += 1
		if s + ' ' + w in bigrams:
			feat[len(words) + bigramId[s + ' ' + w]] += 1
		s = w
	feat.append(1) #offset
	return feat

X2 = [feature2(d) for d in data]

clf2 = linear_model.Ridge(1.0, fit_intercept=False)
clf2.fit(X2, y)
theta2 = clf2.coef_
predictions = clf2.predict(X2)

# mse = 0
# for i in range(len(predictions)):
	# mse += (predictions[i] - y[i]) * (predictions[i] - y[i])
# print mse/5000


mix = [(abs(theta2[w]), words[w]) for w in range(1000)] + [(abs(theta2[w + 1000]), bigrams[w]) for w in range(1000)]
mix.sort(reverse = True)
mix = [x[1] for x in mix[0:1000]]
mixId = dict(zip(mix, range(len(mix))))

def feature3(datum):
	feat = [0]*len(mix)
	r = ''.join([c for c in datum['review/text'].lower() if not c in punctuation])
	s = '<st>'
	for w in r.split():
		if w in mix:
			feat[mixId[w]] += 1
		if s + ' ' + w in mix:
			feat[mixId[s + ' ' + w]] += 1
		s = w
	feat.append(1) #offset
	return feat

X3 = [feature3(d) for d in data]

clf3 = linear_model.Ridge(1.0, fit_intercept=False)
clf3.fit(X3, y)
theta3 = clf3.coef_
predictions = clf3.predict(X3)	

t1 = [(theta3[w], mix[w]) for w in range(1000)]
t1.sort()
print "Most negative unigram:", t1[:10]
print "Most positive unigram:", t1[990:]


mse = 0
mae = 0
for i in range(len(predictions)):
	mse += (predictions[i] - y[i]) * (predictions[i] - y[i])
	mae += abs(predictions[i] - y[i])
print "Mix MSE:", mse/5000
print "Mix MAE:", mae/5000
