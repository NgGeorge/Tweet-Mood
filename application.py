from flask import Flask, request, Response, stream_with_context
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from listener import StreamListener
import simplejson as json
import os
import redis


application = Flask(__name__)
red = redis.StrictRedis(host='localhost', port=6379, db=0)

def event_stream():
    queue = red.pubsub()
    queue.subscribe('tweet_stream')
    for message in queue.listen():
        yield 'data: %s\n\n' % message['data']

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/tweets', methods=['GET'])
def get_tweets():
    return Response(event_stream(), mimetype="text/event-stream")


if __name__ == '__main__':
    application.debug = True
    application.run(threaded=True)
