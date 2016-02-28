from listener import StreamListener

from tweepy import OAuthHandler
from tweepy import Stream

import os

access_token = os.environ.get('TWITTER_ACCESS_TOKEN') 
access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET') 
consumer_key = os.environ.get('TWITTER_CONSUMER_KEY') 
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET') 

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
listener = StreamListener()
stream = Stream(auth, listener)
stream.sample()
