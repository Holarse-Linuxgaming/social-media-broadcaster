import configparser
import tweepy
import base64


def main():
    cr_token = base64.b16decode("676C34386C707750537248664F5049524E4C58"
                                "4C7266667954").decode("utf-8")
    cr_secret = base64.b16decode("30374C524C4A4A5667684C576336516839776E"
                                 "794767674E51657A7A644F63304254485A7173"
                                 "457437766271774D47397A6F").decode("utf-8")
    auth = tweepy.OAuthHandler(cr_token, cr_secret)
    print("[Social Media Broadcaster]: Please open this URL and authorize the "
          "Application:")
    print("\n" + auth.get_authorization_url() + "\n")
    pin = input("[Social Media Broadcaster]: Verification pin number from "
                "twitter.com: ").strip()

    try:
        auth.get_access_token(pin)
        print("[Social Media Broadcaster]:")
        print("  Key: %s" % auth.access_token)
        print("  Secret: %s" % auth.access_token_secret)
        print("  Updating the Config ...")
        print("  Please keep the Key and the Secret save from others!")
        write(auth.access_token, auth.access_token_secret)
    except tweepy.TweepError:
        print("[Social Media Broadcaster]: Error! Failed to get access token.")


def write(access_key, access_secret):
    config = configparser.ConfigParser()
    config.read("../config.ini")
    config.set("Twitter", "ACCESS_KEY", access_key)
    config.set('Twitter', "ACCESS_SECRET", access_secret)
    with open("../config.ini", "w") as configfile:
        config.write(configfile)

if __name__ == "__main__":
    main()
