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

    def make_tweet(self, title, url):
        tweet = title + ': ' + url

        if len(tweet) > 140:
            lenght_url = len(url)
            length_for_title = lenght_url + 7

            tweet = title[:length_for_title] + '(...): ' + url
            return tweet
        else:
            return tweet

    def send_tweet(self, tweet):
        api = self.api
        api.update_status(status=tweet)
