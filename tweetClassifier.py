import re
import math
import json

class tweetClassifier:
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
				pos[ word ] = 0
				neg[ word ] = 0
				if label:
					pos[ word ] += 1
				else:
					neg[ word ] += 1
		
		return pos, neg

	def _extractFeatures( self, tweet, words ):
		"""
		generates features for a single tweet
		"""
		features = dict()
		for word in words:
			features[ word ] = word in tweet

		return features

	def classify( self, tweet ):
		"""
		classify a tweet as negative or positive
		"""
		if self.trained:
			processed = self._cleanTweet( tweet )
			features = self._extractFeatures( processed, self.probs.keys() )
			pos = math.log10( self.pos_prob )
			neg = math.log10( 1 - self.pos_prob )
			
			for word in features.keys():
				if features[ word ]:
					if self.probs[ word ] == 0.0:
						pos += -100.0 # add miniscule value 1e-100
					elif self.probs[ word ] == 1.0:
						neg += -100.0 # add miniscule value 1e-100
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
			self.probs[ word ] = float( pos[ word ] ) / ( pos[ word ] + neg[ word ] )
		
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
use to run tests
"""
if __name__ == '__main__':
	tweets = ['I love this car', 'This view is amazing', 'I feel great this morning',
			  'I am so excited about the concert', 'He is my best friend', 'I do not like this car',
			  'This view is horrible', 'I feel tired this morning', 'I am not looking forward to the concert',
			  'He is my enemy']

	labels = [True, True, True, True, True, False, False, False, False, False]

	clf = tweetClassifier()
	clf.train( tweets, labels )
	print clf.classify( 'I love you!' )
	print clf.to_json()