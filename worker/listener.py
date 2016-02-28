from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from classifier.tweetClassifier import tweetClassifier
import simplejson as json
import redis
import os

r = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=6379, db=0)
clf = tweetClassifier()

class TweetStreamListener(StreamListener):

    with open('classifier/save_trained.json', 'r') as model:
        clf.from_json(model.read())

    def on_data(self, data):
        tweet = json.loads(data)
	print tweet
	if tweet.get('text', None) and tweet.get('place', None):
	    if tweet['place'].get('country_code', '') == 'US':
	        tweet['score'] =  clf.classify(tweet['text'])
	        if tweet['score'] != 'neutral':
	            r.publish('tweet_stream', json.dumps(tweet))
        return True

    def on_error(self, status):
        print status
        if status == 420:
            return False
