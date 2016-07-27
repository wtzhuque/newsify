#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: minidb.py
Author: wtzhuque(wtzhuque@163.com)
Date: 2016/07/25 11:00:15
"""


import tornado
import tornado.web
import tornado.ioloop
import argparse
import leveldb
import logging
import json
import ConfigParser


class MiniDB(tornado.web.Application):
    """
    Mini DB with rest api
    """
    def __init__(self, config):
        self.__db = leveldb.LevelDB(config.get('leveldb', 'path'))
        handlers = [
            (r'/get', DBGetHandler, dict(db = self.__db)),
            (r'/set', DBSetHandler, dict(db = self.__db))
        ]
        settings = dict()
        tornado.web.Application.__init__(self, handlers, settings)


class DBGetHandler(tornado.web.RequestHandler):
    """
    Handle get request of db
    """
    def initialize(self, db):
        """
        init handler, get db instance
        """
        self.__db = db

    def get(self):
        keys = self.get_query_arguments('key')
        res = {}
        for key in keys:
            try:
                val = json.loads(self.__db.Get(key))
                res[key] = json.loads(val_str)
            except Exception as e:
                res[key] = None

        self.write(json.dumps(res))
        return


class DBSetHandler(tornado.web.RequestHandler):
    """
    Handle set request of db
    """
    def initialize(self, db):
        """
        init handler, get db instance
        """
        self.__db = db

    def post(self):
        return


def main():
    """
    Main entry
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default = './conf/config', help = 'config file')
    args = parser.parse_args()
    
    config = ConfigParser.ConfigParser()
    if not config.read(args.config):
        logging.warn('load config file [%s] failed' % args.config)
        return

    port = config.getint('service', 'port')
    
    app_db = MiniDB(config)
    app_db.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

