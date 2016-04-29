from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


import string
exclude = set(string.punctuation)
print exclude
exclude.union(set(['\t',' ','\n']))
import re


tweets = []
for j in xrange(4):
	x1 = raw_input()
	x1 = int(x1)
	tweets1 = []
	for i in xrange(x1):
		y1 = raw_input()
		y1 = ''.join(ch for ch in str(y1) if ch not in exclude)
		y1 = re.sub(' +',' ',y1)
		tweets1 += [str(y1)]
	tweets += [ tweets1 ] 

print tweets

score={}
score[0]=0
score[1]=0
score[2]=0
score[3]=0

for i in xrange(4):
	st = [0,1,2,3]
	st.remove(i)
	for k in st:
		for j in tweets[i]:
			overall = 0.00
			for l in tweets[k]:
				occ = 0.0
				for tw1 in j.split(' '):
					cur = 0.0
					for tw2 in l.split(' '):
						cur += similar(tw1,tw2)
#					cur /= len(l.split(' '))
					occ += cur
				occ = occ/(len(l.split(' ')*len(j.split(' '))))
				if overall < occ:
				  	overall = occ
			score[i] += overall
total = 0
for i in score:
	base = 0
	for j in tweets[i]:
		base += len(j.split(' ')) 
	score[i] = score[i]/base
	total += score[i]

for i in score:
	score[i] /= total


print score
