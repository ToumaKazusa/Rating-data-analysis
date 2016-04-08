import gzip
import unicodedata
import sys
import re
import numpy
from collections import defaultdict
from string import punctuation

def readGz(f):
	for l in gzip.open(f):
		yield eval(l) 
		
fs = open('Feature', 'r')
feature = []
while True:
	l = fs.readline()
	ld = l.split()
	if len(ld) < 1:
		break
	feature.append(ld[0])
fs.close()

theta = []
fs = open('Weight1', 'r')
while True:
	l = fs.readline()
	ld = l.split()
	if len(ld) < 1:
		break
	theta.append(float(ld[0]))
fs.close()
theta = numpy.array(theta)

predictions = open("predictions_Helpful.txt", 'w')
for l in readGz("helpful.json.gz"):
  	help = l['helpful']
	Text = l['reviewText']
	if help['outOf'] == 0 :
		predictions.write(l["reviewerID"] + '-' + l["itemID"]  + '-' + '0' + ',' + '0' + '\n')
		continue
	x = [1, len(Text.split()), l['rating']]
	Text = Text.upper()
	for j in feature:
		if Text.find(j) == -1:
			x.append(0)
		else:
			x.append(1)
	x = numpy.array(x)
	predict = numpy.dot(theta, x)*help['outOf']
	if predict > help['outOf']:
		predict = help['outOf']
	predictions.write(l["reviewerID"] + '-' + l["itemID"]  + '-' + str(help['outOf']) + ',' + str(predict) + '\n')
		