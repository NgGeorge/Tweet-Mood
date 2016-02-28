from flask import Flask, request, Response, stream_with_context
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import simplejson as json
import os
import redis

application = Flask(__name__)
red = redis.StrictRedis(host='happinessmap.zpskdb.0001.usw2.cache.amazonaws.com', port=6379, db=0)

access_token = os.environ.get('TWITTER_ACCESS_TOKEN') 
access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET') 
consumer_key = os.environ.get('TWITTER_CONSUMER_KEY') 
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET') 

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

streams = []

class StreamListener(StreamListener):

    def on_connect(self):
        print 'Stream starting...'

    def on_data(self, data):
        decoded = json.loads(data)
        try: 
            if decoded['geo']:
                tweet = {}
                tweet['screen_name'] = '@'+decoded['user']['screen_name']
                tweet['text'] = decoded['text'].encode('ascii', 'ignore')
                tweet['coord'] = decoded['geo']['coordinates']
                tweet['created_at'] = decoded['created_at']
                print 'A tweet received'
                print tweet
                # publish to 'tweet_stream' channel
                red.publish('tweet_stream', json.dumps(tweet))
                return True
        except:
            pass

    def on_error(self, status):
        print status
        if status == 420:
            #returning False in on_data disconnects the stream
            return False

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/tweets', methods=['GET'])
def get_tweets():
    for stream in streams:
        stream.disconnect()

    listener = StreamListener()
    stream = Stream(auth, listener)
    streams.append(stream)
    stream.sample()
    def event_stream():
        pubsub = red.pubsub()
        pubsub.subscribe('tweet_stream')
        for message in pubsub.listen():
            yield 'data: %s\n\n' % message['data']
    return Response(stream_with_context(event_stream()), mimetype="text/event-stream")

if __name__ == '__main__':
    application.debug = True
    application.run(threaded=True)
