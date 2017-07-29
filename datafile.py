#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Required
- requests
Info
- author : "moran"
- github : "moranzcw@gmail.com"
- date   : "2017.7.24"
"""
import threading
import csv
import os

FILELOCK = threading.Lock()  # Mutex lock for reading and writing csv files.
MAXROW = 100000  # Maximum number of rows in one csv file.
TABLEHEADER = ['user_url_token', 'user_data_json']

class DataFile:
    def __init__(self):
        self.__filepath = os.path.join(os.path.abspath('.'), 'datafile')
        self.__prefix = os.path.join(os.path.abspath('.'), 'data')
        self.__suffix = '.csv'
        self.__currentfile = ''
        self.__currentfilerows = 0
        pass

    def __createdatafile(self):
        if not os.path.exists(self.__data_path):
            os.mkdir(self.__data_path)

        i = 1
        while i:
            filename = self.__prefix + ("%3d" % i) + self.__suffix
            if not os.path.exists(filename):
                # Create a csv file, and write in table header.
                FILELOCK.acquire()
                with open(filename, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, TABLEHEADER)
                    headerrow = dict()
                    for x in TABLEHEADER:
                        headerrow[x] = x
                    writer.writerow(headerrow)
                self.__currentfile = filename
                self.__currentfilerows = 0
                FILELOCK.release()
                break
            i += 1
        return self.__currentfile

    def __getcurrentfile(self):
        if self.__currentfile == '' or self.__currentfilerows >= MAXROW:
            return self.__createdatafile()
        return self.__currentfile

    def __getfilelist(self):
        if not os.path.exists(self.__filepath):
            return list()

        filelist = list()

        FILELOCK.acquire()
        for filename in os.listdir(self.__filepath):
            filename = os.path.join(self.__filepath, filename)
            if os.path.splitext(filename)[1] == self.__suffix:
                with open(filename, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    if reader.fieldnames == TABLEHEADER:
                        filelist.append(os.path.join(self.__filepath, filename))
        FILELOCK.release()

        return filelist

    def getusercrawled(self):
        if not os.path.exists(self.__filepath):
            return list()

        filelist = self.__getfilelist()
        usercrawled = list()

        FILELOCK.acquire()
        for filename in filelist:
            with open(filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    usercrawled.append(row[TABLEHEADER[0]])
        FILELOCK.release()

        return usercrawled

    def add_user_info(self, userinfo):
        FILELOCK.acquire()
        filename = self.__getcurrentfile()
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, TABLEHEADER)
            writer.writerow(userinfo)
        self.__currentfilerows += 1
        FILELOCK.release()

        return True

    def add_user_info_in_bulk(self, userinfolist):
        FILELOCK.acquire()
        filename = self.__getcurrentfile()
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, TABLEHEADER)
            rowcounter = 0
            for userinfo in userinfolist:
                writer.writerow(userinfo)
                self.__currentfilerows += 1
                rowcounter += 1
                if self.__currentfilerows >= MAXROW:
                    break
        FILELOCK.release()
        return rowcounter

df = DataFile()
# df.create_datafile()
print(df.getusercrawled())
