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
import requests
import re
from bs4 import BeautifulSoup
import login

headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/59.0.3071.115 Safari/537.36"
}


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


# 3. GET USER INFORMATION

# user_name_regex = r'(?<=<span class="ProfileHeader-name">).{0,30}(?=</span>)'
# user_name_pattern = re.compile(user_name_regex)
# # <span class="RichText ProfileHeader-headline">FXXK MY CAR节目主持人  |  old school</span>
# user_headline_regex = r'(?<=<span class="RichText ProfileHeader-headline">).{0,50}(?=</span>)'
# user_headline_pattern = re.compile(user_headline_regex)
# # <span><!-- react-text: 1181 -->现居<!-- /react-text --><!-- react-text: 1182 -->上海<!-- /react-text --></span>
# user_location_regex = r'(?<=<span><!-- react-text: \d{2,6} -->现居<!-- /react-text --><!-- react-text: \d{2,6} -->)' \
#                       r'.{0,20}' \
#                       r'(?=<!-- /react-text --></span>)'
# user_location_pattern = re.compile(user_location_regex)
# # <span><!-- react-text: 1049 -->现居<!-- /react-text --><!-- react-text: 1050 -->ghjgj<!-- /react-text --></span>
# user_occupation_regex = r'(?<=<span class="ProfileHeader-name">).{0,30}(?=</span>)'
# user_occupation_pattern = re.compile(user_occupation_regex)
#
# user_education_regex = r'(?<=<span class="ProfileHeader-name">).{0,30}(?=</span>)'
# user_education_pattern = re.compile(user_education_regex)
#
# user_profile_regex = r'(?<=<span class="ProfileHeader-name">).{0,30}(?=</span>)'
# user_profile_pattern = re.compile(user_profile_regex)


def get_user_info(user_data_dict, user_following_page):
    # Get user information.
    user_info = dict()
    try:
        user_info['id'] = user_data_dict['id']
        user_info['url_token'] = user_data_dict['url_token']
        user_info['name'] = user_data_dict['name']
        user_info['headline'] = user_data_dict['headline']
        user_info['avatar_url'] = user_data_dict['avatar_url']
    except:
        return dict()

    # Get user name.
    # try:
    #     user_info['name'] = user_name_parttern.findall(user_following_page)[0]
    # except:
    #     user_info['name'] = ''

    # try:
    #     user_info['headline'] = user_headline_pattern.findall(user_following_page)[0]
    # except:
    #     user_info['headline'] = ''

    # try:
    #     user_info['location'] = user_location_pattern.findall(user_following_page)[0]
    # except:
    #     user_info['location'] = ''

    # try:
    #     user_info['occupation'] = user_occupation_pattern.findall(user_following_page)[0]
    # except:
    #     user_info['occupation'] = ''
    #
    # try:
    #     user_info['education'] = user_education_pattern.findall(user_following_page)[0]
    # except:
    #     user_info['education'] = ''
    #
    # try:
    #     user_info['profile'] = user_profile_pattern.findall(user_following_page)[0]
    # except:
    #     user_info['profile'] = ''

    # print(user_following_page)
    soup = BeautifulSoup(user_following_page)
    print(soup.prettify())
    return user_info


if __name__ == '__main__':
    session = requests.session()
    session = login.load_cookie(session)
    if login.is_login(session):
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


