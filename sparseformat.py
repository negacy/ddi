f = open('dataset_test.txt')
data = f.readlines()
for i in data:
	X =[]
	y = ''
	for j in i.split():
		try:
			if j.split(':')[1] != '0':
				X.append(j)
		except IndexError:
			y = j
	print y, ' '.join(X)

