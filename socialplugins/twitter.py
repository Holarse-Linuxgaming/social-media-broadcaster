#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import base64
import configparser
import mysql.connector
import logging


class Twitter:

    def __init__(self, access_key, access_secret):
        """
         The token and the secret are encoded in Base64 because
         of the policies of Twitter.
         https://blog.nelhage.com/2010/09/dear-twitter/
        """
        self.cr_token = base64.b16decode("676C34386C707750537248664F5049524E4C"
                                         "584C7266667954").decode("utf-8")
        self.cr_secret = base64.b16decode("30374C524C4A4A5667684C5763365168397"
                                          "76E794767674E51657A7A644F6330425448"
                                          "5A7173457437766271774D47397A6F"
                                          ).decode("utf-8")
        self.access_key = access_key
        self.access_secret = access_secret
        self.logger = logging.getLogger(__name__)

    @property
    def api(self):
        try:
            auth = tweepy.OAuthHandler(self.cr_token, self.cr_secret)
            auth.set_access_token(self.access_key, self.access_secret)
            return tweepy.API(auth)
        except tweepy.TweepError as error:
            self.logger.error('Can not login to Twitter: ' + error)
            return False

    def make_message(self, title, url):
        """
        Builds the message (Tweet) for Twitter.

        The maximum length of a Tweet is limited to 140 characters and
        links will be shortened to 23 characters. Because of that
        the description (title) of the feed can have 117 characters.
        """
        tweet = title + ': ' + url

        if len(title) > 115:
            length_url_and_space = 23 + 9
            length_for_title = 140 - length_url_and_space
            tweet = title[:length_for_title] + ' (...): ' + url
            return tweet
        else:
            return tweet

    def send_message(self, text, rss_tbl_name, rss_row_id):
        """
        Sends the message to Twitter and update the database
        """
        api = self.api
        try:
            message = api.update_status(status=text)
            if message:
                config = configparser.ConfigParser()
                config.read('config.ini')
                mysql_user = config.get('MySQL', 'username')
                mysql_pw = config.get('MySQL', 'password')
                mysql_host = config.get('MySQL', 'host')
                mysql_db = config.get('MySQL', 'database')
                mysql_tbl_sc = 'social_twitter'
                message_time = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
                message_url = 'https://twitter.com/' + \
                              message.user.screen_name + '/status/' +  \
                              message.id_str
                try:
                    mysql_cn = mysql.connector.connect(user=mysql_user,
                                                       password=mysql_pw,
                                                       host=mysql_host,
                                                       database=mysql_db)
                    mysql_insert_cr = mysql_cn.cursor()
                    query_social = ("""
                                    INSERT INTO {0} ({0}.message, {0}.time,
                                                                  {0}.url)
                                    VALUES (%s, %s, %s)
                                    """).format(mysql_tbl_sc)
                    mysql_insert_cr.execute(query_social, (text,
                                                           message_time,
                                                           message_url))
                    message_row_id = mysql_insert_cr.lastrowid
                    mysql_cn.commit()
                    query_broadcast = ("""
                                       INSERT INTO broadcast
                                       (broadcast.id_modules,
                                        broadcast.id_social,
                                        broadcast.id_reference_modules,
                                        broadcast.id_reference_social)
                                       VALUES
                                       ((SELECT modules.id
                                         FROM modules
                                         WHERE modules.table = %s),
                                        (SELECT social.id
                                         FROM social
                                         WHERE social.table = %s),
                                        %s,
                                        %s)
                                        """)
                    mysql_insert_cr.execute(query_broadcast, (rss_tbl_name,
                                                              mysql_tbl_sc,
                                                              rss_row_id,
                                                              message_row_id))
                    mysql_cn.commit()

                except mysql.connector.Error as err:
                    errorcode = mysql.connector.errorcode
                    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                        self.logger.error("MySQL: Invalid Login")
                    elif err.errno == errorcode.ER_BAD_DB_ERROR:
                        self.logger.error("MySQL: Database does not exist")
                    else:
                        self.logger.error("MySQL: " + err)
                else:
                    mysql_insert_cr.close()
                    mysql_cn.close()
        except tweepy.TweepError as error:
            self.logger.error('Can not post the message on Twitter.')
