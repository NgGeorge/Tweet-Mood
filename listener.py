from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import simplejson as json
import redis
import os

r = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=6379, db=0)

class TweetStreamListener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data)
        print tweet['text']
        r.publish('tweet_stream', json.dumps(tweet))
        return True

    def on_error(self, status):
        print status
        if status == 420:
            return False
