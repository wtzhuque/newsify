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
import argparse
import leveldb
import logging
import ConfigParser


class MiniDB(tornado.web.Application):
    """
    Mini DB with rest api
    """
    def __init__(self, config):
        handlers = [
            (r'/get', GetHandler),
            (r'/set', SetHandler)
        ]


class DBGetHandler(tornado.web.RequestHandler):
    """
    Handle get request of db
    """
    def get(self):
        return


class DBSetHandler(tornado.web.RequestHandler):
    """
    Handle set request of db
    """
    def post(self):
        return


def main():
    """
    Main entry
    """


if __name__ == "__main__":
    main()

