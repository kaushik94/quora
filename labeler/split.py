import sys
import random

try:
	P = float( sys.argv[1] )
except IndexError:
	P = 0.9
	
print "P = %s" % ( P )


filename = 'labeler_sample.in'
fp_in = open(filename, 'r')
train_n, test_n = map(int, fp_in.readline().split())
writer  = open('test.in', 'w')
actual    = open('actual.txt', 'w')
# predict   = open('predict.txt', 'w')
trainingdata = []
actuals = []
queries = []


for i in xrange(train_n):
	topics = fp_in.readline()
	question = fp_in.readline()
	r = random.random()
	if r < P:
		trainingdata.append(topics+question)
	else:
		actuals.append(topics)
		queries.append(question)

N, n = len(trainingdata), len(queries)
writer.write(str(N)+" "+str(n)+"\n")
for i in xrange(len(trainingdata)):
	writer.write(trainingdata[i])

for i in xrange(len(queries)):
	writer.write(queries[i])
	actual.write(actuals[i])

# print queries
