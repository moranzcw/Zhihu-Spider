#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Required
- requests
Info
- author : "moran"
- email  : "moranzcw@gmail.com"
- github : "moranzcw@gmail.com"
- date   : "2017.7.24"
"""

from threading import Thread
from queue import Queue

my_queue = Queue()


class MyThread1(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # put_data = "you producer data"
        # my_queue.put(put_data)
        pass


class MyThread2(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        get_data = my_queue.get()
        print(get_data)
        pass


if __name__ == '__main__':
    thread1 = MyThread1()
    thread2 = MyThread2()
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
