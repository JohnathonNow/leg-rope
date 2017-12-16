#!/usr/bin/env python3
import collections
import re
import random
from math import log
from keras.preprocessing.text import Tokenizer
import numpy
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.models import load_model
from keras.preprocessing import sequence

DATA_DIR = '../data/'
MODEL_DIR = '../trained/'

tokenizer = Tokenizer(num_words=5000)
rege1 = re.compile(r'[`!"#$%&()*+,-\./:;<=>\?@\[\\\]^_\{|\}~]')
rege2 = re.compile(r'\'')



with open('../data/good_emails.txt') as f:
    goods = f.readlines() 
    goods = [rege1.sub(' ', x).lower() for x in goods]
    goods = [rege2.sub('', x).lower() for x in goods]
    goods = [re.sub(r'[^\x00-\x7f]',r'', x) for x in goods]
    X = goods
    Y = [0 for x in goods]

with open('../data/bad_emails3.txt', encoding='utf-8', errors='ignore') as f:
    bads = f.readlines() 
    bads = [rege1.sub(' ', x).lower() for x in bads]
    bads = [rege2.sub('', x).lower() for x in bads]
    bads = [re.sub(r'[^\x00-\x7f]',r'', x) for x in bads]
    X += bads
    Y += [1 for x in bads]

combined = list(zip(X, Y))
random.shuffle(combined)
X[:], Y[:] = zip(*combined)
tokenizer.fit_on_texts(X)
X = tokenizer.texts_to_sequences(X)

numpy.random.seed(7)
i = int(len(X)*0.5)
X_train = X[:i]
y_train = Y[:i]
X_test  = X[i:]
y_test  = Y[i:]


max_length = 500
X_train = sequence.pad_sequences(X_train, maxlen=max_length)
X_test = sequence.pad_sequences(X_test, maxlen=max_length)

model = load_model(MODEL_DIR+'my_model.h5')
p = n = 0
fp = fn = 0
O = model.predict(X_test)
print(O)
for i in range(len(X_test)):
    y = O[i]
    if y_test[i] == 0:
        n += 1
        if y >= 0.25:
            fp += 1
    else:
        p += 1
        if y < 0.25:
            fn += 1

print('False Positive Rate: {}'.format(100*fp/n))
print('False Negative Rate: {}'.format(100*fn/p))
