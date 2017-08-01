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
from crawlsession import CrawlSession
import datafile

tobecrawled_queue = Queue(maxsize=100000)
response_queue = Queue()


class MasterThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # Load crawled users from file, and create a crawled users set.
        usercrawled_list = datafile.loadusercrawled()
        print(len(usercrawled_list))
        crawled_set = set(usercrawled_list)

        # Load 'uncrawled' users from file in last time, and create a 'to be crawled' users set.
        usertobecrawled_list = datafile.loadusertobecrawled()
        tobecrawled_set = set()
        if len(usertobecrawled_list) == 0:
            usertobecrawled_list.append('excited-vczh')
        for token in usertobecrawled_list:
            try:
                tobecrawled_queue.put(token)
                tobecrawled_set.add(token)
            except:
                continue

        # Main loop.
        lasttime = time.time()
        crawledcount = len(usercrawled_list)

        while crawledcount < 10000000:
            resposeitem = response_queue.get()

            # Confirm a crawled user.
            if resposeitem['state'] == 'OK':
                crawled_set.add(resposeitem['user_url_token'])
                tobecrawled_set.remove(resposeitem['user_url_token'])
                crawledcount += 1
            else:
                tobecrawled_set.remove(resposeitem['user_url_token'])

            # Filter the followinglist.
            followinglist = resposeitem['user_following_list']
            for token in followinglist:
                if token in crawled_set or token in tobecrawled_set:
                    print(token)
                    continue
                else:
                    try:
                        tobecrawled_queue.put(token)
                        tobecrawled_set.add(token)

                    except:
                        continue

            print('User: ' + resposeitem['user_url_token']
                  + ', State: ' + resposeitem['state']
                  + ', Data length: ' + str(resposeitem['length'])
                  + ', following: ' + str(len(resposeitem['user_following_list'])))
            print('Crawled user: ' + str(len(crawled_set))
                  + ', tobecrawled_queue: ' + str(tobecrawled_queue.qsize())
                  + ', Data response_queue: ' + str(response_queue.qsize()))

            # Save crawled users every 30 seconds.
            curtime = time.time()
            if (curtime - lasttime) > 30:
                lasttime = curtime
                datafile.saveusertobecrawled(list(tobecrawled_set))

        print("Master thread exited.")
        pass


class WorkerThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        session = CrawlSession()
        df = datafile.DataFile()

        while True:
            try:
                token = tobecrawled_queue.get(block=True, timeout=30)
            except:
                break

            followinglist = session.getfollowinglist(token)
            info = session.getinfo(token)

            resposeitem = {'user_url_token': token,
                           'user_following_list': followinglist
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
    for i in range(5):
        worker_thread = WorkerThread()
        worker_list.append(worker_thread)

    master_thread.start()
    for t in worker_list:
        t.start()

    master_thread.join()
    for t in worker_list:
        t.join()
