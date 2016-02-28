from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import simplejson as json
import redis

red = redis.StrictRedis(host='localhost', port=6379, db=0)

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
                red.publish('tweet_stream', json.dumps(tweet))
                return True
        except:
            pass

    def on_error(self, status):
        print status
        #if status == 420:
            #returning False in on_data disconnects the stream
            #return False
