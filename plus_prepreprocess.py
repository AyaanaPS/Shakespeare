
f1 = open('data/spensershakespeare', 'r')
f = open('data/spenseyshakes', 'w')

for line in f1.readlines():
	f.write(line.strip())
	f.write('\n')
