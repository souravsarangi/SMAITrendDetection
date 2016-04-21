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
from vertex import *
from goodset import *

print len(goodset)
print len(vertex_labels)

a = dict()
for i in xrange(len(vertex_labels)):
	if vertex_labels[i] in a.keys():
		a[vertex_labels[i]].append(i)
	else:
		a[vertex_labels[i]] = list()
		a[vertex_labels[i]].append(i)

print a

for i in a.keys():
	if len(a[i]) >= 3 :
		for j in a[i]:
			print goodset[j][1],
		print ""

