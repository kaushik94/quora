
output_file = open('../data/test_output_naive.txt', 'w')
input_file = open('../data/test_input.csv', 'r')


def baseline():
	for each in input_file:
		each = each.split(',')
		id_ = each[0]
		output_file.write(str(id_)+" +1"+"\n")

baseline()
