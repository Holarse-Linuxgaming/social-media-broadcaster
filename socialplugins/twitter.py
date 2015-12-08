import tweepy
import base64


# TODO: Check if the Keys and Secrets are correct
#       and if we can login with these keys.


class Twitter:

    def __init__(self, access_key, access_secret):
        self.cr_token = base64.b16decode("676C34386C707750537248664F5049524E4C"
                                         "584C7266667954").decode("utf-8")
        self.cr_secret = base64.b16decode("30374C524C4A4A5667684C5763365168397"
                                          "76E794767674E51657A7A644F6330425448"
                                          "5A7173457437766271774D47397A6F"
                                          ).decode("utf-8")
        self.access_key = access_key
        self.access_secret = access_secret

    @property
    def api(self):
        auth = tweepy.OAuthHandler(self.cr_token, self.cr_secret)
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
