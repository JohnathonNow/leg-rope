#!/usr/bin/env python3
import xml.etree.ElementTree as etree 
import collections
import re
from math import log

rege1 = re.compile(r'[`!"#$%&()*+,-\./:;<=>\?@\[\\\]^_\{|\}~]')
rege2 = re.compile(r'\'')

DATA_DIR = '../data/'

ngram = 3
bad_words = collections.Counter()
good_words = collections.Counter()
good_total = 1
bad_total = 1
P_sbad = 0.000000004
P_sgood = 1-P_sbad

def P_good(w):
    w = tuple(w)
    if w in good_words: return good_words[w] / good_total
    else: return 1 / good_total #give unknown one count

def P_bad(w):
    w = tuple(w)
    if w in bad_words: return bad_words[w] / bad_total
    else: return 1 / bad_total #give unknown one count

def classify(s):
    words = s.split()
    p = log(P_sbad/P_sgood) + sum([log(P_bad(words[i-ngram:i])/P_good(words[i-ngram:i])) for i in range(ngram-1,len(words))])
    return p > 0
#train
with open(DATA_DIR+'./test_users.txt') as f:
    bads = set(f.read().split('\n'))
tree = etree.parse(DATA_DIR+'./test.xml')
root = tree.getroot()
for conversation in root:
    for message in conversation:
        author = message[0].text
        text = rege1.sub(' ', (message[2].text or '').lower())
        text = rege2.sub('', text)
        words = text.split()
        words = [words[i] for i in range(len(words)) if i==0 or words[i-1] != words[i]]
        if len(words) < 1: continue
        for i in range(ngram-1,len(words)):
            w = tuple(words[i-ngram:i])
            if author in bads:
                bad_words[w] += 1
                bad_total += 1
            else:
                good_words[w] += 1
                good_total += 1

#test
fp = 0
fn = 0
p = 0
n = 0
with open(DATA_DIR+'./train_users.txt') as f:
    bads = set(f.read().split('\n'))
tree = etree.parse(DATA_DIR+'./train.xml')
root = tree.getroot()
for conversation in root:
    lines = {}
    for message in conversation:
        author = message[0].text
        text = rege1.sub(' ', (message[2].text or '').lower())
        text = rege2.sub('', text)
        words = text.split()
        words = [words[i] for i in range(len(words)) if i==0 or words[i-1] != words[i]]
        text = ' '.join(words)
        lines[author] = lines.get(author,'')+text+' '
    for author in lines:
        bad = classify(lines[author])
        if author in bads:
            p += 1
            if not bad: fn += 1
        else:
            n += 1
            if bad: fp += 1
print("False negative rate {}".format(fn/p))
print("False positive rate {}".format(fp/n))
