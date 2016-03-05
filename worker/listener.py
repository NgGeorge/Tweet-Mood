from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from classifier.tweetClassifier import tweetClassifier
import simplejson as json
import redis
import pika
import os

#r = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=6379, db=0)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='tweet_stream', type='fanout')
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
                    channel.basic_publish(exchange='tweet_stream',
                                          routing_key='',
                                          body=json.dumps(tweet))
	            #r.publish('tweet_stream', json.dumps(tweet))
        return True

    def on_error(self, status):
        print status
        if status == 420:
            connection.close()
            return False
