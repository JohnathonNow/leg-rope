#!/usr/bin/env python3
import collections
import re
from math import log
import random
from keras.preprocessing.text import Tokenizer
import numpy
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
tokenizer = Tokenizer(num_words=5000)
rege1 = re.compile(r'[`!"#$%&()*+,-\./:;<=>\?@\[\\\]^_\{|\}~]')
rege2 = re.compile(r'\'')

MODEL_DIR = '../trained/'


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

#Code below largely from https://machinelearningmastery.com/sequence-classification-lstm-recurrent-neural-networks-python-keras/
max_length = 500
X_train = sequence.pad_sequences(X_train, maxlen=max_length)
X_test = sequence.pad_sequences(X_test, maxlen=max_length)
embedding_vecor_length = 32
model = Sequential()
model.add(Embedding(5000, embedding_vecor_length, input_length=max_length))
model.add(LSTM(100))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
model.fit(X_train, y_train, nb_epoch=3, batch_size=64)
model.save(MODEL_DIR+"my_model.h5")
model.save_weights(MODEL_DIR+'model.hdf5')
with open(MODEL_DIR+'model.json', 'w') as f:
    f.write(model.to_json())
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))
