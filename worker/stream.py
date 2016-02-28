import daemon
from listener import TweetStreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import redis
import os

def stream():
	access_token = os.environ.get('TWITTER_ACCESS_TOKEN') 
	access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET') 
	consumer_key = os.environ.get('TWITTER_CONSUMER_KEY') 
	consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET') 

	r = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=6379, db=0)
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	listener = TweetStreamListener()
	stream = Stream(auth, listener)
	stream.filter(locations=[-125.0011, 24.9493, -66.9326, 49.5904], async=True)

with daemon.DaemonContext():
	stream()
