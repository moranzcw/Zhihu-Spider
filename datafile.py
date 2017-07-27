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
import csv
import os

table_header = ['user_id', 'user_url_token']
datafile_name = 'data.csv'


def create_datafile(table_header):
    if os.path.exists(datafile_name):
        return

    with open('data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, table_header)
        header_row = dict()
        for x in table_header:
            header_row[x] = x
        writer.writerow(header_row)


def add_user_info(user_info, table_header):
    if not os.path.exists(datafile_name):
        create_datafile(table_header)

    with open(datafile_name, 'a', newline='') as datafile:
        writer = csv.DictWriter(datafile, table_header)
        writer.writerow(user_info)


def add_user_info_in_bulk(user_info_list, table_header):
    if not os.path.exists(datafile_name):
        create_datafile(table_header)

    with open(datafile_name, 'a', newline='') as datafile:
        writer = csv.DictWriter(datafile, table_header)
        for user_info in user_info_list:
            writer.writerow(user_info)

# user_info = {'user_id': 'sdsd', 'user_url_token': 'sdgdfg'}
# user_info_list = [user_info, user_info]
# create_datafile(table_header)
# add_user_info(user_info, table_header)
# add_user_info_in_bulk(user_info_list, table_header)

