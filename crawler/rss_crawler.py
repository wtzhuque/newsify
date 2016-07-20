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
import time
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
        url_list = []
        if 'entries' not in rss_doc:
            return doc_list
       
        rss_state = {}
        if rss in self.__state:
            rss_state = self.__state[rss]

        latest_updatetime = 0
        if 'latest_updatetime' in rss_state:
            latest_updatetime = rss_state['latest_updatetime']
        
        cur_latest = latest_updatetime
        for entry in rss_doc.entries:
            timestamp = time.mktime(entry.published_parsed)
            if timestamp <= latest_updatetime:
                continue
            
            if timestamp > cur_latest:
                cur_latest = timestamp

            doc_attr = entry.keys()
            doc = {}
            
            if 'title' in doc_attr:
                doc['title'] = entry.title
            if 'summary' in doc_attr:
                doc['summary'] = entry.summary
            if 'content' in doc_attr:
                doc['content'] = entry.content
            if 'tags' in doc_attr:
                doc['tags'] = entry.tags
            doc['timestamp'] = timestamp
            doc_list.apppend(doc)
        latest_updatetime = cur_latest
        return doc_list, url_list


def dump_docs(doc_list):
    """
    dump docs to local db
    """
    print doc_list


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
        doc_list, url_list = crawler.crawl(rss)
        if len(doc_list) > 0:
            dump_docs(doc_list)


if __name__ == "__main__":
    main()
