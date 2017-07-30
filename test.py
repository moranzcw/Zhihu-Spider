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
crawled_queue = Queue()


class MasterThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # Load crawled users from file, and create a crawled users set.
        usercrawled_list = datafile.loadusercrawled()
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
            crawleditem = crawled_queue.get()

            # Confirm a crawled user.
            crawled_set.add(crawleditem['user_url_token'])
            tobecrawled_set.remove(crawleditem['user_url_token'])
            crawledcount += 1

            # Filter the followinglist.
            followinglist = crawleditem['user_following_list']
            for token in followinglist:
                if token in crawled_set or token in tobecrawled_set:
                    continue
                else:
                    try:
                        tobecrawled_queue.put_nowait(token)
                        tobecrawled_set.add(token)
                    except:
                        continue

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

            info = session.getinfo(token)
            df.saveinfo(info)

            followinglist = session.getfollowinglist(token)
            crawleditem = {'user_url_token': token, 'user_following_list': followinglist}
            crawled_queue.put(crawleditem)
        print("Worker thread exited.")

if __name__ == '__main__':
    master_thread = MasterThread()

    worker_list = []
    for i in range(2):
        worker_thread = WorkerThread()
        worker_list.append(worker_thread)

    master_thread.start()
    for t in worker_list:
        t.start()

    master_thread.join()
    for t in worker_list:
        t.join()
