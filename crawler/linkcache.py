#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: minidb.py
Author: wangtao(wangtao@baidu.com)
Date: 2016/03/24 13:20:46
"""

import argparse
import logging
import json
import redis


class LinkCache(object):
    """
    Restore link attrs
    """
    def __init__(self, config):
        redis_host = config.get('linkcache', 'redis-host')
        redis_port = config.get('linkcache', 'redis-port')
        self.__redis = redis.Redis(redis_host, redis_port)

    def get_link_updatetime(self, link):
        time_str = self.__redis.get('%s_updatetime' % link)
        if time_str is not None:
            print 'time_str:', time_str
            return int(time_str)
        return None

    def set_link_updatetime(self, link, timestamp):
        self.__redis.set('%s_updatetime' % link, str(timestamp)) 

    def get_link_attr(self, link, attr):
        """
        Get link attr
        """

    def set_link_attr(self, link, attr, val):
        """
        Set link attr
        """
       
