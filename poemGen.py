import numpy as np
import nltk
from nltk import word_tokenize
from HMM import unsupervised_HMM
import random

# First read the file, remove numbers, white space, etc
filename = 'data/shakespeare.txt'

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
	lines[l] = lines[l].replace(')','')
	lines[l] = lines[l].replace('(','')
	lines[l] = lines[l].strip(' ')

# Now lines, is a list of all the lines in the file.

# This dictionary contains words associated with each type
wordType = {}

types = []
type_map = {}
type_counter = 0

for line in lines:

	lineSeq = []

	# Tokenize each line to get the tags
	newLine = nltk.pos_tag(word_tokenize(line))

	# Iterate through the tuples
	for pair in newLine:
		tag = pair[1]

		if tag not in type_map:
			type_map[tag] = type_counter
			type_counter += 1

		if tag not in wordType:
			wordType[tag] = [pair[0]]
		else:
			wordType[tag].append(pair[0])

		lineSeq.append(type_map[tag])

	types.append(lineSeq)

HMM = unsupervised_HMM(types, 4, 10)

# Reverse our tag map
tag_map = { type_map[key]: key for key in type_map.keys() }

poem = []
for i in range(10):
	emission = HMM.generate_emission(8)
	line = ''
	for val in emission:
		tag = tag_map[val]
		wordOptions = wordType[tag]
		word = random.choice(wordOptions)
		line += word + ' '
	poem.append(line)

for line in poem:
	print line

