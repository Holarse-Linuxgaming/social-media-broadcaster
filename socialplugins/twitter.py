import tweepy

'''
TODO: Check if the Keys and Secrets are correct and if we can login with these keys.
'''

class Twitter:
	def __init__(self, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET):
		self.CONSUMER_KEY = CONSUMER_KEY
		self.CONSUMER_SECRET = CONSUMER_SECRET
		self.ACCESS_KEY = ACCESS_KEY
		self.ACCESS_SECRET = ACCESS_SECRET
	def getApi(self):
		auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
		auth.set_access_token(self.ACCESS_KEY, self.ACCESS_SECRET)
		return tweepy.API(auth)

	def sendTweet(self, Tweet):
		api = self.getApi()
		api.update_status(status=Tweet)