import mailbox
import re
import collections
from math import log
from bs4 import BeautifulSoup

rege1 = re.compile(r'[`!"#$%&()*+,-\./:;<=>\?@\[\\\]^_\{|\}~]')
rege2 = re.compile(r'\'')
bads = []
goods = []

bad_words = collections.Counter()
good_words = collections.Counter()
good_total = 1
bad_total = 1
P_sbad = 0.004
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
    p = log(P_sbad/P_sgood) + sum([log(P_bad(words[i-2:i])/P_good(words[i-2:i])) for i in range(1,len(words))])
    return p > 0

with open('../data/good_emails.txt') as f:
    goods = f.readlines() 
    goods = [rege1.sub(' ', x).lower() for x in goods]
    goods = [rege2.sub('', x).lower() for x in goods]

with open('../data/bad_emails3.txt') as f:
    bads = f.readlines() 
    bads = [rege1.sub(' ', x).lower() for x in bads]
    bads = [rege2.sub('', x).lower() for x in bads]


bad_train = bads[0::2]
bad_test = bads[1::2]
good_train = goods[0::2]
good_test = goods[1::2]

for text in good_train:
    words = text.split()
    if len(words) < 1: continue
    for i in range(1,len(words)):
        w = words[i-2:i]
        w = tuple(w)
        good_words[w] += 1
        good_total += 1

for text in bad_train:
    words = text.split()
    if len(words) < 1: continue
    for i in range(1,len(words)):
        w = words[i-2:i]
        w = tuple(w)
        bad_words[w] += 1
        bad_total += 1
        
#test
fp = 0
fn = 0
p = 0
n = 0
for text in good_test:
    if classify(text):
        fp += 1
    n += 1
for text in bad_test:
    if not classify(text):
        fn += 1
    p += 1

print("Bads: {}".format(p))
print("Goods: {}".format(n))
print("False negative rate {}".format(100*fn/p))
print("False positive rate {}".format(100*fp/n))
