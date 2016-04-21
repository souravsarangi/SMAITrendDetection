# Ngrams Approach for Twitter trend detection
#
#
#
>In this method indexing is done on n-grams and then based on the df-idf score of each top K n-grams are extracted and then they are further clustered. Top C clusters are taken and a topic corresponding to each cluster is then identified and treated as a trending topic.

#  
#     
Steps Involved: 

- All the tweets are parsed and only two attributes (tweet_text and tweet_time ) of them are used as inputs in this model.
- An Iterator Iterates over all the tweets and Indexes 1gram, 2gram, and 3 grams where these n-grams serve as index to a dictionary mapping tweet_time to frequency of the corresponding n gram for that particular time.
- Now we calculate the df-idf score for each of these n-grams and then we extract some top K n-grams based on the df-idf score.

  ![alt text](https://scontent-sin1-1.xx.fbcdn.net/v/t1.0-9/13007284_1056567421075157_8400821834248643816_n.jpg?oh=530cd3e1608558b15b19ffa08e2f355f&oe=57B6B5C5 "df-idf score" ) 

- Now at this point we introduce a distance measure d between two ngrams as no. of tweets both of them co-occur. (Normalization could be done we used log base 2 ). 
Using the above mentioned d measure a adjacency matrix is formed and a clustering algorithm is employed ( Spectral Clustering ).
- Finally for every cluster a topic is assigned.
- All the top C topics (each corresponding to one such cluster ) are treated/detected as trending topics.
