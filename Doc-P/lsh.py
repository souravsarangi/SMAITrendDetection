import math
from math import log
from  tokenise import *
import random
import operator


with open("small.txt") as f:
	data=f.read()
print "haiyya"

data=data.split("@@@")
tf=[]
idf={}
N=1
tweetsize=[]
for tweet in  data:
	print "tweet"+str(N)
	N+=1
	te=tokenise(tweet)
	tweetsize.append(len(te))
	dic={}
	for i in te:
		try:
			dic[i]+=1
		except KeyError:
			dic[i]=1
	tf.append(dic)
	for key in dic:
		try:
			idf[key]+=1
		except KeyError:
			idf[key]=1
for i in xrange(len(tf)):
	for j in tf[i]:
		print "tfidf"+str(i)
		tf[i][j]=log(1+tf[i][j])/log(1+N/idf[j])

def cossim(tf1,tf2):
	tfidfD1=1
	tfidfD2=1
	tfidfN=0
	for i in tf1:
		try:
			tfidfN=tf2[i]*tf1[i]
		except KeyError:
			pass
		tfidfD1+=tf1[i]*tf1[i]
	for i in tf2:
		tfidfD2+=tf2[i]*tf2[i]

	return 1.0*tfidfN/(pow(tfidfD1,0.5)*pow(tfidfD2,0.5))


threshsimscore=0.005
clusterno=0
cluster={}
cluster[0]=clusterno
clu=[]
clu.append([0])

total=0
co=0
for i in xrange(1,len(tf)):
	f=0
	bestscore=-1
	topset=[]
	for j in xrange(len(clu)):
		x=random.randint(0,len(clu[j]))
		simrank=cossim(tf[i],tf[j])
		x=random.randint(0,len(clu[j]))
		simrank+=cossim(tf[i],tf[j])
		if simrank>2*threshsimscore:
			topset.append([j,simrank])
	sorted(topset,key=lambda l:l[1], reverse=True)
	topset=topset[0:5]
	'''try:
		if topset[0][1]>threshsimscore:
			if topset[0][1]>bestscore:
				f=1
				bestscore=simrank
				bestcluster=cluster[j]
	except IndexError:
		pass'''
	for k in topset:
		for j in clu[k[0]]:
			simrank=cossim(tf[i],tf[j])
			total+=simrank
			co+=1
			if simrank>threshsimscore:
				if simrank>bestscore:
					f=1
					bestscore=simrank
					bestcluster=cluster[j]
	if f==1:
		cluster[i]=bestcluster
		clu[bestcluster].append(i)
	else:
		clusterno+=1
		cluster[i]=clusterno
		clu.append([])
		clu[clusterno].append(i)
	print "current"+str(i)+" CLUSTERS="+str(clusterno)
		

print clusterno

threshmembers=8
topclusters=[]
for i in clu:
	if len(i)>threshmembers:
		score=0
		for j in i:
			for word in tf[j]:
				score+=math.exp(-1.0*tf[j][word]/tweetsize[j])
		topclusters.append([i,score])


sorted(topclusters,key=lambda l:l[1], reverse=True)

topclusters=topclusters[0:10]
print len(topclusters)
for i in topclusters:
	topwords={}
	for j in i[0]:
		for word in tf[j]:
			score=tf[j][word]/tweetsize[j]
			try:
				topwords[word]+=score
			except KeyError:
				topwords[word]=score
	topwords= sorted(topwords.items(), key=operator.itemgetter(1), reverse=True)
	topwords=topwords[0:10]
	for i in topwords:
		print i[0],
	print

print
print
print
print
print

print len(topclusters)
for i in topclusters:
	maxtweetscore=0.0
	for j in i[0]:
		tweetscore=0.0
		for word in tf[j]:
			score=tf[j][word]/tweetsize[j]
			try:
				tweetscore+=score
			except KeyError:
				tweetscore+=score
		if tweetscore>maxtweetscore:
			maxtweetscore=tweetscore
			toptweet=tf[j]
	for i in toptweet:
		print i,
	print



