import numpy as np
import nltk
from nltk import word_tokenize

datapath = './'
filename = 'data/spenseyshakes'

lines = np.array( open(filename).read().splitlines() )

notblank = np.where( lines != '')[0]
lines = lines[ notblank ]

notnumber = np.where( [ len(line) > 10 for line in lines ] )[0]
lines = lines[ notnumber ]

for l in range(len(lines)):
	lines[l] = lines[l].replace('.','')
	lines[l] = lines[l].replace(',','')
	lines[l] = lines[l].replace(';','')
	lines[l] = lines[l].replace(':','')
	lines[l] = lines[l].replace('?','')
	lines[l] = lines[l].replace('!','')
	lines[l] = lines[l].replace('  ','')
	lines[l] = lines[l].replace('(','')
	lines[l] = lines[l].replace(')','')
	
words = np.array([ line.split(' ') for line in lines ])
maxwords = max([ len(line) for line in words ])

#X = [ [0 for _ in range(maxwords)] for __ in range(len(words)) ]
X = []
rhymepairs = []
dic = {'END': 0}	## really 'START' since it's going backwards
index = 1

types = []
wordType = {}
type_map = {}
type_counter = 0

for l in range(len(words)):

	line = words[l]
	xline = []

	lineSeq = []
	
	for w in range(len(line)):

		word = line[-(w+1)].lower()		## go backwards (for rhyming)

		wordToken = nltk.pos_tag(word_tokenize(word))
		# print(wordToken)
		if word in dic.keys():
			pass
		else: 
			dic[word] = index
			index += 1

		tag = wordToken[0][1]
		wordID = dic[word]

		if tag not in type_map.keys():
			type_map[tag] = type_counter
			type_counter +=1

		if tag not in wordType.keys():
			wordType[tag] = [wordID]
		else:
			wordType[tag].append(wordID)

		lineSeq.append(type_map[tag])

		#X[l][w] = dic[word]
		xline.append( dic[word] )

	xline.append( 0 )
	X.append(xline)
	types.append(lineSeq)

	## store rhyming pairs:
	if (l+1) % 14 == 0:
		rhymepairs.append( [words[l-13][-1],words[l-11][-1]] )	## line 1,3
		rhymepairs.append( [words[l-12][-1],words[l-10][-1]] )	## line 2,4

		rhymepairs.append( [words[l-9][-1],words[l-7][-1]] )	## line 5,7
		rhymepairs.append( [words[l-8][-1],words[l-6][-1]] )	## line 6,8

		rhymepairs.append( [words[l-5][-1],words[l-3][-1]] )	## line 9,11
		rhymepairs.append( [words[l-4][-1],words[l-2][-1]] )	## line 10,12

		rhymepairs.append( [words[l-1][-1],words[l][-1]] )	## line 13,14

dic2 = { dic[key]: key for key in dic.keys() }
# Reverse our tag map
tag_map = { type_map[key]: key for key in type_map.keys() }
				
import pickle

pickle.dump(dic,open('word_map.pkl','wb'))
pickle.dump(dic2,open('word_map2.pkl','wb'))
pickle.dump(X,open('data1.pkl','wb'))
pickle.dump(rhymepairs,open('rhymepairs.pkl','wb'))

pickle.dump(types,open('data2.pkl', 'wb'))
pickle.dump(tag_map, open('tag_map.pkl', 'wb'))
pickle.dump(wordType, open('word_type.pkl', 'wb'))





