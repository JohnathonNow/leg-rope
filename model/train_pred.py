#!/usr/bin/env python3
import xml.etree.ElementTree as etree 
import collections
import re
from math import log
from keras.preprocessing.text import Tokenizer
import numpy
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
tokenizer = Tokenizer(num_words=5000)
rege1 = re.compile('[`!"#$%&()*+,-\./:;<=>\?@\[\\\]^_\{|\}~]')
rege2 = re.compile('\'')

with open('./test_users.txt') as f:
    bads = set(f.read().split('\n'))

X = []
Y = []

tree = etree.parse('./test.xml')
root = tree.getroot()
for conversation in root:
    messages = {}
    for message in conversation:
        author = message[0].text
        text = rege1.sub(' ', (message[2].text or '').lower())
        text = rege2.sub('', text)
        words = text.split()
        words = [words[i] for i in range(len(words)) if i==0 or words[i-1] != words[i]]
        if len(words) < 1: continue
        words = ' '.join(words) + ' '
        messages[author] = messages.get(author, '') + words
    for author in messages:
        words = messages[author]
        X.append(words)
        Y.append(1 if author in bads else 0)

tokenizer.fit_on_texts(X)
X = tokenizer.texts_to_sequences(X)

X = X[:100000]
Y = Y[:100000]
numpy.random.seed(7)
i = int(len(X)*0.6)
X_train = X[:i]
y_train = Y[:i]
X_test  = X[i:]
y_test  = Y[i:]

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
model.save("my_model.h5")
model.save_weights('model.hdf5')
with open('model.json', 'w') as f:
    f.write(model.to_json())
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))
