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

FILELOCK = threading.RLock()  # Mutex lock for reading and writing csv files.
MAXSIZE = 100 * 1024 * 1024  # Maximum size of one csv file - 100MB.
TABLEHEADER = ['user_url_token', 'user_data_json']


class DataFile:
    def __init__(self):
        self.__filepath = os.path.join(os.path.abspath('.'), 'datafile')
        self.__prefix = os.path.join(self.__filepath, 'data')
        self.__suffix = '.csv'
        self.__currentfile = ''
        self.__updatecurrentfile()
        pass

    def __updatecurrentfile(self):
        """Traverse every csv file to find a unfilled csvfile as currentfile.
        if such a file doesn't exist, create a new csv file.

        Parameters:
            None.

        Returns:
            None.
        """
        if os.path.exists(self.__currentfile) and os.path.getsize(self.__currentfile) < MAXSIZE:
            return

        if not os.path.exists(self.__filepath):
            os.mkdir(self.__filepath)

        FILELOCK.acquire()
        i = 0
        while True:
            i += 1
            # generate a filename.
            filename = self.__prefix + ("%04d" % i) + self.__suffix

            if os.path.exists(filename):
                if os.path.getsize(filename) < MAXSIZE:
                    # if the file exists and the file is unfilled, set the file to currentfile.
                    self.__currentfile = filename
                    break
                else:
                    continue
            else:
                # if the file doesn't exists, Create a new csv file, and write table header in.
                with open(filename, 'w', newline='') as csvfile:
                    # Create table header.
                    headerrow = dict()
                    for x in TABLEHEADER:
                        headerrow[x] = x
                    # Write in.
                    writer = csv.DictWriter(csvfile, TABLEHEADER)
                    writer.writerow(headerrow)
                self.__currentfile = filename
                break
        FILELOCK.release()
        return

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

    def adduserinfo(self, userinfo):
        FILELOCK.acquire()
        self.__updatecurrentfile()
        with open(self.__currentfile, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, TABLEHEADER)
            writer.writerow(userinfo)
        FILELOCK.release()
        return True

    def adduserinfobatch(self, userinfolist):
        FILELOCK.acquire()
        self.__updatecurrentfile()
        with open(self.__currentfile, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, TABLEHEADER)
            for userinfo in userinfolist:
                writer.writerow(userinfo)
        FILELOCK.release()
        return True


df = DataFile()
print(df.getusercrawled())
df.adduserinfobatch([{'user_url_token': 'u11', 'user_data_json': 'json11'},
                {'user_url_token': 'u12', 'user_data_json': 'json12'},
                {'user_url_token': 'u13', 'user_data_json': 'json13'},
                {'user_url_token': 'u14', 'user_data_json': 'json14'}])

