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


class CrawlSession(ZhihuSession):
    def __init__(self):
        ZhihuSession.__init__(self)
        self.__currenttoken = ''
        self.__currentjson = {}

    def __getpagejson(self, urltoken):
        user_following_url = "https://www.zhihu.com/people/" + urltoken + "/following"
        response = self.get(user_following_url, headers=headers)

        if response.status_code == 200:
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
                pagejson_text = soup.body.contents[1].attrs['data-state']
                pagejson = json.loads(pagejson_text)
            except:
                pagejson = dict()
        else:
            pagejson = dict()
        self.__currenttoken = urltoken
        self.__currentjson = pagejson
        return pagejson

    def getfollowinglist(self, urltoken):
        if urltoken != self.__currenttoken:
            self.__getpagejson(urltoken)

        try:
            followinglist = self.__currentjson['people']['followingByUser'][urltoken]['ids']
            tempset = set(followinglist)
            tempset.remove(None)
            followinglist = list(tempset)
        except:
            followinglist = list()

        return followinglist

    def getinfo(self, urltoken):
        if urltoken != self.__currenttoken:
            self.__getpagejson(urltoken)

        try:
            infojson = self.__currentjson['entities']['users'][urltoken]
            info = {'user_url_token': urltoken, 'user_data_json': json.dumps(infojson)}
        except:
            info = {'user_url_token': urltoken, 'user_data_json': ''}
        return info


# if __name__ == '__main__':
#     session = CrawlSession()
#
#     urltoken = "moranzcw"
#     followinglist = session.getfollowinglist(urltoken)
#     info = session.getinfo(urltoken)
#
#     print(followinglist)
#     print(info)

