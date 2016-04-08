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

### Just the first 5000 reviews

print "Reading data..."
data = list(parseData("processed_data.json"))[:100000]
print "done"



punctuation = set(string.punctuation)
t = 0
count = [0] * 101
for d in data:
	t = t + 1
	r = ''.join([c for c in d['reviewText'].lower() if not c in punctuation])
	c = len(r.split())
	print t
	c = c/10
	if c >= 100:
		c = 99
	count[c] += 1

	
print count
raw_input()

### Ignore capitalization and remove punctuation, with stemming, remove stopwords

wordCount = defaultdict(int)
punctuation = set(string.punctuation)
stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
stemmer = PorterStemmer()
t = 0
for d in data:
	t = t + 1
	print t
	r = ''.join([c for c in d['reviewText'].lower() if not c in punctuation])
	for w in r.split():
		if w in stopwords:
			continue
		# w = stemmer.stem(w)
		wordCount[w] += 1

print len(wordCount)


### Just take the most popular words...

counts = [(wordCount[w], w) for w in wordCount]
counts.sort()
counts.reverse()

words = [x[1] for x in counts[:1000]]
wordId = dict(zip(words, range(len(words))))
wordSet = set(words)

### Sentiment analysis
def feature(datum):
	feat = [0]*len(words)
	r = ''.join([c for c in datum['reviewText'].lower() if not c in punctuation])
	for w in r.split():
		if w in words:
			feat[wordId[w]] += 1
	feat.append(1) #offset
	return feat

X = [feature(d) for d in data]
fs = open("TFdata.txt", "w")
for item in X:
	pre = str(item)
	pre = pre.replace("[", "")
	pre = 	pre.replace("]", "\n")
	fs.write(pre)

#No regularization
#theta,residuals,rank,s = numpy.linalg.lstsq(X, y)

#With regularization
# clf = linear_model.Ridge(1.0, fit_intercept=False)
# clf.fit(X, y)
# theta = clf.coef_
# predictions = clf.predict(X)

# mse = 0
# for i in range(len(predictions)):
	# mse += (predictions[i] - y[i]) * (predictions[i] - y[i])
# print mse