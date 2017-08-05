#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Info
- author : "moran"
- github : "moranzcw@gmail.com"
- date   : "2017.7.24"
"""
import os
import time
from threading import Thread
from queue import Queue
import json
from crawlsession import CrawlSession
import datafile

__author__ = """\
  ___    ___
 |   \  /   |
 |    \/    | ______  __ ___  ___ __  ______
 |  |\  /|  |/  __  \|  '___//  _`  ||  '_  \ 
 |  | \/ |  |  (__)  |  |   |  (_|  ||  | |  |
 |__|    |__|\______/|__|    \___,__||__| |__|"""

tocrawl_queue = Queue(maxsize=100000)
response_queue = Queue()
df = datafile.DataFile()

concurrent = 5
threads_numbers = 1
interval_time = threads_numbers/concurrent


class MasterThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.count = {
            'crawled_count': 0,
            'tocrawl_count': 0,
            'response_count': 0,
            'success_count': 0,
            'failed_count': 0,
            'last_time': 0.0
        }
        # 从文件读取已爬取用户的list，并转换为set，用户去重
        crawled_list = df.loadusercrawled()
        self.crawled_set = set(crawled_list)
        self.tocrawl_set = set()
        # 从文件读取待爬取用户的列表，并导入待爬取用户的queue
        tocrawled_list = df.loaduseruncrawled(self.crawled_set)
        for token in tocrawled_list:
            try:
                tocrawl_queue.put_nowait(token)
                self.tocrawl_set.add(token)
            except:
                continue
        self.count['crawled_count'] = len(crawled_list)
        self.count['tocrawl_count'] = tocrawl_queue.qsize()

    def log(self):
        curtime = time.time()
        interval = curtime - self.count['last_time']
        if interval > 1.0:
            self.count['last_time'] = curtime
        else:
            return

        os.system('cls')
        print('\033[1;32m')
        print(__author__)
        print('\033[0m')

        print("已爬取：\033[1;33;46m" + str(self.count['crawled_count']) + "\033[0m个")
        print("待爬取队列：\033[1;33;46m%6d\033[0m'个，响应队列：\033[1;33;46m%d\033[0m个"
              % (self.count['tocrawl_count'], self.count['response_count']))
        print("获取：\033[1;33;46m%2.2f\033[0m个/秒，未获取：\033[1;33;46m%2.2f\033[0m个/秒"
              % (self.count['success_count']/interval, self.count['failed_count']/interval))
        self.count['success_count'] = 0
        self.count['failed_count'] = 0
        pass

    def run(self):
        while self.count['crawled_count'] < 10000000:
            resposeitem = response_queue.get()

            # 确认是否爬取到一个用户信息，若是，则加入已爬取集合中
            if resposeitem['state'] == 'OK':
                self.crawled_set.add(resposeitem['user_url_token'])
                self.count['crawled_count'] += 1
                self.count['success_count'] += 1
            else:
                self.count['failed_count'] += 1

            # 无论是否成功爬取，都从待爬取集合中删除
            if resposeitem['user_url_token'] in self.tocrawl_set:
                self.tocrawl_set.remove(resposeitem['user_url_token'])

            # 获得用户关注列表，并去重
            followinglist = resposeitem['user_following_list']
            for token in followinglist:
                if token not in self.crawled_set and token not in self.tocrawl_set:
                    try:
                        tocrawl_queue.put_nowait(token)
                        self.tocrawl_set.add(token)
                    except:
                        continue

            self.count['tocrawl_count'] = tocrawl_queue.qsize()
            self.count['response_count'] = response_queue.qsize()

            self.log()

        print("Master thread exited.")
        pass


class WorkerThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        session = CrawlSession()

        last_time = time.time()
        while True:
            if (time.time() - last_time) < interval_time:
                continue
            else:
                last_time = time.time()

            try:
                token = tocrawl_queue.get(block=True, timeout=30)
            except:
                break

            info = session.getinfo(token)

            temp = json.loads(info['user_following_list'])
            resposeitem = {'user_url_token': info['user_url_token'],
                           'user_following_list': temp['ids']
                           }
            if len(info['user_data_json']) == 0:
                resposeitem['state'] = 'Cannot_Obtain'
                resposeitem['length'] = 0
            else:
                df.saveinfo(info)
                resposeitem['state'] = 'OK'
                resposeitem['length'] = len(info['user_data_json'])

            response_queue.put(resposeitem)
        print("Worker thread exited.")

if __name__ == '__main__':
    master_thread = MasterThread()

    worker_list = []
    for i in range(threads_numbers):
        worker_thread = WorkerThread()
        worker_list.append(worker_thread)

    master_thread.start()
    for t in worker_list:
        t.start()

    master_thread.join()
    for t in worker_list:
        t.join()

