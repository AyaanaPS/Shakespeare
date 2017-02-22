
import numpy as np

datapath = './'
filename = 'shakespeare.txt'

lines = np.array( open(filename).read().splitlines() )

notblank = np.where( lines != '')[0]
lines = lines[ notblank ]

notnumber = np.where( [ line[:5] != '     ' for line in lines ] )[0]
lines = lines[ notnumber ]

for l in range(len(lines)):
	lines[l] = lines[l].replace('.','')
	lines[l] = lines[l].replace(',','')
	lines[l] = lines[l].replace(';','')
	lines[l] = lines[l].replace(':','')
	lines[l] = lines[l].replace('?','')
	lines[l] = lines[l].replace('!','')
	
words = np.array([ line.split(' ') for line in lines ])

maxwords = max([ len(line) for line in words ])

X = np.zeros((words.shape[0],maxwords+1))	## value 0 corresponds to 'end'
dic = {'END': 0}
index = 1

for l in range(len(words)):
	line = words[l]
	for w in range(len(line)):

		word = line[w].lower()
		
		if word in dic.keys():
			pass
		else: 
			dic[word] = index
			index += 1

		X[l][w] = dic[word]

from hmmlearn.hmm import MultinomialHMM as hmm

model = hmm(n_components=4,n_iter=1000)
model.fit(X.astype('int'))

samples = [ model.sample( n_samples = 8 ) for _ in range(14) ]

dic2 = { dic[key]: key for key in dic.keys() }
poem = [ [ dic2[s[0]] for s in sample[0] ] for sample in samples ]


