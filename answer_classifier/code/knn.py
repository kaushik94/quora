
test_file = open('../data/test_input.csv', 'r')
train_file = open('../data/input_.csv', 'r')
output_file = open('../data/test_output_knn.txt', 'w')

def get_dist(A, B):
	if len(A) != len(B):
		print "something wrong, lengths of vectors not equal"
		return 1
	dist = 0
	for i in xrange(len(A)):
		dist += (A[i] - B[i])**2
	return dist**0.5

def get_best(k, Q):
	Q = sorted(Q)
	if k > len(Q):
		best = Q
	else:
		best = Q[:k]
	# print len(best)
	poss = 0
	negs = 0
	for each in best:
		x = each[1].strip('\r\n')
		if x == '+1':
			poss += 1
		else:
			negs += 1
	print poss, negs
	if poss > negs:
		return '+1'
	return '-1'

def knn(test, train, k):
	results = []
	for each in test:
		id_ = each[0]
		features = map(float, each[1:])
		Q = []
		for one in train:
			fea = map(float, one[1:-1])
			result = one[-1]
			score = get_dist(features, fea)
			Q.append((score, result))
		best_k = get_best(k, Q)
		results.append((id_, best_k))
	return results

def run_knn():
	test = []
	train = []
	for each in test_file:
		each = each.split(',')
		test.append(each)
	for each in train_file:
		each = each.split(',')
		train.append(each)
	results = knn(test, train, 5)
	for each in results:
		output_file.write(str(each[0])+" "+str(each[1])+"\n")

run_knn()
