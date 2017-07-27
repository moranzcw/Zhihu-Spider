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
import login

headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/59.0.3071.115 Safari/537.36"
}


def get_user_data_json(session, user_url_token):
    # Access the user following page.
    user_following_url = "https://www.zhihu.com/people/" + user_url_token + "/following"
    response = session.get(user_following_url, headers=headers)
    data_json = dict()
    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            data_json_text = soup.body.contents[1].attrs['data-state']
            data_json = json.loads(data_json_text)
        except:
            data_json = json.loads('')
    return data_json


def get_user_following_list(user_data_json, user_url_token):
    try:
        user_following_list = user_data_json['people']['followingByUser'][user_url_token]['ids']
        temp_set = set(user_following_list)
        temp_set.remove(None)
        user_following_list = list(temp_set)
    except:
        user_following_list = list()
    return user_following_list


def get_user_info(user_data_json, user_url_token):
    try:
        user_data = user_data_json['entities']['users'][user_url_token]
        user_data_json_text = json.dumps(user_data)
    except:
        return ''
    return user_data_json_text


if __name__ == '__main__':
    session = requests.session()
    session = login.load_cookie(session)
    if not login.is_login(session):
        session = login.login(session)

    user_url_token = "moranzcw"
    user_data_json = get_user_data_json(session, user_url_token)
    user_following_list = get_user_following_list(user_data_json, user_url_token)
    user_info = get_user_info(user_data_json, user_url_token)
