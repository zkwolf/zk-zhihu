#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import sqlite3
import win32crypt
import os
import json
from bs4 import BeautifulSoup
import logging
import time
import re
import requests

logging.basicConfig(level=logging.INFO)
url_queue = []
w_url = []

def get_chrome_cookies():
    '''
        这里请先用chrome登陆知乎以获取coookie
    '''
    url = '.zhihu.com'
    cmd = 'copy \"' + os.getenv('LOCALAPPDATA') + '\\Google\\Chrome\\User Data\\Default\\Cookies' + '\" D:\\python-chrome-cookies'
    os.system(cmd)
    conn = sqlite3.connect("d:\\python-chrome-cookies")
    ret_list = []
    ret_dict = {}
    for row in conn.execute("select host_key, name, path, value, encrypted_value from cookies"):
        if row[0] != url:
            continue
        ret = win32crypt.CryptUnprotectData(row[4], None, None, None, 0)
        ret_list.append((row[1], ret[1]))
        ret_dict[row[1]] = ret[1].decode()
    conn.close()
    os.system('del "D:\\python-chrome-cookies"')
    with open('cookies', 'w') as f:
        f.write(str(ret_dict))

def get_queue():
    if os.path.exists('followees.txt'):
        logging.info('file exists')
        with open('followees.txt', 'r') as f:
            for line in f.readlines():
                url_queue.append(line.strip('\n'))

def get_content():
    header = {
            'Host': 'www.zhihu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
            'Referer': 'http://www.zhihu.com/people/zkwolf10824/followees',
    }
    if not os.path.exists('cookies'):
        get_chrome_cookies()
    with open('cookies', 'r') as f:
        cookie = eval(f.read())
    s = requests.Session()
    s.cookies.update(cookie)
    for url in url_queue:
        r = s.get(url, headers=header)
        soup = BeautifulSoup(r.text, 'html.parser')
        sex_i = soup.select('span.gender.item i')
        try:
           sex = re.search(r'class="icon icon-profile-(.*)"', str(sex_i)).group(1)
           if sex == 'female':
               w_url.append(url)
               print(url)
        except:
            print('error: %s' % (url))
        time.sleep(2)

if __name__ == "__main__":
    get_queue()
    get_content()
