import configparser
import modules.rssfeed
import socialplugins.twitter

# TODO: Fix Lenght of a Tweet!

config = configparser.ConfigParser()
config.read('config.ini')
intervall = config.get('General', 'timer', fallback='30')
intervall = int(intervall)


def main():
    for sections in config.sections():
        if (config.has_option(sections, 'plugin') and
                config.get(sections, 'plugin')):
            url = config.get(sections, 'url', fallback='no')
            updates = read_rss(intervall, url)
            if updates is not False:
                print('There is an update!')
                send_to_twitter(updates)
            else:
                print('There is currently no updates.')


def read_rss(intervall, url):
    if url != 'no':
        rssfeed = modules.rssfeed.RSSFeed(url)
        return rssfeed.check_article_update(intervall)


def send_to_twitter(array):
    consumer_key = config.get('Twitter', 'CONSUMER_KEY')
    consumer_secret = config.get('Twitter', 'CONSUMER_SECRET')
    access_key = config.get('Twitter', 'ACCESS_KEY')
    access_secret = config.get('Twitter', 'ACCESS_SECRET')

    for title_key, rss_entries in array.items():
        tweet = title_key + ': ' + rss_entries[0]
        if len(tweet) > 140:
            print('TODO: Fix Lenght of a Tweet!')
        else:
            print(tweet)
            twitter \
                = socialplugins.twitter.Twitter(consumer_key, consumer_secret,
                                                access_key, access_secret)
            twitter.sendTweet(tweet)

if __name__ == "__main__":
    main()
