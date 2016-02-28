from flask import Flask, request, Response, render_template
from listener import TweetStreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import redis
import os

application = Flask(__name__)

access_token = os.environ.get('TWITTER_ACCESS_TOKEN') 
access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET') 
consumer_key = os.environ.get('TWITTER_CONSUMER_KEY') 
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET') 

r = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=6379, db=0)

def event_stream():
    queue = r.pubsub()
    queue.subscribe('tweet_stream')
    for message in queue.listen():
        yield 'data: %s\n\n' % message['data']

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/tweets')
def get_tweets():
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    listener = TweetStreamListener()
    stream = Stream(auth, listener)
    stream.filter(locations=[-125.0011, 24.9493, -66.9326, 49.5904], async=True)

    application.debug = True
    application.run(threaded=True, use_reloader=False)


