#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
"""
File: parser.py
Author: wangtao(wtzhuque@163.com)
Date: 2016/08/01 17:52:45
"""

import argparse
import logging
import leveldb
import ConfigParser


class Parser(object):
    """
    Parser
    """
    def parse(self, doc):
        """
        Parse doc
        """


def main():
    """
    Main Entry
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data', default = './data', help = 'input data, leveldb')
    parser.add_argument('-c', '--config', default = './conf/config', help = 'config file')
    args = parser.parse_args()
    
    config = ConfigParser.ConfigParser()
    if not config.read(args.config):
        logging.warn('load config file [%s] failed' % args.config)
        return

    data = leveldb.LevelDB(args.data)
    for doc_key in data.RangeIter(include_value=False):
        print 'doc=>', str(doc_key)



if __name__ == "__main__":
    main()
