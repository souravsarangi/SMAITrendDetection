#######################################################################################
#
#			SMAI MAJOR PROJECT
#			  TEAM CHIPMONKS
#
#######################################################################################


#######################################################################################
#
#		APPROACH 2 NGRAMS [ index on 1, 2, and 3 grams ]
#
#######################################################################################


import string
import datetime as dt
import json

class IndexBox:

	def __init__(self, leastTime = dt.datetime(2010,1,1), timeFrame = 1000):
		assert( isinstance(leastTime,dt.datetime) )
		self.leastTime = leastTime
		self.timeframe = timeFrame
		self.data = {}

	def insertTweet( self, tweet_text, tweet_time ):
		if not isinstance(tweet_time, dt.datetime):
			print "Incorrect time format expected datetime instance"
			return
		Indx = self.getIndexTime( tweet_time )

		filtered_tweet = self.filter_t( tweet_text )
		tweet_words = len(filtered_tweet)
		if tweet_words == 0:
			return

		if filtered_tweet[0] not in self.data:
			self.data[filtered_tweet[0]] = {}
		if Indx not in self.data[filtered_tweet[0]]:
			self.data[filtered_tweet[0]][Indx] = 0

		self.data[filtered_tweet[0]][Indx] += 1

		if tweet_words > 1:

			if filtered_tweet[1] not in self.data:
				self.data[filtered_tweet[1]] = {}
			if Indx not in self.data[filtered_tweet[1]]:
				self.data[filtered_tweet[1]][Indx] = 0
			self.data[filtered_tweet[1]][Indx] += 1

			grams_2 = filtered_tweet[0]+'~~'+filtered_tweet[1]
			if grams_2 not in self.data:
				self.data[grams_2] = {}
			if Indx not in self.data[grams_2]:
				self.data[grams_2][Indx] = 0

			self.data[grams_2][Indx] += 1


		for i in xrange(2,tweet_words):
			if filtered_tweet[i] not in self.data:
				self.data[filtered_tweet[i]] = {}
			if Indx not in self.data[filtered_tweet[i]]:
				self.data[filtered_tweet[i]][Indx] = 0
			self.data[filtered_tweet[i]][Indx] += 1

			grams_2 = filtered_tweet[i-1]+'~~'+filtered_tweet[i]
			if grams_2 not in self.data:
				self.data[grams_2] = {}
			if Indx not in self.data[grams_2]:
				self.data[grams_2][Indx] = 0
			self.data[grams_2][Indx] += 1

			grams_3 = filtered_tweet[i-2]+'~~'+filtered_tweet[i-1]+'~~'+filtered_tweet[i]
			if grams_3 not in self.data:
				self.data[grams_3] = {}

			if Indx not in self.data[grams_3]:
				self.data[grams_3][Indx] = 0
			self.data[grams_3][Indx] += 1

	def getIndexTime( self, tweet_time  ):
		return int((tweet_time - self.leastTime).total_seconds() / self.timeframe)

	def filter_t( self, tweet_text ):
		replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
		tweet_text = tweet_text.translate(replace_punctuation)
		return tweet_text.split()

	def save(self, file_name):
		with open(file_name, 'w') as f:
			json.dump(self.data, f)
	def load(self, file_name, force = 0):
		if len(self.data) != 0  and force == 0:
			print '\033[93m' + 'Data not Loaded as the current indexbox is not empty\n\t\t........[ to forcefully initialize pass 1 as 2nd parameter ]' + '\033[0m'
			return
		with open(file_name,'r') as f:
			try:
				self.data = json.load(f)
			except ValueError:
				self.data = {}

				
if __name__ == '__main__':
	x = IndexBox()
	x.insertTweet('that was done by mistake!!!',dt.datetime(2016,12,1))
	print x.data
	x.save('darshan')
