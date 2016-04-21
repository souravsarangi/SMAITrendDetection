from pyspark.mllib.fpm import FPGrowth
from operator import itemgetter
from  tokenise import *

from pyspark import SparkContext
sc = SparkContext('local', 'Exam_3')
data = open("output.txt","r").read()
data=data.split("\n@@@\n")
data2=[]
f=open("newoutput.txt","w").write("")
for i in data:
	for j in set(tokenise(i)):
		if j!='"rt':
			with open("newoutput.txt","a") as f:
				f.write(j+" ")
	with open("newoutput.txt","a") as f:
				f.write("\n")

data=sc.textFile("newoutput.txt")
#print data2
print "starting"
transactions = data.map(lambda line: line.strip().split(' '))

model = FPGrowth.train(transactions, minSupport=0.001, numPartitions=10)
result = sorted(model.freqItemsets().collect(),key=lambda x: len(x[0]), reverse=True)
for fi in result:
    print(fi)


