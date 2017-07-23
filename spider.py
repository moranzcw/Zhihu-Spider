import requests
import re
import json
from threading import Thread
from queue import Queue

urlQueue = Queue()
infoQueue = Queue()

f = open(r'test.txt', 'r')  # 打开所保存的cookies内容文件
cookies = {}  # 初始化cookies字典变量
for line in f.read().split(';'):  # 按照字符：进行划分读取
    # 其设置为1就会把字符串拆分成2份
    name, value = line.strip().split('=', 1)
    cookies[name] = value  # 为字典cookies添加内容

headers = {
    "Host": "www.zhihu.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/58.0.3029.110 \
    Safari/537.36"
}
user_id_regex = r'(?<=api/v4/people/).{32}'
user_id_pattern = re.compile(user_id_regex)
user_url_token_regex = r'(?<="url_token": ").{32}'


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


def get_info(user_id):
    response = requests.get("https://www.zhihu.com/api/v4/members/" + user_id, headers=headers, cookies=cookies)
    # if response.status_code == 200:
    print(response.status_code)
    print(response.text)
    if response.status_code == 200:
        user_url_token_list = user_id_pattern.findall(response.text)
    else:
        user_url_token_list = []
    # print (r.text)
    return user_url_token_list


class Worker(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # url = urlQueue.get()
        # info = ()
        # infoQueue.put(info)
        pass


class Master(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # url = ''
        # urlQueue.put(url)
        # infoQueue.get()
        pass


if __name__ == '__main__':
    # print(headers)
    resp = get_info("9ffd5c016aabeafd1030e63fe410beb8")
    print(resp)
