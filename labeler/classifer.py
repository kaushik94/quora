import operator

stopwords = ['a',
# 'able',
'about',
'across',
'after',
'all',
'almost',
'also',
'am',
'among',
'an',
'and',
'any','are','as','at','be','because','been','but','by','can',
             'cannot','could','dear','did','do','does','either','else','ever','every',
             'for','from','get','got','had','has','have','he','her','hers','him','his',
             'how','however','i','if','in','into','is','it','its','just','least','let',
             'like','likely','may','me','might','most','must','my','neither','no','nor',
           'not','of','off','often','on','only','or','other','our','own','rather','said',
             'say','says','she','should','since','so','some','than','that','the','their',
             'them','then','there','these','they','this','tis','to','too','twas','us',
             'wants','was','we','were','what','when','where','which','while','who',
             'whom','why','will','with','would','yet','you','your']

TOP_TOPICS = [
    183,
    29,
    189,
    78,
    159,
    142,
    147,
    190,
    45,
    124,
]


# stopwords = ['the', 'a', '.', ',', ' ', 'and', 'of', 'are', 'in', 'for', 'on', 'i', 'you', 'me']

MAX = 250
MAX_TOPICS = 10

def list_stop(line):
	unstoppable = []
	words = line.lower().split()
	for word in words:
		if word not in stopwords:
			unstoppable.append(word)
	return unstoppable

def str_stop(line):
	unstoppable = []
	words = line.lower().split()
	for word in words:
		if word not in stopwords:
			unstoppable.append(word)
	return ' '.join(unstoppable)

def load_data():
	test = []
	train = []
	N, n = map(int, raw_input().split())
	for i in xrange(N):
		x = raw_input().split()
		topics = map(int, x)
		query = raw_input()
		train.append([topics, query])
	for i in xrange(n):
		query = raw_input()
		test.append(query)
	return train, test

def bow(line):
	hashmap = {}
	words = list_stop(line)
	for word in words:
		if word in hashmap:
			hashmap[word] += 1
		else:
			hashmap[word] = 0
	return hashmap

def get_random(N):
	return TOP_TOPICS[:N]

def get_blank_votes():
	A = range(1, MAX+1)
	B = [0]*MAX
	return dict(zip(A, B))

class BaseClassifier():
	def __init__(self):
		self.trainingdata, self.testdata = load_data()
		# self.trainingdata = map(lambda x: str_stop())
	def fit(self):
		raise NotImplementedError('No bro !')
	def transform(self):
		raise NotImplementedError('No bro !')
	def fit_transform(self):
		for each in self.testdata:
			print ' '.join(str(i) for i in TOP_TOPICS)

class KnnClassifier(BaseClassifier):
	def fit_transform(self):
		for index, each in enumerate(self.testdata):
			results = []
			voting = get_blank_votes()
			words = bow(each)
			for labels, each in self.trainingdata:
				twords = bow(each)
				score = self._get_voting(twords, words)
				for label in labels:
					voting[label] += score
			toppers = sorted(voting.iteritems(), key=operator.itemgetter(1), reverse=True)[:MAX_TOPICS]
			for topper, score in toppers:
				if score is 0:
					break
				else:
					results.append(topper)
			if len(results) != MAX_TOPICS:
				toadd = MAX_TOPICS - len(results)
				results.extend(get_random(toadd))
			print ' '.join(str(i) for i in results)

	def _get_voting(self, twords, words):
		score = 0
		for each in twords:
			if each in words:
				score += twords[each]*words[each]
		return score

	def normalize(self):
		pass

def clean(data):
	cleaned = []
	for tags, query in data:
		cleaned.append([tags, list_stop(query)])
	return cleaned

def clean2(data):
	cleaned = []
	for query in data:
		cleaned.append(list_stop(query))
	return cleaned


def get_best(voting):
	toppers = sorted(voting.iteritems(), key=operator.itemgetter(1), reverse=True)[:MAX_TOPICS]
	results = []
	for one, two in toppers:
		if two is 0:
			break
		results.append(one)
	return results

class TFIDF_KNN_Classifier(BaseClassifier):
	def fit(self):
		self.trainingdata = clean(self.trainingdata)
		self.occ = {}
		self.entries = {}
		self.occ_tag = {}
		for tags, each in self.trainingdata:
			for word in each:
				if word in self.entries:
					self.entries[word] += 1
				else:
					self.entries[word] = 1
				for tag in tags:
					if tag in self.occ:
						if word in self.occ[tag]:
							self.occ[tag][word] += 1
						else:
							self.occ[tag][word] = 1
					else:
						self.occ[tag] = {}
						self.occ[tag][word] = 1
					for other in tags:
						if other is not tag:
							if tag in self.occ_tag:
								if other in self.occ_tag[tag]:
									self.occ_tag[tag][other] += 1
								else:
									self.occ_tag[tag][other] = 1
							else:
								self.occ_tag[tag] = {}
								self.occ_tag[tag][other] = 1
		for each_tag in self.occ:
			for each_word in self.occ[each_tag]:
				self.occ[each_tag][each_word] /= self.entries[each_word]*1.0
				
	def _get_voting(self, query):
		voting = dict(zip(range(1, 251), [0]*250))
		for i in xrange(1, 251):
			if i in self.occ:
				for each in query:
					if each in self.occ[i]:
						voting[i] += self.occ[i][each]
		return voting 

	def _fill(self, best):
		score = dict(zip(range(1, 251), [0]*250))
		remaining = MAX_TOPICS - len(best)
		for each in best:
			for tag in self.occ_tag:
				if each is not tag:
					if each in self.occ_tag[tag]:
						score[each] += self.occ_tag[tag][each]
		best.append(get_best(score)[:remaining])
		return best

	def transform(self):
		self.testdata = clean2(self.testdata)
		for each in self.testdata:
			voting = self._get_voting(each)
			best = get_best(voting)
			best = self._fill(best)
			print ' '.join(str(i) for i in best)



BC = TFIDF_KNN_Classifier()
BC.fit()
BC.transform()
