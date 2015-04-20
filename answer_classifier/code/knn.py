import numpy as np
from sklearn.preprocessing import normalize

from sklearn import linear_model
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
from sklearn import svm

from sklearn.ensemble import AdaBoostClassifier

knn_scikit = KNeighborsClassifier(n_neighbors=13)
pca = PCA()

test_file = open('../data/test_input.csv', 'r')
train_file = open('../data/input_.csv', 'r')
output_file = open('../data/test_output_knn.txt', 'w')


def run_knn():
	test = []
	train = []
	ids = []
	results = []
	for each in test_file:
		each = each.split(',')
		ids.append(each[0])
		test.append(map(float, each[1:]))
	test = np.array(test)
	# print test
	# print normalize(test)
	for each in train_file:
		each = each.split(',')
		results.append(int(each[-1]))
		train.append(map(float, each[1:-1]))
	# print train
	# print normalize(train)
	# print np.array(results)
	"""
	pca.fit(train)
	test = pca.transform(test)
	train = pca.transform(train)
	knn_scikit.fit(train, results)
	out = knn_scikit.predict(test)
	clf = svm.SVC(kernel='rbf')
	clf.fit(train, results)
	out = clf.predict(test)
	"""
	clf = svm.LinearSVC(C=0.01, penalty="l1", dual=False)
	clf.fit(train, results)
	out = clf.predict(test)

	classifier = AdaBoostClassifier(n_estimators=200)
	classifier.fit(train, results)
	out = classifier.predict(test)
	# print [i for i, e in enumerate(clf.coef_[0]) if e != 0 and abs(e) > 1e-6]
	for i in xrange(len(out)):
		result = transform(int(out[i]))
		output_file.write(str(ids[i])+" "+result+"\n")

run_knn()
