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
import uuid
import time
import socket
import ConfigParser
import feedparser

from minidb import MiniDB
from linkcache import LinkCache

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

    def crawl(self, rss, lastupdate):
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

        latest_updatetime = lastupdate
        if 'latest_updatetime' in rss_state:
            latest_updatetime = rss_state['latest_updatetime']
        
        cur_latest = latest_updatetime
        for entry in rss_doc.entries:
            doc_attr = entry.keys()
            if 'published_parsed' not in doc_attr:
                continue

            timestamp = int(time.mktime(entry.published_parsed))
            if timestamp <= latest_updatetime:
                continue
            
            if timestamp > cur_latest:
                cur_latest = timestamp

            doc = {}
           
            doc['link'] = rss 
            if 'title' in doc_attr:
                doc['title'] = entry.title
            if 'summary' in doc_attr:
                doc['summary'] = entry.summary
            if 'content' in doc_attr:
                doc['content'] = entry.content
            if 'tags' in doc_attr:
                doc['tags'] = entry.tags
            doc['timestamp'] = timestamp
            doc_list.append(doc)
        latest_updatetime = cur_latest
        return doc_list, url_list


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
    db = MiniDB(args.db)
    linkcache = LinkCache(config)

    while True:
        for rss in rss_list:
            timestamp = linkcache.get_link_updatetime(rss)
            try:
                doc_list, url_list = crawler.crawl(rss, timestamp)
            except Exception as e:
                logging.warn('crawl error rss=[%s] err=[%s]' % (rss, str(e)))
                continue

            for doc in doc_list:
                db.set(str(uuid.uuid1()), doc)
                if timestamp:
                    if doc['timestamp'] > timestamp:
                        timestamp = doc['timestamp']
                else:
                    timestamp = doc['timestamp']
            
            if timestamp:
                linkcache.set_link_updatetime(rss, timestamp)
                logging.info('rss=[%s] doc_num=[%d] timestamp=[%d]' % (rss, len(doc_list), timestamp))
            else:
                logging.info('rss=[%s] doc_num=[%d]' % (rss, len(doc_list)))

        time.sleep(300)


if __name__ == "__main__":
    main()
