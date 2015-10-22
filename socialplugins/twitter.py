import tweepy


# TODO: Check if the Keys and Secrets are correct
#       and if we can login with these keys.


class Twitter:

    def __init__(self, consumer_key, consumer_secret,
                 access_key, access_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_key = access_key
        self.access_secret = access_secret

    @property
    def api(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        return tweepy.API(auth)

    def send_tweet(self, tweet):
        api = self.api
        api.update_status(status=tweet)
