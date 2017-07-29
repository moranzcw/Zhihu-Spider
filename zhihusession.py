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
import requests
import re
import time
import os.path

try:
    from cookielib import LWPCookieJar
except:
    from http.cookiejar import LWPCookieJar

headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/59.0.3071.115 Safari/537.36"
}

class ZhihuSession(requests.Session):
    def __init__(self):
        requests.Session.__init__(self)
        self.cookies = LWPCookieJar(filename='cookies')

        if self.__load_cookie() and self.__is_login():
            print("You have already logged in.")
        else:
            # Try to log in until you succeed.
            while not self.login():
                pass

    def __load_cookie(self):
        """Load cookie from file.

        Parameters:
            session - a requests lib session

        Returns:
            bool - cookie has successfully loaded or not
        """
        try:
            self.cookies.load(ignore_discard=True)
        except:
            return False
        return True

    def __save_cookie(self):
        """Save cookie to file.
        """
        try:
            self.cookies.save()
        except:
            return False
        return True

    def __is_login(self):
        """Confirm you've logged in or not by checking the user's information page.

        Parameters:
            session - a requests lib session

        Returns:
            bool - you have logged in or not.
        """
        url = "https://www.zhihu.com/settings/profile"
        response = self.get(url, headers=headers, allow_redirects=False)
        login_code = response.status_code
        if login_code == 200:
            return True
        return False

    def __get_xsrf(self):
        """Get dynamic _xsrf code from zhihu.com

        Parameters:
            session - a requests lib session

        Returns:
            string - _xsrf code
        """
        index_page = self.get('https://www.zhihu.com', headers=headers)
        regex = r'name="_xsrf" value="(.*?)"'
        _xsrf = re.findall(regex, index_page.text)
        return _xsrf[0]

    def __get_captcha(self):
        """Get captcha image from log in page.

        Parameters:
            session - a requests lib session

        Returns:
            string - captcha image file path
        """
        t = str(int(time.time() * 1000))
        captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
        r = self.get(captcha_url, headers=headers)
        with open('captcha.jpg', 'wb') as f:
            f.write(r.content)
            f.close()
        return os.path.abspath('captcha.jpg')

    def login(self):
        """Log in.

        Parameters:
            session - a requests lib session

        Returns:
            session - a requests lib session
        """
        # Get _xsrf code.
        _xsrf = self.__get_xsrf()
        headers["X-Xsrftoken"] = _xsrf
        headers["X-Requested-With"] = "XMLHttpRequest"

        # Input account and password.
        account = input("Input your account(Email of phone number):\n>  ")
        password = input("Input your password:\n>  ")

        postdata = {
            '_xsrf': _xsrf,
            'password': password
        }
        # Infer that the account is a phone number or an email.
        if re.match(r"^1\d{10}$", account):
            # Log in with phone number.
            post_url = 'https://www.zhihu.com/login/phone_num'
            postdata['phone_num'] = account
        else:
            if "@" in account:
                # Log in with email.
                post_url = 'https://www.zhihu.com/login/email'
                postdata['email'] = account
            else:
                print("Account error, please log in again.")
                return False

        # Get Captcha.
        captcha_filepath = self.__get_captcha()
        print("Find the captcha.jpg in directory \"%s\" and input captcha code." % captcha_filepath)
        postdata["captcha"] = input("please input the captcha\n>")

        # Log in.
        login_response = self.__post(post_url, data=postdata, headers=headers)
        login_code = login_response.json()
        print(login_code['msg'])
        if not login_code['r'] == 0:
            return False

        # Save cookie.
        self.__save_cookie()
        return True

if __name__ == '__main__':
    session = ZhihuSession()
