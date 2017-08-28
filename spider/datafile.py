#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description
- 将知乎用户的个人信息json存储到csv文件中。
- 实现了一些必要的功能：
    - 从已有的csv文件中提取出所有用户，用于程序中断后重启时加载已爬取用户列表。
    - 从已有的csv文件中提取指定数目的未爬取用户，用于程序中断后重启时生成任务队列。
- 类DataFile为单例模式，在程序中只有一个实例。
- 线程安全。
Info
- author: "moran"
- github: "moranzcw@gmail.com"
- date: "2017.7.24"
"""
import threading
import csv
import sys
import os.path
import json

__author__ = """\
  /\/\   ___  _ __ __ _ _ __  
 /    \ / _ \| '__/ _` | '_ \ 
/ /\/\ \ (_) | | | (_| | | | |
\/    \/\___/|_|  \__,_|_| |_|"""

# 操作文件时使用的可重入互斥锁，用于保证线程安全
FILELOCK = threading.Lock()


class Singleton(object):
    """
    实现单例模式，DataFile在程序中只有一个实例

    Attributes:
        _instance: 唯一实例的引用。
    """
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance


class DataFile(Singleton):
    """
    操作csv文件，保存用户数据。

    Attributes:
        FILEPATH: 存储数据文件（csv文件）的文件夹绝对路径
        PREFIX: 每个csv文件的文件名前缀，包含绝对路径。每个文件名由 “前缀” + 编号 + “后缀” 组成。
        SUFFIX: 每个csv文件的文件名后缀，即格式 '.csv'
        MAXSIZE: 每个csv文件的最大尺寸，单位Byte
        TABLEHEADER: 每个csv文件的表头，也就是第一行内容，方便使用csv库中的DictWriter/DictReader按dict方式存取
        __currentfile: 当前操作文件的绝对路径文件名，由于数据较大，分多个文件保存，所以需要变量来指向当前操作的文件
    """
    def __init__(self):
        self.FILEPATH = os.path.join(os.path.dirname(sys.path[0]), 'datafile')  # 此脚本文件路径的上一级路径
        self.PREFIX = os.path.join(self.FILEPATH, 'data')
        self.SUFFIX = '.csv'
        self.MAXSIZE = 100 * 1024 * 1024
        self.TABLEHEADER = ['user_url_token', 'user_data_json', 'user_following_list']
        self.__currentfile = ''
        self.__updatecurrentfile()
        pass

    def loadusercrawled(self):
        """加载已爬取用户列表。

        从已有的csv文件加载已经爬取用户的url token，即每个csv文件的第一列，得到一个列表。
        此函数用于爬虫程序中断后重启时的状态恢复。

        Args:
            None.

        Returns:
            list: 一个包含已经爬取用户的url token的list。

        Raises:
            None.
        """
        # 数据文件夹不存在，就返回一个空列表
        if not os.path.exists(self.FILEPATH):
            return list()

        FILELOCK.acquire()
        # 从存储数据文件的文件夹中找出所有csv文件，得到一个包含所有csv绝对路径文件名的list。
        csvfilelist = list()
        for filename in os.listdir(self.FILEPATH):
            filename = os.path.join(self.FILEPATH, filename)
            if os.path.splitext(filename)[1] == self.SUFFIX:
                with open(filename, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    if reader.fieldnames == self.TABLEHEADER:
                        csvfilelist.append(os.path.join(self.FILEPATH, filename))

        # 从上面的列表中，依次遍历每个文件，得到一个包含已经爬取用户的url token的list。
        usercrawled = list()
        for filename in csvfilelist:
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    usercrawled.append(row[self.TABLEHEADER[0]])

        FILELOCK.release()
        return usercrawled

    def loaduseruncrawled(self, usercrawled_set, user_count=100000):
        """加载未爬取用户列表。

        从已有的csv文件加载已经爬取用户的关注列表（csv文件的第三列），
        并用已爬取用户列表去重，得到一个未爬取用户的列表。
        默认加载100000个未爬取用户。
        此函数用于爬虫程序中断后重启时的状态恢复。

        Args:
            None.

        Returns:
            list: 一个包含未爬取用户的url token的list。

        Raises:
            None.
        """
        if not os.path.exists(self.FILEPATH):
            useruncrawled = list()
            useruncrawled.append('excited-vczh')
            return useruncrawled

        FILELOCK.acquire()
        # 从存储数据文件的文件夹中找出所有csv文件，得到一个包含所有csv绝对路径文件名的list。
        csvfilelist = list()
        for filename in os.listdir(self.FILEPATH):
            filename = os.path.join(self.FILEPATH, filename)
            if os.path.splitext(filename)[1] == self.SUFFIX:
                with open(filename, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    if reader.fieldnames == self.TABLEHEADER:
                        csvfilelist.append(os.path.join(self.FILEPATH, filename))
        csvfilelist.sort()

        # 从上面的列表中，依次遍历每个文件，得到一个不超过100000个未爬取用户的列表。
        useruncrawled = list()
        for filename in csvfilelist[::-1]:
            if len(useruncrawled) >= user_count:
                break
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                user_following_list = list()
                for row in reader:
                    tempjson = json.loads(row[self.TABLEHEADER[2]])
                    user_following_list += tempjson['ids']
                for user in user_following_list[::-1]:
                    if len(useruncrawled) >= 100000:
                        break
                    if user not in usercrawled_set:
                        useruncrawled.append(user)
        FILELOCK.release()

        if len(useruncrawled) == 0:
            useruncrawled.append('excited-vczh')
        return useruncrawled

    def __updatecurrentfile(self):
        """更新当前操作文件。

        由于数据较大，分多个文件保存，每个文件不超过100MB，所以需要不断检查已有文件
        的大小，当大小达到限制，就创建一个新文件，并更新__currentfile变量的文件名。

        Args:
            None.

        Returns:
            None.

        Raises:
            None.
        """
        # 数据文件夹不存在，创建一个数据文件夹
        if not os.path.exists(self.FILEPATH):
            os.mkdir(self.FILEPATH)

        FILELOCK.acquire()
        # 从'data0001.csv'开始依次按序号生成文件名，判断目录下是否已存在该文件；
        # 若存在该文件：
        #   文件大小不到设置的MAXSIZE，就将该文件作为当前操作文件，并退出函数；
        #   文件大小已经达到设置的MAXSIZE，就继续生成下一个文件名，重复以上操作；
        # 若不存在该文件：
        #   用这个文件名创建一个新csv文件，做为当前操作文件，并退出函数。
        i = 0
        while True:
            i += 1
            # generate a filename.
            filename = self.PREFIX + ("%04d" % i) + self.SUFFIX

            if os.path.exists(filename):
                if os.path.getsize(filename) < self.MAXSIZE:
                    # if the file exists and the file is unfilled, set the file to currentfile.
                    self.__currentfile = filename
                    break
                else:
                    continue
            else:
                # if the file doesn't exists, Create a new csv file, and write table header in.
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    # Create table header.
                    headerrow = dict()
                    for x in self.TABLEHEADER:
                        headerrow[x] = x
                    # Write in.
                    writer = csv.DictWriter(csvfile, self.TABLEHEADER)
                    writer.writerow(headerrow)
                self.__currentfile = filename
                break
        FILELOCK.release()
        return None

    def __getcurrentfile(self):
        """获取当前操作文件。

        由于文件实时更新，所以在每次存取文件前，需要确认__currentfile指向的文件没有过期。
        若__currentfile指向的文件存在且文件大小未达到MAXSIZE，则直接返回__currentfile；
        若__currentfile指向的文件不存在或者文件大小达到MAXSIZE，则更新__currentfile；

        Args:
            None.

        Returns:
            str: 返回指向当前操作文件的文件名（包含绝对路径）。

        Raises:
            None.
        """
        if os.path.exists(self.__currentfile) and os.path.getsize(self.__currentfile) < self.MAXSIZE:
            return self.__currentfile
        else:
            self.__updatecurrentfile()
        return self.__currentfile

    def saveinfo(self, userinfo):
        """存入用户信息。

        传入一个包含用户信息的dict，并写入当前操作文件。
        其中dict的key与TABLEHEADER中的每个item一一对应。

        Args:
            userinfo: 一个包含用户信息的dict, 其中TABLEHEADER中的每个item作为这个dict中的一个key，
                value则是每个key对应的用户信息

        Returns:
            bool: 用户信息已经写入文件.

        Raises:
            None.
        """

        result = True
        filename = self.__getcurrentfile()
        FILELOCK.acquire()
        # filename = self.PREFIX + '0002' + self.SUFFIX
        try:
            with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, self.TABLEHEADER)
                writer.writerow(userinfo)
        except:
            result = False
        FILELOCK.release()
        return result

    def saveinfobatch(self, userinfolist):
        """批量存入用户信息。

        传入一个包含多个用户信息的list，每个item与均为dict，表示一个用户，其他同saveinfo函数。
        本函数用于提升写入效率，降低操作文件的次数

        Args:
            userinfolist: 一个包含多个用户信息的list, 每个item与均为dict，表示一个用户，其他同saveinfo函数。

        Returns:
            bool: 用户信息已经写入文件.

        Raises:
            None.
        """

        result = True
        filename = self.__getcurrentfile()
        FILELOCK.acquire()
        try:
            with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, self.TABLEHEADER)
                for userinfo in userinfolist:
                    writer.writerow(userinfo)
        except:
            result = False
        FILELOCK.release()

        return result


if __name__ == '__main__':
    pass
