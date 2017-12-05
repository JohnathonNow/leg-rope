import mailbox
import re
import collections
from math import log
from bs4 import BeautifulSoup

regex = re.compile('[`!"#$%&()*+,-./:;<=>?@[\]^_\{|\}~]')
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

mbox = mailbox.mbox('phishing.mbox')
for message in mbox:
    if message.is_multipart():
        content = ''.join((part.get_payload(decode=True) or b'').decode("utf-8",'replace')  for part in message.get_payload())
    else:
        content = (message.get_payload(decode=True) or b'').decode("utf-8",'replace') 
    soup = BeautifulSoup(content,  'html.parser')
    text = regex.sub(' ', (soup.get_text() or '').lower())
    bads.append(text)
mbox = mailbox.mbox('clean.mbox')
for message in mbox:
    ct = ''
    if message.is_multipart():
        content = ''
        for part in message.get_payload():
            ct = message.get_content_type()
            content += (part.get_payload(decode=True) or b'').decode("utf-8",'replace') + ' '
    else:
        ct = message.get_content_type()
        content = (message.get_payload(decode=True) or b'').decode("utf-8",'replace') 
    try:
        if ct == 'text/html':
            soup = BeautifulSoup(content,  'html.parser')
            text = soup.get_text() or ''
        elif ct == 'text/plain':
            text = content
        else:
            continue
        text = regex.sub(' ', text.lower())
        goods.append(text)
    except Exception as E:
        print(E)

bad_train = bads[100:]
bad_test = bads[:100]
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
print("False negative rate {}".format(fn/p))
print("False positive rate {}".format(fp/n))
