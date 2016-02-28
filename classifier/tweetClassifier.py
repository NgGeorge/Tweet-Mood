import re
import math
import json

class tweetClassifier():
	"""
	classifies tweets as positive or negative through the use of a naive bayes classifier
	"""

	def __init__( self ):
		"""
		only declares class variables
		"""
		self.trained = False
		self.probs = dict()
		self.pos_prob = 0.5

	def _cleanTweet( self, tweet ):
		"""
		split message, removing words 2 char or shorter and non alphanumeric characters
		"""
		return re.sub( r'(\b\w{1,2}\b|[^a-zA-Z\d\s])', '', tweet ).lower().split()

	def _uniqueWords( self, tweets, labels ):
		"""
		occurrences of words as negative and positive
		"""
		pos = dict()
		neg = dict()
		for tweet, label in zip( tweets, labels ):
			for word in tweet:
				if word not in pos.keys():
					pos[ word ] = 0
				
				if word not in neg.keys():
					neg[ word ] = 0

				if label:
					pos[ word ] += 1
				else:
					neg[ word ] += 1
		
		return pos, neg

	def classify( self, tweet ):
		data = self.probabilities( tweet )
		if data[ 'positive' ] > 0.7:
			return 'positive'
		elif data[ 'negative' ] > 0.7:
			return 'negative'
		else:
			return 'neutral'

	def probabilities( self, tweet ):
		"""
		produce probabilities of negative and positive
		"""
		if self.trained:
			processed = self._cleanTweet( tweet )
			pos = math.log10( self.pos_prob )
			neg = math.log10( 1 - self.pos_prob )
			
			for word in processed:
				if word in self.probs.keys():
					if self.probs[ word ] == 0.0:
						pos += -30.0 # add miniscule value 1e-100
					elif self.probs[ word ] == 1.0:
						neg += -30.0 # add miniscule value 1e-100
					else:
						pos += math.log10( self.probs[ word ] )
						neg += math.log10( 1 - self.probs[ word ] )

			pos = 10**pos
			neg = 10**neg
			return { 'positive': pos / ( pos + neg ), 'negative': neg / ( pos + neg ) }
		else:
			raise RunTimeError('must train classifier before classifying')

	def train( self, tweets, labels ):
		"""
		train classifier using training tweets and labels
		"""
		if len( tweets ) != len( labels ):
			raise ValueError( 'number of tweets and labels are mismatching' )

		processed = [ self._cleanTweet( tweet ) for tweet in tweets ]
		pos, neg = self._uniqueWords( processed, labels )
		self.pos_prob = float( sum( labels ) ) / len( labels )

		for word in pos.keys():
			self.probs[ word ] = float( pos[ word ] ) / float( pos[ word ] + neg[ word ] )
		
		self.trained = True

	def to_json( self ):
		"""
		save state of tweet classifier to json string
		"""
		return json.dumps( { 'trained': self.trained, 'probs': self.probs, 'pos_prob': self.pos_prob } )
		
	def from_json( self, saved ):
		"""
		load state of tweet classifier from json string
		"""
		data = json.loads( saved )
		self.trained = data[ 'trained' ]
		self.probs = data[ 'probs' ]
		self.pos_prob = data[ 'pos_prob' ]

"""
train classifier
"""
if __name__ == '__main__':
	raw_tweets = open( 'messages1.txt', 'r' )
	raw_labels = open( 'labels1.txt', 'r' )

	data_tweets = json.loads( raw_tweets.read() )
	data_labels = json.loads( raw_labels.read() )

	raw_tweets.close()
	raw_labels.close()

	tweets = list()
	labels = list()
	for key in data_labels.keys():
		tweets.append( data_tweets[ key ] )
		labels.append( data_labels[ key ] )

	clf = tweetClassifier()
	clf.train( tweets, labels )
	
	save = open( 'save_trained.txt', 'w+' )
	save.write( clf.to_json() )
	save.close()