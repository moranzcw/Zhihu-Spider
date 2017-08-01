#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Info
- author : "moran"
- github : "moranzcw@gmail.com"
- date   : "2017.7.24"
"""
import threading
import csv
import os.path

FILEPATH = os.path.join(os.path.abspath('.'), 'datafile')  # Path for the data file.

USERTOBECRAWLED_FILELOCK = threading.RLock()  # Mutex lock for reading and writing user to be crawled file.
USERTOBECRAWLED_FILENAME = 'usertobecrawled.txt'  # File name for user to be crawled .


def loadusertobecrawled():
    usertobecrawled = list()

    if not os.path.exists(FILEPATH):
        return usertobecrawled

    filename = os.path.join(FILEPATH, USERTOBECRAWLED_FILENAME)
    if not os.path.exists(filename):
        return usertobecrawled

    USERTOBECRAWLED_FILELOCK.acquire()
    with open(filename, 'r') as file:
        for line in file.readlines():
            line = line.strip('\n')
            usertobecrawled.append(line)
    USERTOBECRAWLED_FILELOCK.release()

    return usertobecrawled


def saveusertobecrawled(usertobecrawled):
    if not os.path.exists(FILEPATH):
        os.mkdir(FILEPATH)

    filename = os.path.join(FILEPATH, USERTOBECRAWLED_FILENAME)

    USERTOBECRAWLED_FILELOCK.acquire()
    with open(filename, 'w', newline='') as file:
        for token in usertobecrawled:
            file.write(token+'\n')
    USERTOBECRAWLED_FILELOCK.release()

    return True


FILELOCK = threading.RLock()  # Mutex lock for reading and writing csv files.
PREFIX = os.path.join(FILEPATH, 'data')
SUFFIX = '.csv'
MAXSIZE = 100 * 1024 * 1024  # Maximum size of one csv file - 100MB.
TABLEHEADER = ['user_url_token', 'user_data_json']


def loadusercrawled():
    usercrawled = list()

    if not os.path.exists(FILEPATH):
        return usercrawled

    csvfilelist = list()
    FILELOCK.acquire()
    # Find every csv file in FILEPATH.
    for filename in os.listdir(FILEPATH):
        filename = os.path.join(FILEPATH, filename)
        if os.path.splitext(filename)[1] == SUFFIX:
            with open(filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                if reader.fieldnames == TABLEHEADER:
                    csvfilelist.append(os.path.join(FILEPATH, filename))

    # Read in every url token from every csv file.
    for filename in csvfilelist:
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                usercrawled.append(row[TABLEHEADER[0]])
    FILELOCK.release()

    return usercrawled


class DataFile:
    def __init__(self):
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
        if not os.path.exists(FILEPATH):
            os.mkdir(FILEPATH)

        FILELOCK.acquire()
        i = 0
        while True:
            i += 1
            # generate a filename.
            filename = PREFIX + ("%04d" % i) + SUFFIX

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

    def __getcurrentfile(self):
        if os.path.exists(self.__currentfile) and os.path.getsize(self.__currentfile) < MAXSIZE:
            return self.__currentfile
        else:
            self.__updatecurrentfile()
        return self.__currentfile

    def saveinfo(self, userinfo):
        FILELOCK.acquire()
        filename = self.__getcurrentfile()
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, TABLEHEADER)
            writer.writerow(userinfo)
        FILELOCK.release()
        return True

    def saveinfobatch(self, userinfolist):
        FILELOCK.acquire()
        filename = self.__getcurrentfile()
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, TABLEHEADER)
            for userinfo in userinfolist:
                writer.writerow(userinfo)
        FILELOCK.release()
        return True


if __name__ == '__main__':
    ff = loadusercrawled()
    print(ff)
    # saveusertobecrawled(ff)
