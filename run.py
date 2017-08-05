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

tobecrawled_queue = Queue(maxsize=100000)
response_queue = Queue()
df = datafile.DataFile()

concurrent = 5
threads_numbers = 5
interval_time = concurrent/threads_numbers


class MasterThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        # 从文件读取已爬取用户的list，并转换为set，用户去重
        usercrawled_list = df.loadusercrawled()
        self.crawled_count = len(usercrawled_list)
        self.crawled_set = set(usercrawled_list)
        print(len(self.crawled_set))
        # 从文件读取待爬取用户的列表，并导入待爬取用户的queue
        usertobecrawled_list = df.loaduseruncrawled(self.crawled_set)
        for token in usertobecrawled_list:
            try:
                tobecrawled_queue.put_nowait(token)
                self.crawled_set.add(token)
            except:
                continue

    def run(self):
        while self.crawled_count < 10000000:
            resposeitem = response_queue.get()

            # Confirm a crawled user.
            if resposeitem['state'] == 'OK':
                self.crawled_set.add(resposeitem['user_url_token'])
                self.crawled_count += 1
            else:
                if resposeitem['user_url_token'] in self.crawled_set:
                    self.crawled_set.remove(resposeitem['user_url_token'])

            # Filter the followinglist.
            followinglist = resposeitem['user_following_list']
            for token in followinglist:
                if token in self.crawled_set:
                    continue
                else:
                    try:
                        tobecrawled_queue.put_nowait(token)
                    except:
                        continue

            print('User: ' + resposeitem['user_url_token']
                  + ', State: ' + resposeitem['state'])
            print('Data length: ' + str(resposeitem['length'])
                  + ', following: ' + str(len(resposeitem['user_following_list'])))
            print('Crawled user: ' + str(self.crawled_count)
                  + ', tobecrawled_queue: ' + str(tobecrawled_queue.qsize())
                  + ', Data response_queue: ' + str(response_queue.qsize()))
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
                token = tobecrawled_queue.get(block=True, timeout=30)
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
