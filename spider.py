#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import re
import login

headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/59.0.3071.115 Safari/537.36"
}


# 9ffd5c016aabeafd1030e63fe410beb8

# {"avatar_url_template": "https://pic2.zhimg.com/c7d53b471237006a318de480af7fd44d_{size}.jpg",
# "badge": [],
# "type": "people",
# "name": "\u8c46\u6d46\u6cb9\u6761",
# "url": "http://www.zhihu.com/api/v4/people/9ffd5c016aabeafd1030e63fe410beb8",
# "gender": 0,
# "user_type": "people",
# "is_advertiser": false,
# "avatar_url": "https://pic2.zhimg.com/c7d53b471237006a318de480af7fd44d_is.jpg",
# "is_org": false,
# "headline": "\u5fae\u535a\uff1aCammmilla",
# "url_token": "li-zi-qing-68-6",
# "id": "9ffd5c016aabeafd1030e63fe410beb8"}


# 1. GET USER URL TOKEN

def get_user_data_dict(session, user_id):
    # Access the user data in json.
    user_data_url = "https://www.zhihu.com/api/v4/members/" + user_id
    response = session.get(user_data_url, headers=headers)

    # Format the json data into a dict.
    user_data_dict = dict()
    if response.status_code == 200:
        try:
            user_data_dict = response.json()
        except:
            return user_data_dict
    return user_data_dict


def get_user_url_token(user_data_dict):
    # Get user url token.
    try:
        user_url_token = user_data_dict['url_token']
    except:
        return ''
    return user_url_token


# 2. GET USER FOLLOWING LIST

user_id_regex = r'(?<=api/v4/people/).{32}'
user_id_pattern = re.compile(user_id_regex)


def get_user_following_page(session, user_url_token):
    # Access the user following page.
    user_following_url = "https://www.zhihu.com/people/" + user_url_token + "/following"
    response = session.get(user_following_url, headers=headers)
    if response.status_code == 200:
        return response.text
    return ''


def get_user_following_id_list(user_following_page):
    # Parse out the following list from the page.
    user_following_id_list = user_id_pattern.findall(user_following_page)
    user_following_id_list = list(set(user_following_id_list))
    return user_following_id_list


# 3. GET USER

def get_user_info(user_data_dict, user_following_page):
    # Get user information.
    try:
        user_info = [user_data_dict['id'],
                     user_data_dict['url_token'],
                     user_data_dict['name'],
                     user_data_dict['headline'],
                     user_data_dict['avatar_url_template'],
                     user_data_dict['avatar_url']]
    except:
        return list()

    # try:
    #
    # except:

    return user_info


if __name__ == '__main__':
    session = requests.session()
    session = login.load_cookie(session)
    if login.isLogin(session):
        print("OK")
    else:
        session = login.login(session)
    user_data_dict = get_user_data_dict(session, "9ffd5c016aabeafd1030e63fe410beb8")
    print(user_data_dict)
    user_url_token = get_user_url_token(user_data_dict)
    print(user_url_token)

    user_following_page = get_user_following_page(session, user_url_token)
    # print(user_following_page)
    user_following_id_list = get_user_following_id_list(user_following_page)
    print(user_following_id_list)

    user_info = get_user_info(user_data_dict, user_following_page)
    print(user_info)


