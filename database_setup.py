#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup the database for the SocialMediaBroadcaster."""

import configparser
import mysql.connector
import argparse
import os.path
import sys


def structure_action(action, mysql_username, mysql_password,
                     mysql_database, mysql_host):
    """Create, delete or reset the structure for the database."""
    try:
        mysql_cn = mysql.connector.connect(user=mysql_username,
                                           password=mysql_password,
                                           database=mysql_database,
                                           host=mysql_host)
        mysql_cr = mysql_cn.cursor()
        if action == 'create':
            tablesdatabase = 'Tables_in_' + mysql_database
            sql_check_structure = ("""
                                   SHOW TABLES IN {0}
                                   WHERE {1} = 'broadcast'
                                       OR {1} = 'social'
                                       OR {1} = 'modules'
                                    """).format(mysql_database, tablesdatabase)
            mysql_cr.execute(sql_check_structure)
            mysql_cr.fetchall()
            if mysql_cr.rowcount == 3:
                print('There is already a MySQL structure!')
                print('If you want to reset the structure, use the -r or ' +
                      '--reset parameter. ' +
                      '(socialmediabroadcaster_install.py --reset)')
            if mysql_cr.rowcount < 3:
                sql_create_tbl = ("""
                                  DROP TABLE IF EXISTS `broadcast`;
                                  CREATE TABLE `broadcast` (
                                    `id` bigint(20) NOT NULL,
                                    `id_modules` bigint(20) NOT NULL,
                                    `id_social` bigint(20) NOT NULL,
                                    `id_reference_modules` bigint(20) NOT NULL,
                                    `id_reference_social` bigint(20) NOT NULL
                                  ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
                                  ALTER TABLE `broadcast`
                                    ADD PRIMARY KEY (`id`) USING BTREE,
                                    MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

                                  DROP TABLE IF EXISTS `modules`;
                                  CREATE TABLE `modules` (
                                    `id` bigint(20) NOT NULL,
                                    `table` text,
                                    `enabled` int(1) NOT NULL DEFAULT '0'
                                  ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
                                 ALTER TABLE `modules`
                                    ADD PRIMARY KEY (`id`) USING BTREE,
                                    MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

                                 DROP TABLE IF EXISTS `social`;
                                 CREATE TABLE `social` (
                                    `id` bigint(20) NOT NULL,
                                    `table` text
                                 ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
                                 ALTER TABLE `social`
                                    ADD PRIMARY KEY (`id`) USING BTREE,
                                    MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
                                """)
                for result in mysql_cr.execute(sql_create_tbl, multi=True):
                    pass
                mysql_cn.commit()
                print('Structure was successful created!')
        elif action == 'delete' or action == 'reset':
            sql_find_tbls = "SELECT {0}.table FROM {0}"
            tbls = list()
            mysql_cr.execute(sql_find_tbls.format('social'))
            for tbl_name in mysql_cr:
                tbls.append(tbl_name[0])
            mysql_cr.execute(sql_find_tbls.format('modules'))
            for tbl_name in mysql_cr:
                tbls.append(tbl_name[0])
            if action == 'delete':
                qry_drop_tbls = ''
                for tbl_name in tbls:
                    qry_drop_tbls = (qry_drop_tbls + 'DROP TABLE IF EXISTS ' +
                                     tbl_name + ";\n")
                qry_drop_tbls = qry_drop_tbls[:-1]
                qry_drop_tbls = (qry_drop_tbls +
                                 "DROP TABLE IF EXISTS `broadcast`;\n" +
                                 "DROP TABLE IF EXISTS `social`;\n" +
                                 "DROP TABLE IF EXISTS `modules`;")
                for results in mysql_cr.execute(qry_drop_tbls, multi=True):
                    pass
            elif action == 'reset':
                # TODO: Check, if the tables exist on the database
                qry_reset_tbls = ''
                for tbl_name in tbls:
                    qry_reset_tbls = (qry_reset_tbls +
                                      'TRUNCATE TABLE ' + tbl_name +
                                      ";\n")
                qry_reset_tbls = qry_reset_tbls[:-1]
                qry_reset_tbls = (qry_reset_tbls +
                                  "TRUNCATE TABLE `broadcast`;")
                for results in mysql_cr.execute(qry_reset_tbls, multi=True):
                    pass
            mysql_cn.commit()
            if action == 'delete':
                print('Structure was successful deleted!')
            elif action == 'reset':
                print('Structure was successful reset!')
    except mysql.connector.Error as err:
        errorcode = mysql.connector.errorcode
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('MySQL: Invalid Login')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('MySQL: Database does not exist')
        else:
            print('MySQL: ' + str(err))
    else:
        mysql_cr.close()
        mysql_cn.close()


def parse():
    """Parse the arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--delete', action='store_true',
                        help='delete the MySQL database')
    parser.add_argument('-r', '--reset', action='store_true',
                        help='reset the MySQL database')
    opts = parser.parse_args()
    return opts


def main():
    args = parse()
    if os.path.isfile('config.ini'):
        print('Found config file under ' +
              os.path.dirname(os.path.realpath(__file__)) + '!')
        file = 'config.ini'
    elif os.path.isfile('/etc/socialmediabroadcaster/config.ini'):
        print('Found config file under /etc!')
        file = '/etc/socialmediabroadcaster/config.ini'
    else:
        # TODO: Create a config if this is missing
        print('Config not found!')
        sys.exit()
    config = configparser.ConfigParser()
    config.read(file)
    if(config.has_section('MySQL')):
        print('The MySQL section was found!')
        mysql_user = config.get('MySQL', 'username')
        mysql_pw = config.get('MySQL', 'password')
        mysql_host = config.get('MySQL', 'host')
        mysql_db = config.get('MySQL', 'database')
        if args.reset and not args.delete:
            structure_action('reset', mysql_user, mysql_pw,
                             mysql_db, mysql_host)
        elif args.delete and not args.reset:
            structure_action('delete', mysql_user, mysql_pw,
                             mysql_db, mysql_host)
        elif not args.delete and not args.reset:
            structure_action('create', mysql_user, mysql_pw,
                             mysql_db, mysql_host)
        else:
            print('Too many arguments!')
            print('Choice only one, e.g. ./socialmediabroadcaster_install -r')
    else:
        # TODO: Query the MySQL details and save them to the config
        print('Your MySQL settings could not be found.')


if __name__ == "__main__":
    main()
