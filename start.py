#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import logging
import argparse
import mysql.connector
import modules.rssfeed
import time
import socialplugins.twitter
import socialplugins.gnusocial


def main():
    args = parse()
    level = getattr(logging, args.log.upper(), None)
    if not isinstance(level, int):
        raise ValueError('Invalid log level: %s' % args.log)
    logging.basicConfig(filename='socialmediabroadcaster.log', filemode='a',
                        level=level,
                        format='%(asctime)s %(levelname)s:%(message)s')
    logging.getLogger(__name__)
    logging.debug('Starting SocialMediaBroadcaster.')
    config = configparser.ConfigParser()
    config.read('config.ini')
    intervall = config.get('General', 'timer', fallback='0')
    intervall = int(intervall)

    mysql_user = config.get('MySQL', 'username')
    mysql_pw = config.get('MySQL', 'password')
    mysql_host = config.get('MySQL', 'host')
    mysql_db = config.get('MySQL', 'database')
    mysql_cn = mysql.connector.connect(user=mysql_user, password=mysql_pw,
                                       host=mysql_host, database=mysql_db)
    mysql_cr = mysql_cn.cursor()

    for sections in config.sections():
        if (config.has_option(sections, 'plugin') and
                config.get(sections, 'plugin')):
            if config.get(sections, 'plugin') == 'rssfeed':
                url = config.get(sections, 'url')
                rss = modules.rssfeed.RSSFeed(url)
                section_name = sections.lower()
                rss_entries = rss.check_article_update(section_name, intervall)
                rss_tbl_name = 'rss_' + section_name

                if rss_entries:
                    for rss_title, rss_entry in rss_entries.items():
                        insert_feed = ("""
                                       INSERT INTO {0}
                                       ({0}.title, {0}.url, {0}.time)
                                       VALUES (%s, %s, %s)
                                       """).format(rss_tbl_name)
                        entry_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                   rss_entry[2])
                        mysql_cr.execute(insert_feed, (rss_title, rss_entry[0],
                                                       entry_time))
                        mysql_cn.commit()
                        rss_feed_id = mysql_cr.lastrowid

                        if config.has_section('Twitter'):
                            access_key = config.get('Twitter', 'ACCESS_KEY')
                            access_secret = config.get('Twitter',
                                                       'ACCESS_SECRET')
                            twitter =  \
                                socialplugins.twitter.Twitter(access_key,
                                                              access_secret)
                            message = twitter.make_message(rss_title,
                                                           rss_entry[0])
                            twitter.send_message(message, rss_tbl_name,
                                                 rss_feed_id)
                        if config.has_section('GNUSocial'):
                            username = config.get('GNUSocial', 'username')
                            password = config.get('GNUSocial', 'password')
                            gnu_url = config.get('GNUSocial', 'url')
                            gnusocial =  \
                                socialplugins.gnusocial.GNUSocial(gnu_url,
                                                                  username,
                                                                  password)
                            message = gnusocial.make_message(rss_title,
                                                             rss_entry[0])
                            gnusocial.send_message(message, rss_tbl_name,
                                                   rss_feed_id)


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log', metavar='level', action='store',
                        default='INFO',
                        choices=['debug', 'info', 'warning',
                                 'error', 'critical'],
                        help='Sets the level of the logs. (%(choices)s)')
    opts = parser.parse_args()
    return opts


if __name__ == "__main__":
    main()
