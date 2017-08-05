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
import proxy

headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    #               "AppleWebKit/537.36 (KHTML, like Gecko) "
    #               "Chrome/59.0.3071.115 Safari/537.36"
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063"
}


class CrawlSession(requests.Session):
    def __init__(self):
        requests.Session.__init__(self)

    def __getpagejson(self, urltoken):
        user_following_url = "https://www.zhihu.com/people/" + urltoken + "/following"
        try:
            response = self.get(user_following_url, headers=headers, proxies=proxy.proxies)
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
        pagejson = self.__getpagejson(urltoken)
        # 提取该用户的关注用户列表
        try:
            followinglist = pagejson['people']['followingByUser'][urltoken]['ids']
            tempset = set(followinglist)
            tempset.remove(None)
            followinglist = list(tempset)
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


# if __name__ == '__main__':
#     session = CrawlSession()
#
#     urltoken = "moranzcw"
#     followinglist = session.getfollowinglist(urltoken)
#     info = session.getinfo(urltoken)
#
#     print(followinglist)
#     print(info)

