
import pickle

HMM = pickle.load(open('HMM_1_4_20.pkl','rb'))
word_map2 = pickle.load(open('word_map2.pkl','rb'))

def countSyllables(word):
        return 1

def syl_count(sequence):
	syl_each = [ countSyllables(word_map2[n]) for n in sequence ]
	syl_cum = [ sum( syl_each[:i] ) for i in range(1,len(sequence)) ]
	return syl_cum

M = emissionlength = 10		
## 10 max, could be all 1-syllable words
## trim to 10 syllables, or if can't trim then scrap and generate a new one

rhymes = ['' for _ in range(14)]
poem = ['' for _ in range(14)]

for nRhymes in range(7):

	nSyl1, nSyl2 = 0,0
	
	#while (nSyl1 != 10)*(nSyl2 != 10):
	
        rhymeline1, rhymeline2 = HMM.generate_emission(M)
        
        ## some lines cut short by 'END'/'START'
        if 0 in rhymeline1: rhymeline1 = rhymeline1[:rhymeline1.index(0)]
        if 0 in rhymeline2: rhymeline2 = rhymeline2[:rhymeline2.index(0)]
        
        nSyl_seq1 = syl_count(rhymeline1)
        nSyl_seq2 = syl_count(rhymeline2)

        if 10 in nSyl_seq1: 
                rhymeline1 = rhymeline1[:nSyl_seq1.index(10)+1]
                nSyl1 = 10

        if 10 in nSyl_seq2: 
                rhymeline2 = rhymeline2[:nSyl_seq2.index(10)+1]
                nSyl2 = 10

	text1 = ' '.join([ word_map2[n] for n in rhymeline1[::-1] ])
	text2 = ' '.join([ word_map2[n] for n in rhymeline2[::-1] ])
	print text1
	print text2
	print ''
	
	rhymes[nRhymes*2] = text1
	rhymes[nRhymes*2+1] = text2

poem[0] = rhymes[0]
poem[2] = rhymes[1]

poem[1] = rhymes[2]
poem[3] = rhymes[3]

poem[4] = rhymes[4]
poem[6] = rhymes[5]

poem[5] = rhymes[6]
poem[7] = rhymes[7]

poem[8] = rhymes[8]
poem[10] = rhymes[9]

poem[9] = rhymes[10]
poem[11] = rhymes[11]

poem[12] = rhymes[12]
poem[13] = rhymes[13]
