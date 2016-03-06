from flask import Flask, request, Response, render_template
from listener import TweetStreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import redis
import pika
import os

application = Flask(__name__)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get('RABBIT_HOST'), port=5672))
channel = connection.channel()

channel.exchange_declare(exchange='tweet_stream', type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='tweet_stream', queue=queue_name)

def event_stream():
    '''
    queue = r.pubsub()
    queue.subscribe('tweet_stream')
    for message in queue.listen():
        yield 'data: %s\n\n' % message['data']
    '''
    for method_frame, properties, body in channel.consume(queue_name):
        channel.basic_ack(method_frame.delivery_tag)

        yield 'data: %s\n\n' % body

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/tweets')
def get_tweets():
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    application.debug = True
    application.run(threaded=True, use_reloader=False)
