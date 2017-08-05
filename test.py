#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Info
- author : "moran"
- github : "moranzcw@gmail.com"
- date   : "2017.7.24"
"""
from threading import Thread
from crawlsession import CrawlSession


class WorkerThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        pass

if __name__ == '__main__':

    worker_list = []
    for i in range(1):
        worker_thread = WorkerThread()
        worker_list.append(worker_thread)

    for t in worker_list:
        t.start()
    for t in worker_list:
        t.join()
