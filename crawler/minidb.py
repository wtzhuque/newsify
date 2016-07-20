#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: minidb.py
Author: wangtao(wangtao@baidu.com)
Date: 2016/03/24 13:20:46
"""

import argparse
import logging
import leveldb
import json


class MiniDB(object):
    """
    Mini db based on leveldb
    """
    def __init__(self, path):
        self.__db = leveldb.LevelDB(path)

    def get(self, key):
        return json.loads(self.__db.Get(key))

    def set(self, key, val):
        return self.__db.Put(key, json.dumps(val))

