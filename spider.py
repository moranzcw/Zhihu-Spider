import requests
import re

headers = {
    "Host":"www.zhihu.com",
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
r = requests.get("https://www.zhihu.com/people/moranzcw/following", headers = headers)

print(r.status_code)
print(r.headers)
print(r.encoding)
print(r.text)