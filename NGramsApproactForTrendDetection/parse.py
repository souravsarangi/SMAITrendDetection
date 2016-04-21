import json
from ngrams import IndexBox
from datetime import datetime, timedelta
import re

def feed_data(file_data, file_save):
	reader = open(file_data)
	tweet_count = 0
	box = IndexBox()
	for tweet in reader.xreadlines():
		try:
			tweet_x = json.loads(tweet)
			tweet_text =  re.sub(r"http\S+","",tweet_x['text'].encode('utf-8')) 
			timex = datetime(2016,1,1) + timedelta(hours=int(tweet_x['created_at']))	# only for the current dataset
			box.insertTweet(tweet_text,timex)
		except ValueError:
			print tweet_count
		tweet_count += 1
		print tweet_count
	box.save(file_save)
	reader.close()


if __name__ == '__main__':
	feed_data('twitter_data.txt','output.txt')
