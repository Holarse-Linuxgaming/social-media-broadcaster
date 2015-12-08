import configparser
import modules.rssfeed
import socialplugins.twitter
import socialplugins.gnusocial

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
                send_to_twitter(updates)
                send_to_gnusocial(updates)


def read_rss(intervall, url):
    if url != 'no':
        rssfeed = modules.rssfeed.RSSFeed(url)
        return rssfeed.check_article_update(intervall)


def send_to_twitter(array):
    access_key = config.get('Twitter', 'ACCESS_KEY')
    access_secret = config.get('Twitter', 'ACCESS_SECRET')

    for title_key, rss_entries in array.items():
            twitter = socialplugins.twitter.Twitter(access_key, access_secret)
            tweet = twitter.make_tweet(title_key, rss_entries[0])
            print('Social Media Broadcaster: (Twitter) ' + tweet)
            twitter.send_tweet(tweet)


def send_to_gnusocial(array):
    username = config.get('GNUSocial', 'username')
    password = config.get('GNUSocial', 'password')
    url = config.get('GNUSocial', 'url')

    for title_key, rss_entries in array.items():
            gnusocial \
                = socialplugins.gnusocial.GNUSocial(url, username, password)
            queet = gnusocial.make_queet(title_key, rss_entries[0])
            print('Social Media Broadcaster: (GnuSocial) ' + queet)
            gnusocial.send_queet(queet)


if __name__ == "__main__":
    main()
