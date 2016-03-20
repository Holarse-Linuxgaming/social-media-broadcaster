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
              SELECT rss_holarse.title
              FROM rss_holarse
              WHERE rss_holarse.title = %s
              LIMIT 1
             """)
    title = 'Paradox feiert Cities Skylines-Jubiläum ' \
            'mit kostenlosem Content-Update'
    mysql.execute(query, (title, ))
    rows = mysql.fetchall()
    if mysql.rowcount > 0:
        print('Artikel ist vorhanden')
    else:
        print('Artikel ist nicht vorhanden')
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
