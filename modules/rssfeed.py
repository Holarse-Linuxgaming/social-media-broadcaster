#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
import time
import configparser
import mysql.connector
import logging


class RSSFeed:

    def __init__(self, rssfeed):
        self.rssfeed = feedparser.parse(rssfeed)
        self.logger = logging.getLogger(__name__)

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

    def check_article_update(self, rss_name, intervall=0):
        article_news = {}
        if (intervall == 0 or intervall > 0 and
                self.check_last_update(intervall)):
            config = configparser.ConfigParser()
            config.read('config.ini')
            mysql_user = config.get('MySQL', 'username')
            mysql_pw = config.get('MySQL', 'password')
            mysql_host = config.get('MySQL', 'host')
            mysql_db = config.get('MySQL', 'database')
            mysql_tbl = 'rss_' + rss_name
            try:
                mysql_connection = mysql.connector.connect(user=mysql_user,
                                                           password=mysql_pw,
                                                           host=mysql_host,
                                                           database=mysql_db)
                mysql_cursor = mysql_connection.cursor()
                for entries in self.rssfeed.entries:
                    article_time = entries.published_parsed
                    local_time = time.gmtime()
                    difference \
                        = time.mktime(article_time) - time.mktime(local_time)
                    difference = int((difference / 60)) * -1
                    if (intervall == 0 or difference >= 0 and
                            difference <= intervall):
                        query = ("""
                                 SELECT {0}.title
                                 FROM {0}
                                 WHERE {0}.title = %s
                                 LIMIT 1
                                 """).format(mysql_tbl)
                        mysql_cursor.execute(query, (entries.title, ))
                        mysql_cursor.fetchone()
                        if mysql_cursor.rowcount == -1:
                            article_news[entries.title] = [entries.link,
                                                           entries.summary,
                                                           article_time]
            except mysql.connector.Error as err:
                errorcode = mysql.connector.errorcode
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    self.logger.error('MySQL: Invalid Login')
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    self.logger.error('MySQL: Database does not exist')
                else:
                    self.logger.error(err)
            else:
                mysql_cursor.close()
                mysql_connection.close()
            if article_news == {}:
                return False
            else:
                return article_news

    def debug_output(self):
            print(self.title)
            print(self.description)
            articles = 1
            for entries in self.rssfeed.entries:
                if articles <= 5:
                    self.logger.debug(entries.title)
                    self.logger.debug(time.strftime('Date: %d.%m.%Y'
                                                    'Time: %H:%M:%S',
                                                    entries.published_parsed))
                    articles = articles + 1
