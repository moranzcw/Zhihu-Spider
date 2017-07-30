#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Info
- author : "moran"
- github : "moranzcw@gmail.com"
- date   : "2017.7.24"
"""
from threading import Thread
from queue import Queue
import time

my_queue = Queue()

count = 0


class MyThread1(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        for i in range(100):
            my_queue.put(str(i))
            print("Thread1 put in.")
            time.sleep(1)
        pass


class MyThread2(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        for i in range(100):
            a = my_queue.get()
            print("Thread2 get " + a)
        pass


if __name__ == '__main__':
    thread1 = MyThread1()
    thread2 = MyThread2()
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
