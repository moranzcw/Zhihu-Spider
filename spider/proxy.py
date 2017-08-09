#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description
- 获取IP代理。
Info
- author : "moran"
- github : "moranzcw@gmail.com"
- date   : "2017.7.29"
"""
__author__ = """\
  /\/\   ___  _ __ __ _ _ __  
 /    \ / _ \| '__/ _` | '_ \ 
/ /\/\ \ (_) | | | (_| | | | |
\/    \/\___/|_|  \__,_|_| |_|"""

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = ""
proxyPass = ""

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}

def getproxies():
    return proxies
