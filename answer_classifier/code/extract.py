import csv

input_file = '../data/input.txt'
output_file = '../data/input_.csv'
test_input = '../data/test_input.csv'

f = open(input_file, 'r')
lines = f.readlines()
of = open(output_file, 'w')
tf = open(test_input, 'w')

def integer(inp):
	if inp == '+1':
		return '+1'
	return '-1'

def extract_to_CSV():
		w = csv.writer(of, delimiter=',')
		t = csv.writer(tf, delimiter=',')
		testing = False
		for index, line in enumerate(lines):
			if index is 0:
				N, M = map(int, line.split())
				continue
			if index is not 0:
				if index == N+1:
					testing = True
					continue
			line = line.split()
			ans_id = line[0]
			if not testing:
				result = integer(line[1])
				# print line
				features = [float(x.split(':')[1]) for x in line[2:]]
				row = [ans_id]
				row.extend(features)
				row.append(result)
				w.writerow(row)
			if testing:
				features = [float(x.split(':')[1]) for x in line[1:]]
				row = [ans_id]
				row.extend(features)
				t.writerow(row)
extract_to_CSV()
	
