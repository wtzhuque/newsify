#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: rss_crawler.py
Author: wangtao(wangtao@baidu.com)
Date: 2016/03/24 13:20:46
"""


import argparse
import logging
import leveldb
import socket
import ConfigParser

import feedparser


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

socket.setdefaulttimeout(12)

class RSSCrawler(object):
    """
    Crawler for rss feed
    """
    def __init__(self):
        self.__state = {}

    def crawl(self, rss):
        """
        Crawl rss page
        """
        logging.info("fetch rss %s" % rss)
        rss_doc = feedparser.parse(rss)
        doc_list = []
        if 'entries' not in rss_doc:
            return doc_list
        
        for entry in rss_doc.entries:
            doc = {}
            doc['title'] = entry.title
            logging.info("title => %s" % entry.title)
            doc['summary'] = entry.summary
            doc['content'] = entry.content
            doc['tags'] = entry.tags
            logging.info("tags => %s" % entry.tags)


def main():
    """
    Main Entry
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--rss', help = 'start pages')
    parser.add_argument('-d', '--db', default = './db', help = 'output db')
    parser.add_argument('-c', '--config', default = './conf/config', help = 'config file')
    args = parser.parse_args()
    
    config = ConfigParser.ConfigParser()
    if not config.read(args.config):
        logging.warn('load config file [%s] failed' % args.config)
        return

    rss_list = []

    if args.rss is not None:
        rss_file = open(args.rss)
        for line in rss_file.readlines():
            rss_list.append(line.strip())
        rss_file.close()

    if not rss_list:
        logging.warn('no seed page specified, will exit')
        return

    crawler = RSSCrawler()

    for rss in rss_list:
        crawler.crawl(rss)


if __name__ == "__main__":
    main()
