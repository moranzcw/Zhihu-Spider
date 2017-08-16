#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description
- 获取指定知乎用户的主页，并提取出个人信息。
- 类Crawl为单例模式，在程序中只有一个实例。
- 线程安全。
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
import proxy

__author__ = """\
  /\/\   ___  _ __ __ _ _ __  
 /    \ / _ \| '__/ _` | '_ \ 
/ /\/\ \ (_) | | | (_| | | | |
\/    \/\___/|_|  \__,_|_| |_|"""

# User Agent
UA = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36"

# HTTP 请求头
headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    "User-Agent": UA
}


class Singleton(object):
    """
    实现单例模式，Crawl在程序中只有一个实例

    Attributes:
        _instance: 唯一实例的引用。
    """
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance


class Crawl(Singleton):
    """
    获取指定知乎用户主页，并提取出个人信息。

    Attributes:
        None.
    """
    def __init__(self):
        pass

    def __getpagejson(self, urltoken):
        """
        获取指定知乎用户的主页，并提取出存储个人信息的json。

        Args:
            urltoken: 用户主页url地址中包含的token，具有唯一性。

        Returns:
            pagejson: 一个从用户信息json加载的dict

        Raises:
            None.
        """
        user_following_url = "https://www.zhihu.com/people/" + urltoken + "/following"
        try:
            response = requests.get(user_following_url, headers=headers, proxies=proxy.getproxies())
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                pagejson_text = soup.body.contents[1].attrs['data-state']
                pagejson = json.loads(pagejson_text)
            else:
                pagejson = dict()
        except:
            pagejson = dict()

        return pagejson

    def getinfo(self, urltoken):
        """
        调用__getpagejson函数，获取个人信息json，从中提取出该用户信息和关注用户的列表

        Args:
            urltoken: 用户主页url地址中包含的token，具有唯一性。

        Returns:
            dict: 一个包含用户信息json字符串和关注用户列表的dict

        Raises:
            None.
        """
        pagejson = self.__getpagejson(urltoken)
        # 提取该用户的关注用户列表
        try:
            followinglist = pagejson['people']['followingByUser'][urltoken]['ids']
            # 去出重复元素
            tempset = set(followinglist)
            tempset.remove(None)
            followinglist = list(tempset)
            # 转换为json字符串
            followinglist = json.dumps({'ids': followinglist})
        except:
            followinglist = json.dumps({'ids': list()})

        # 提取该用户的信息，并转换为字符串
        try:
            infojson = json.dumps(pagejson['entities']['users'][urltoken])
        except:
            infojson = ''

        info = {'user_url_token': urltoken,
                'user_data_json': infojson,
                'user_following_list': followinglist
                }
        return info


if __name__ == '__main__':
    pass


