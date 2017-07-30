#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Required
- requests
- bs4 (Beautiful Soup)
Info
- author : "moran"
- github : "moranzcw@gmail.com"
- date   : "2017.7.27"
"""
import requests
from bs4 import BeautifulSoup
import json
import threading
import queue
from zhihusession import ZhihuSession

headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/59.0.3071.115 Safari/537.36"
}


def get_page_json(session, user_url_token):
    # Access the user following page.
    user_following_url = "https://www.zhihu.com/people/" + user_url_token + "/following"
    response = session.get(user_following_url, headers=headers)
    page_json = dict()
    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            page_json_text = soup.body.contents[1].attrs['data-state']
            page_json = json.loads(page_json_text)
        except:
            page_json = json.loads('')
    return page_json


def get_user_following_list(page_json, user_url_token):
    try:
        user_following_list = page_json['people']['followingByUser'][user_url_token]['ids']
        temp_set = set(user_following_list)
        temp_set.remove(None)
        user_following_list = list(temp_set)
    except:
        user_following_list = list()
    return user_following_list


def get_user_info(page_json, user_url_token):
    try:
        user_info_json = page_json['entities']['users'][user_url_token]
        user_info = json.dumps(user_info_json)
    except:
        return ''
    return user_info


if __name__ == '__main__':
    session = ZhihuSession()

    user_url_token = "moranzcw"
    user_data_json = get_page_json(session, user_url_token)
    user_following_list = get_user_following_list(user_data_json, user_url_token)
    user_info = get_user_info(user_data_json, user_url_token)

