
import numpy as np

data_ver = 1

import pickle
X = pickle.load(open('data%d.pkl' % data_ver,'rb'))
dic = pickle.load(open('word_map.pkl','rb'))

from HMM import unsupervised_HMM

n_states = 4
n_iters = 1000

for n_states in [4]:

	for n_iters in [20]:

		HMM = unsupervised_HMM(X, n_states, n_iters)

		pickle.dump(HMM,open('HMM_%d_%d_%d.pkl' % (data_ver,n_states,n_iters),'wb'))

