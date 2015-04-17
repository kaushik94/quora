import sys

filename = sys.argv[1]
out = open('../data/'+filename, 'r')
comp = open('../data/output.txt', 'r')

outputs = []
ideal = []

for each in out:
	x = each.split()
	outputs.append(x)
for each in comp:
	x = each.split()
	ideal.append(x)

def compare_exact():
	pos = 0
	if len(outputs) != len(ideal):
		print "something wrong, lengths don't match"
		return 1
	for i in xrange(len(outputs)):
		# print outputs[i][1], ideal[i][1]
		if outputs[i][0] != ideal[i][0]:
			print "something wrong, ids don't match"
			return 1
		if outputs[i][1] == ideal[i][1]:
			pos += 1
	return float(pos)/len(outputs)

print compare_exact()
