#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import logging
import configparser
import mysql.connector
import time
import xml.etree.ElementTree as ET


class GNUSocial:

    def __init__(self, url, username, password):
        self.url = url + '/api/statuses/update.xml'
        self.username = username
        self.password = password
        self.logger = logging.getLogger(__name__)

    def make_message(self, title, url):
        """
        The maximum length of a queet is 1024 characters.
        """
        queet = title + ': ' + url

        if len(queet) > 1024:
            lenght_url = len(url)
            length_for_title = 1024 - lenght_url + 7
            # 7 is for '(...): '

            queet = title[:length_for_title] + '(...): ' + url
            return queet
        else:
            return queet

    def send_message(self, text, rss_tbl_name, rss_row_id):
        send = requests.post(self.url, auth=(self.username, self.password),
                             data={'status': text})
        if send.status_code is requests.codes.ok:
            config = configparser.ConfigParser()
            config.read('config.ini')
            mysql_user = config.get('MySQL', 'username')
            mysql_pw = config.get('MySQL', 'password')
            mysql_host = config.get('MySQL', 'host')
            mysql_db = config.get('MySQL', 'database')
            mysql_tbl_sc = 'social_gnusocial'

            xml_root = ET.fromstring(send.text)
            message_url = xml_root.find("external_url").text
            message_time = xml_root.find("created_at").text
            message_time = time.strptime(message_time,
                                         "%a %b %d %H:%M:%S %z %Y")
            message_time = time.strftime('%Y-%m-%d %H:%M:%S', message_time)
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
        else:
            self.logger.error('Social Media Broadcaster:'
                              'Error in Posting the Queet!')
            self.logger.error('Social Media Broadcaster: HTML Error ' +
                              send.status_code)
