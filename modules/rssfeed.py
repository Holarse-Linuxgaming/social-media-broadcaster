import feedparser
import time


# TODO:   Implement fallbacks for RSS Feeds, where the 'created' or 'published'
#         tags are missing


class RSSFeed:

    def __init__(self, rssfeed):
        self.rssfeed = feedparser.parse(rssfeed)

    @property
    def title(self):
        return self.rssfeed.feed.title

    @property
    def description(self):
        return self.rssfeed.feed.description

    @property
    def last_update(self):
        try:
            return self.rssfeed.published_parsed
        except AttributeError:
            # If there is no lastBuildDate or similiar in the RSSFeed
            return self.rssfeed.updated_parsed

    def check_last_update(self, update_time):
        local_time = time.gmtime()
        feed_update_time = self.last_update
        difference = time.mktime(feed_update_time) - time.mktime(local_time)
        difference = int((difference / 60)) * -1

        if difference <= update_time and difference >= 0:
            return True
        else:
            return False

    def check_article_update(self, intervall):
        article_news = {}
        if self.check_last_update(intervall):
            for entries in self.rssfeed.entries:
                article_time = entries.published_parsed
                locale_time = time.gmtime()
                difference \
                    = time.mktime(article_time) - time.mktime(locale_time)
                difference = int((difference / 60)) * -1

                if difference <= intervall and difference >= 0:
                    article_title = entries.title
                    article_short_description = entries.summary
                    article_url = entries.link
                    article_news[article_title] = [article_url,
                                                   article_short_description]
            if article_news == {}:
                return False
            else:
                return article_news
        else:
            return False

    def debug_output(self):
            print(self.title)
            print(self.description)
            articles = 1
            for entries in self.rssfeed.entries:
                if articles <= 5:
                    print(entries.title)
                    print(time.strftime('Date: %d.%m.%Y Time: %H:%M:%S',
                                        entries.published_parsed))
                    articles = articles + 1
