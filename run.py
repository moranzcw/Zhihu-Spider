#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Info
- author : "moran"
- github : "moranzcw@gmail.com"
- date   : "2017.7.24"
"""
import time
from threading import Thread
from queue import Queue
import json
from crawlsession import CrawlSession
import datafile
import os

__author__ = """\
  /\/\   ___  _ __ __ _ _ __  
 /    \ / _ \| '__/ _` | '_ \ 
/ /\/\ \ (_) | | | (_| | | | |
\/    \/\___/|_|  \__,_|_| |_|"""

tocrawl_queue = Queue(maxsize=100000)
response_queue = Queue()
df = datafile.DataFile()

threads_numbers = 20


class MasterThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.count = {
            'crawled_count': 0,
            'tocrawl_count': 0,
            'response_count': 0,
            'success_count': 0,
            'failed_count': 0,
            'data_count': 0,
            'last_time': 0.0
        }
        # 从文件读取已爬取用户的list，并转换为set，用户去重
        print("加载已爬取用户列表...")
        crawled_list = df.loadusercrawled()
        self.crawled_set = set(crawled_list)
        self.tocrawl_set = set()
        # 从文件读取待爬取用户的列表，并导入待爬取用户的queue
        print("生成任务队列...")
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

        print("已获取：\033[30;47m" + str(self.count['crawled_count']) + "\033[0m用户")
        print("任务队列：\033[30;47m%d\033[0m用户" % self.count['tocrawl_count'])
        print("响应队列：\033[30;47m%d\033[0m用户" % self.count['response_count'])
        print("有效：\033[30;47m%.2f\033[0m用户/秒" % (self.count['success_count']/interval))
        print("无效：\033[30;47m%.2f\033[0m用户/秒" % (self.count['failed_count']/interval))
        print("并发：\033[30;47m%.2f\033[0m请求/秒" % ((self.count['failed_count']+self.count['success_count'])/interval))
        print("有效带宽：\033[30;47m%.2f\033[0m kbps" % ((self.count['data_count']*8/1024)/interval))

        self.count['success_count'] = 0
        self.count['failed_count'] = 0
        self.count['data_count'] = 0
        pass

    def run(self):
        while self.count['crawled_count'] < 10000000:
            resposeitem = response_queue.get()

            # 确认是否爬取到一个用户信息，若是，则加入已爬取集合中
            if resposeitem['state'] == 'OK':
                self.crawled_set.add(resposeitem['user_url_token'])
                self.count['crawled_count'] += 1
                self.count['data_count'] += resposeitem['length']
                self.count['success_count'] += 1
            else:
                self.count['failed_count'] += 1

            # 无论是否成功爬取，都从待爬取集合中删除
            if resposeitem['user_url_token'] in self.tocrawl_set:
                self.tocrawl_set.remove(resposeitem['user_url_token'])

            # 获得用户关注列表，并去重
            followinglist = resposeitem['user_following_list']
            for token in followinglist:
                if tocrawl_queue.qsize() > 99000:
                    break
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

        while True:

            try:
                token = tocrawl_queue.get(block=True, timeout=30)
            except:
                break

            info = session.getinfo(token)

            tempjson = json.loads(info['user_following_list'])

            resposeitem = {'user_url_token': info['user_url_token'],
                           'user_following_list': tempjson['ids']
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

