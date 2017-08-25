#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description
- 实现多线程，主线程和若干工作线程。
- 主线程：维护一个已爬取用户的set，用于去重；从响应队列中取出关注用户的列表，去重后放入任务队列。
- 工作线程：从任务队列获取url token，爬取用户信息后，存入csv文件；并生成响应信息放入响应队列。
Info
- author : "moran"
- github : "moranzcw@gmail.com"
- date   : "2017.7.24"
"""
import time
import os
import json
from threading import Thread
from queue import Queue
from crawl import Crawl
from datafile import DataFile

__author__ = """\
  /\/\   ___  _ __ __ _ _ __  
 /    \ / _ \| '__/ _` | '_ \ 
/ /\/\ \ (_) | | | (_| | | | |
\/    \/\___/|_|  \__,_|_| |_|"""

# 任务队列，从主线程到工作线程
task_queue = Queue(maxsize=100000)
# 响应队列，从工作线程到主线程
response_queue = Queue()

# 数据文件操作接口
df = DataFile()
# 用户信息获取接口
crawl = Crawl()

# 工作线程的数量
threads_numbers = 20


class MasterThread(Thread):
    """
    主线程

    Attributes:
        count: 状态信息，用于实时显示爬虫状态
        crawled_set: 已爬取用户集合，用于去除重复用户
        task_set: 待爬取用户集合，元素与任务队列保持一致，用于去除重复用户
    """
    def __init__(self):
        Thread.__init__(self)
        # 用与log函数展示实时进度
        self.count = {
            'crawled_count': 0,  # 已爬取用户数量
            'task_count': 0,  # 任务数量
            'response_count': 0,  # 响应数量
            'success_count': 0,  # 单位时间获取用户信息成功数量
            'failed_count': 0,  # 单位时间获取用户失败数量
            'data_count': 0,  # 单位时间获取用户信息的总字节数
            'last_time': 0.0  # 上次刷新时间
        }
        # 从文件读取已爬取用户的list，并转换为set，用于去重
        print("加载已爬取用户列表...")
        crawled_list = df.loadusercrawled()
        self.crawled_set = set(crawled_list)
        # 从文件读取待爬取用户的列表，并导入任务队列
        print("生成任务队列...")
        self.task_set = set()
        tocrawled_list = df.loaduseruncrawled(self.crawled_set)
        for token in tocrawled_list:
            try:
                task_queue.put_nowait(token)
                self.task_set.add(token)
            except:
                continue
        self.count['crawled_count'] = len(crawled_list)
        self.count['task_count'] = task_queue.qsize()

    def run(self):
        while self.count['crawled_count'] < 10000000:
            responseitem = response_queue.get()

            # 确认是否爬取到一个用户信息，若是，则加入已爬取集合中
            if responseitem['state'] == 'OK':
                self.crawled_set.add(responseitem['user_url_token'])
                # 更新状态新信息
                self.count['crawled_count'] += 1
                self.count['data_count'] += responseitem['length']
                self.count['success_count'] += 1
            else:
                self.count['failed_count'] += 1

            # 无论是否成功爬取，都从待爬取集合中删除
            if responseitem['user_url_token'] in self.task_set:
                self.task_set.remove(responseitem['user_url_token'])

            # 获得用户关注列表，并去重
            followinglist = responseitem['user_following_list']
            for token in followinglist:
                if task_queue.qsize() > 99000:
                    break
                if token not in self.crawled_set and token not in self.task_set:
                    try:
                        task_queue.put_nowait(token)
                        self.task_set.add(token)
                    except:
                        continue
            # 输出状态信息
            self.log()

        print("Master thread exited.")
        pass

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

        self.count['task_count'] = task_queue.qsize()
        self.count['response_count'] = response_queue.qsize()

        print("已获取：\033[30;47m" + str(self.count['crawled_count']) + "\033[0m用户")
        print("任务队列：\033[30;47m%d\033[0m用户" % self.count['task_count'])
        print("响应队列：\033[30;47m%d\033[0m用户" % self.count['response_count'])
        print("有效：\033[30;47m%.2f\033[0m用户/秒" % (self.count['success_count']/interval))
        print("无效：\033[30;47m%.2f\033[0m用户/秒" % (self.count['failed_count']/interval))
        print("并发：\033[30;47m%.2f\033[0m请求/秒" % ((self.count['failed_count']+self.count['success_count'])/interval))
        print("有效带宽：\033[30;47m%.2f\033[0m kbps" % ((self.count['data_count']*8/1024)/interval))

        self.count['success_count'] = 0
        self.count['failed_count'] = 0
        self.count['data_count'] = 0
        pass


class WorkerThread(Thread):
    """
    工作线程

    Attributes:
        None.
    """
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            # 从任务队列获取一个url token
            try:
                token = task_queue.get(block=True, timeout=30)
            except:
                break

            # 获取该用户信息
            info = crawl.getinfo(token)
            # 生成响应信息，每个响应包含一个保存用户信息的json和该用户的关注列表
            tempjson = json.loads(info['user_following_list'])
            responseitem = {'user_url_token': info['user_url_token'],
                           'user_following_list': tempjson['ids']
                           }

            if len(info['user_data_json']) == 0:
                # 未获取到用户信息，在响应信息中加入失败状态
                responseitem['state'] = 'Cannot_Obtain'
                responseitem['length'] = 0
            else:
                # 获取到用户信息，在响应信息中加入成功状态
                df.saveinfo(info)
                responseitem['state'] = 'OK'
                responseitem['length'] = len(info['user_data_json'])

            # 将响应信息放入响应队列
            response_queue.put(responseitem)
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

