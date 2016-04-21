import numpy as np
import lda
#from numpy import genfromtxt
import pandas as pd
import itertools
import logging
import argparse
import operator
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import re
import fileinput

# use matplotlib style sheet
try:
    plt.style.use('ggplot')
except:
    # version of matplotlib might not be recent
    pass

import sqlite3
import unicodedata

c = list()
for line in fileinput.input():
    result = re.search('"text":(.*), "created_at":', line)
    result = result.group(1)
    result = result.decode('unicode_escape').encode('ascii','ignore')
    result = re.sub(r"http\S+", "", result)
    c.append(result)

x=[]
token_dict = {}
i=0


for row in c:
    y=[]
    row = row.split(',')
    y.append(row[0].encode('utf-8'))
    token_dict[i] = y
    i += 1
    x.append(y)
print token_dict[1]
corpus = []
titles = []
cites = {}
listc = []
dic={}
j=0
for id, session in sorted(token_dict.iteritems(), key=lambda t: int(t[0])):
    dic[session[0]]=session
    corpus.append(session[0])
    titles.append(session[0])
    j+=1



for i in xrange(len(token_dict)):
	token_dict[i]=str(token_dict[i])


from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
print("\n Build DTM")
tf = CountVectorizer(stop_words='english')


print("\n Fit DTM")
tfs1 = tf.fit_transform(token_dict.values())
vocab = tf.get_feature_names()


# set the number of topics to look for
num = 20
model = lda.LDA(n_topics=num, n_iter=500, random_state=1)
#model = DBSCAN(eps = 0.3 , min_samples =10)

# we fit the DTM not the TFIDF to LDA
print("\n Fit LDA to data set")
model.fit_transform(tfs1)
doc_topic = model.doc_topic_
print len(doc_topic)
n_top_words = 10

print("\n Obtain the words with high probabilities")
topic_word = model.topic_word_  # model.components_ also works
#print topic_word
f=open('topic.txt','w')
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
    f.write('Topic {}: {}'.format(i, ' '.join(topic_words)))
    f.write('\n')
f.close()
for i in range(0, 10):
    print("{} (top topic: {})".format(titles[i], doc_topic[i].argmax()))
    print(doc_topic[i].argsort()[::-1][:3])

f=open('doc.txt','w')
dic_topic={}
#set topics
for n in range(len(doc_topic)):
    topic_most_pr = doc_topic[n].argmax()
    f.write("doc: {} topic: {}\n{}...".format(n,
                                            topic_most_pr,
                                            titles[n]))
    f.write('\n')
    if topic_most_pr not in dic_topic.keys():
    		dic_topic[topic_most_pr]=[]
    dic_topic[topic_most_pr].append(titles[n])
    #topics.insert(topic_most_pr)
f.close()
f, ax= plt.subplots(5, 1, figsize=(8, 6), sharex=True)
for i, k in enumerate([0, 1, 2, 3, 4]):
    ax[i].stem(doc_topic[k,:], linefmt='r-',
               markerfmt='ro', basefmt='w-')
    ax[i].set_xlim(-1, 21)
    ax[i].set_ylim(0, 1)
    ax[i].set_ylabel("Prob")
    ax[i].set_title("Document {}".format(k))

ax[4].set_xlabel("Topic")

plt.tight_layout()
plt.show()

id_list = []
for cite in ans:
	id_list.append(dic[cite][0])
print id_list


cities = []
citations = {}
#print listc

for cite in ans:
	if dic[cite][1] != "":
		cities = dic[cite][1].strip().split(";")
		citations[dic[cite][0]] = cities
		#print cities

print "The citations for Topic:",top_max
print citations
