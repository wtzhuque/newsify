#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: kv_storage.py
Author: wangtao(wangtao@baidu.com)
Date: 2016/03/24 13:20:46
"""

import argparse
import logging
import leveldb
import redis


class KVStorageLocal(object):
    """
    Local implemention for kv storage
    """
    def __init__(self, path):
        self.__db = leveldb.LevelDB(path)

    def get(self, key):
        try:
            return self.__db.Get(key)
        except KeyError as key_err:
            return None

    def set(self, key, value):
        return self.__db.Put(key, value)


class KVStorageRedis(object):
    """
    Redis implemention for kv storage
    """
    def __init__(self, redis_host, redis_port):
        self.__redis = redis.Redis(redis_host, redis_port)

    def get(self, key):
        return self.__redis.get(key)

    def set(self, key, value):
        return self.__redis.set(key, value)


