import numpy as np
import lda
import pandas as pd
import itertools
import logging
import argparse
import operator
import matplotlib.pyplot as plt
import nltk
import fileinput
import re
from collections import defaultdict
from sortedcontainers import SortedList, SortedSet
import simplejson
from scan import *
from scipy.sparse import csr_matrix


stopwords =  ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'be    fore', 'being', 'below', 'between', 'both', 'but', 'by', 'cannot', 'could', 'did', 'do', 'does', 'doing', 'down', 'during', 'each', 'few', 'for',     'from', 'further', 'had', 'has', 'have', '', 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'i    nto', 'is', 'it', 'its', 'itself', 'me', 'more', 'most', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ou    ght', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'she', 'should', 'so', 'some', 'such', 'than', 'that', 'the', 'their', 'theirs', '    them', 'themselves', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'we', 'were    ', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'with', 'would', 'you', 'your', 'yours', 'yourself', 'yourselves']
stopwords.extend(['.', ',', '"', "'",'RT' , '@' , '#' ,  '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']) # remove it if you need punctuation 

lim = 208000
old_total = 0
new_total = 0
delta = 0.5
j = 0
new_dictionary = defaultdict(int)
old_dictionary = defaultdict(int)
word_match_dictionary = defaultdict(int)
for line in fileinput.input():
	result = re.search('"text":(.*), "created_at":', line)
	result = result.group(1)
	result = result.decode('unicode_escape').encode('ascii','ignore')
	result = re.sub(r"http\S+", "", result)
	j+=1
	#print result
	tokens = nltk.word_tokenize(result.encode('utf-8'))
	for i in tokens:
		if i not in stopwords:
			if j < lim:
				old_dictionary[i]+= 1
				old_total+=1
				
			else:
				new_dictionary[i] += 1
				new_total += 1
				for k in tokens:
					if k not in stopwords:
						word_match_dictionary[(i,k)]+=1
old_size = len(old_dictionary)
print old_total
new_size = len(new_dictionary)
print new_total
goodset = SortedSet()
for i in new_dictionary.keys():
	val = float(new_dictionary[i] + delta)/float(new_dictionary[i] + delta*new_size)
	val/= float(old_dictionary[i] + delta)/float(old_dictionary[i] + delta*old_size)	
	if(len(goodset) < 300):
		goodset.add((val , i))
	else:
		if goodset[0][0] < val:
			del(goodset[0])
			goodset.add((val , i))

matrix = [[0 for i in xrange(len(goodset))] for i in xrange(len(goodset))]
for i in xrange(len(goodset)):
	#print i
	for j in xrange(len(goodset)):
		matrix[i][j] = float(word_match_dictionary[(goodset[i][1],goodset[j][1])])/min(new_dictionary[goodset[i][1]] , new_dictionary[goodset[j][1]])

matrix = np.matrix(matrix)
goodset = list(goodset)
fo = open('goodset.py' , 'wb')
fo.write("goodset = " )
simplejson.dump(goodset , fo)
fo.close()


k = csr_matrix(matrix)
d = scan(k , 0.7 , 2)
d = list(d)

fo = open("vertex.py" , 'wb')
fo.write("vertex_labels = ")
simplejson.dump(d , fo)
fo.close()
"""
mat = list(matrix)
fo = open('matrix.py' , 'wb')
fo.write("matrix = " )
simplejson.dump(mat , fo)
fo.close()
"""

