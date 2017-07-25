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
import time
import os.path
try:
    from cookielib import LWPCookieJar
except:
    from http.cookiejar import LWPCookieJar


def load_cookie(session):
    """Load cookie from file.

    Parameters:
        session - a requests lib session

    Returns:
        bool - cookie has successfully loaded or not
    """
    session.cookies = LWPCookieJar(filename='cookies')
    try:
        session.cookies.load(ignore_discard=True)
    except:
        return session
    return session


def save_cookie(session):
    """Save cookie to file.
    """
    session.cookies.save()
    return session


def isLogin(session):
    """Confirm you've logged in or not by checking the user's information page.

    Parameters:
        session - a requests lib session

    Returns:
        bool - you have logged in or not.
    """
    url = "https://www.zhihu.com/settings/profile"
    response = session.get(url, headers=headers, allow_redirects=False)
    login_code = response.status_code
    if login_code == 200:
        return True
    return False


def get_xsrf(session):
    """Get dynamic _xsrf code from zhihu.com

    Parameters:
        session - a requests lib session

    Returns:
        string - _xsrf code
    """
    # 获取登录时需要用到的_xsrf
    index_page = session.get('https://www.zhihu.com', headers=headers)
    pattern = r'name="_xsrf" value="(.*?)"'
    # 这里的_xsrf 返回的是一个list
    _xsrf = re.findall(pattern, index_page.text)
    return _xsrf[0]


def get_captcha(session):
    """Get captcha image from log in page.

    Parameters:
        session - a requests lib session

    Returns:
        string - captcha image file path
    """
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    
    return os.path.abspath('captcha.jpg')


headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/59.0.3071.115 Safari/537.36"
}


def login(session):
    """Log in.

    Parameters:
        session - a requests lib session

    Returns:
        None
    """

    # # Have logged in or not.
    # if isLogin(session):
    #     print("You have already logged in.")
    #     return

    # Get _xsrf code.
    _xsrf = get_xsrf(session)
    headers["X-Xsrftoken"] = _xsrf
    headers["X-Requested-With"] = "XMLHttpRequest"

    while True:
        # Input account and password.
        account = input("Input your account(Email of phone number):\n>  ")
        password = input("Input your password:\n>  ")

        # Infer that the account is a phone number or an email.
        if re.match(r"^1\d{10}$", account):
            print("Log in with phone number.\n")
            post_url = 'https://www.zhihu.com/login/phone_num'
            postdata = {
                '_xsrf': _xsrf,
                'password': password,
                'phone_num': account
            }
        else:
            if "@" in account:
                print("Log in with email.\n")
            else:
                print("Account error, please log in again.")
                continue
            post_url = 'https://www.zhihu.com/login/email'
            postdata = {
                '_xsrf': _xsrf,
                'password': password,
                'email': account
            }
        break

    # Try to log in without captcha code.
    login_response = session.post(post_url, data=postdata, headers=headers)

    # If the logon fails, log in again with captcha code.
    login_code = login_response.json()
    if login_code['r'] == 1:
        # 不输入验证码登录失败
        # 使用需要输入验证码的方式登录
        captcha_filepath = get_captcha(session)
        print("Find the captcha.jpg in directory \"%s\" and input captcha code." % captcha_filepath)
        postdata["captcha"] = input("please input the captcha\n>")
        login_page = session.post(post_url, data=postdata, headers=headers)
        login_code = login_page.json()
        print(login_code['msg'])

    # Save cookie.
    save_cookie(session)
    return session


# if __name__ == '__main__':
#     session = requests.session()
#     load_cookie(session)
#     if isLogin(session):
#         print("logged in.")
#     else:
#         login(session)
