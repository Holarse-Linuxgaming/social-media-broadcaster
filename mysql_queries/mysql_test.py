#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector

try:
    name = 'socialmediabroadcaster'
    mysql_connection = mysql.connector.connect(user=name,
                                               password='test',
                                               host='localhost',
                                               database=name)
    mysql = mysql_connection.cursor()
    query = ("""
             SELECT rss_holarse.title, rss_holarse.url,
                    social_gnusocial.message
             FROM rss_holarse
             JOIN broadcast on rss_holarse.id = broadcast.id_reference_modules
             JOIN modules on broadcast.id_modules = modules.id
             JOIN social on social.id = broadcast.id_social
             JOIN social_gnusocial on
             social_gnusocial.id = broadcast.id_reference_social
             GROUP BY rss_holarse.id
             """)
    mysql.execute(query)

    for(title, url, queet) in mysql:
        print(title, url)
        print(queet)
except mysql.connector.Error as err:
    errorcode = mysql.connector.errorcode
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Username or password is wrong")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    mysql.close()
    mysql_connection.close()
