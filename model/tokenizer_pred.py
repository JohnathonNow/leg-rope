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
rege1 = re.compile(r'[`!"#$%&()*+,-\./:;<=>\?@\[\\\]^_\{|\}~]')
rege2 = re.compile(r'\'')

DATA_DIR = '../data/'

with open(DATA_DIR+'./test_users.txt') as f:
    bads = set(f.read().split('\n'))

X = []

tree = etree.parse(DATA_DIR+'./test.xml')
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

tokenizer.fit_on_texts(X)
print(tokenizer.word_index)
