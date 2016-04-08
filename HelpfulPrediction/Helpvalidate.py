import gzip
import random
import numpy
from collections import defaultdict

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
### Helpfulness baseline: similar to the above. Compute the global average helpfulness rate, and the average helpfulness rate for each user
# theta = theta[:3]

t = 0
sample = 0
error = 0
for l in readGz("train.json.gz"):
  	help = l['helpful']
	Text = l['reviewText']
	t += 1
	if t > 200000:		
		break
	if help['outOf'] == 0 or t <= 100000:
		continue
	y = help['nHelpful']/float(help['outOf'])
	x = [1, len(Text.split()), l['rating']]
	Text = Text.upper()
	for j in feature:
		if Text.find(j) == -1:
			x.append(0)
		else:
			x.append(1)
	x = numpy.array(x)
	predict = numpy.dot(theta, x)
	error += abs(y - predict)
	sample += 1
print "Done!"
print "Train error:", error/sample, "\tSample:", sample






