from ngrams import IndexBox
import datetime
import math
import operator
import numpy as np
from sklearn.cluster import spectral_clustering as SC
import math

def get_trending_topics( FILE_LOAD,dt, load_file, load_from_file = 0, no_of_topics = 10  , t=50000):
	DataIndex = IndexBox()
	DataIndex.load(FILE_LOAD)

	if load_from_file == 0:
		trendTime = DataIndex.getIndexTime( dt )
		df_idft_scores = {}
		for i in DataIndex.data:
			df_idft_scores[i] = get_df_idft( DataIndex.data[i] , t, trendTime)
		sorted_by_score = sorted(df_idft_scores.items(), key=operator.itemgetter(1), reverse=True)
		trending_topics = []
		count = 0
		for i in sorted_by_score:
			trending_topics += [i[0].encode('utf-8')]
			count += 1
			if count == 1000:		# 1000 top df-idf ngrams for clustering
				break
		save_to_file = open(load_file,'w')
		save_to_file.write('$$'.join(trending_topics))
		save_to_file.close()
		return 'saved to file'
	
	else:
		load_from_file = open(load_file,'r')
		trending_topics = load_from_file.read().split('$$')
		GraphMatrix  = []
		for ng1 in trending_topics:
			row = []
			for ng2 in trending_topics:
		        	score = 0
				for tw1 in DataIndex.data[ng1.decode('utf-8')]:
					for tw2 in DataIndex.data[ng2.decode('utf-8')]:
						if tw1 == tw2: 
							score += 1
				row += [math.log(score+1,2)]
			GraphMatrix += [np.array(row)]
		GraphMatrix = np.array(GraphMatrix)
		No_of_clusters = 5
		clusters = SC(GraphMatrix, n_clusters=No_of_clusters,eigen_solver='arpack')

		f_stop = open('stopwords.txt','r')
		stopwords = f_stop.read().split('\n')

		Mark = [0]*No_of_clusters
		count = 0
		topics_trending = []
		for i in clusters:
			current_gram = trending_topics[count].decode('utf-8')
			if Mark[i] == 0:
				if '~~' not in current_gram:
					if current_gram not in stopwords and (not current_gram.isdigit()):
						topics_trending += [current_gram]
						Mark[i]=1
				else:
					topics_trending += [current_gram]
					Mark[i]=1
			count += 1
		return topics_trending	
		
def get_df_idft( freq_list, t , trendTime):
	sum_prev_t = 0
	cur_t = 1
	for j in freq_list:
		i = int(j.encode('utf-8'))
		if (i < trendTime) and (i >= (trendTime - t)):
			sum_prev_t += freq_list[j]
		elif i == trendTime:
		 	cur_t += freq_list[j]
	sum_prev_t = math.log((sum_prev_t*1.0)/t + 1) + 1
	return (cur_t*1.0)/sum_prev_t

print get_trending_topics('output.txt', datetime.datetime(2016,1,1) + datetime.timedelta( hours=22 ) ,'thousandtopics.txt',1)
