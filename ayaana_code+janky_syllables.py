import numpy as np
import nltk
from nltk import word_tokenize
from HMM import unsupervised_HMM
import random
from nltk.corpus import cmudict
import string
import curses 
from curses.ascii import isdigit 

d = cmudict.dict()
phoneme_dict = dict(cmudict.entries())
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
		if pair[0] not in {"'s", "'"}:
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

HMM = unsupervised_HMM(types, 4, 5)

# Reverse our tag map
tag_map = { type_map[key]: key for key in type_map.keys() }
'''
def nsyl(word):
	return len(''.join(c if c in"aeiouyAEIOUY"else' 'for c in word.rstrip('e')).split())
'''

def nsyl(word):
	word = word.lower()
	if word in {"sway'st", "mak'st", "dearths", "'gainst", "'this", "'truth", "stick'st", "'had"}:
		return 1
	if word in {"thrivers", "filching", "dateless", "savour", "wherefore","wand'rest", "compeers", "shouldst", "blenches", "basest", "o'ersways", "riper", "burthen", "humour", "diest", "freezings"}:
		return 2
	if word in {"equipage", "usurer", "honouring", "warrantise", "amazeth", "buriest", "sepulchres", "departest", "convertest", "cherubins", "shallowest"}:
		return 3
	if word in {"incertainty", "inheritors"}:
		return 4
	if word in {"'","'s"}:
		return 11
	return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]

poem = [[] for i in range(14)]

for i in range(14):
	emission = HMM.generate_emission(10)
	syls = 0 
	line = ''
	print "um"
	for val in emission:
		tag = tag_map[int(val)]
		wordOptions = wordType[tag]
		word = random.choice(wordOptions)
		syls += nsyl(word)
		if syls > 10:
			syls -= nsyl(word)
			while True:
				print "infinite loop - start over"
				print syls, wordOptions
				word = random.choice(wordOptions)
				if nsyl(word) + syls == 10:
					syls += nsyl(word)
					break 
		line += word + ' '
		if syls == 10:
			poem[i] = line 
			last_word = word 
			break
	
for line in poem:
	print line