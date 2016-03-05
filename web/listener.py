from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import simplejson as json
import redis
import pika
import os

#r = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=6379, db=0)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='tweet_stream', type='fanout')

class TweetStreamListener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data)
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
