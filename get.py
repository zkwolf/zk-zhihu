#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import sqlite3
import win32crypt
import os
import json
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
    cmd = 'copy \"' + \
        os.getenv('LOCALAPPDATA') + '\\Google\\Chrome\\User Data\\Default\\Cookies' + \
        '\" D:\\python-chrome-cookies'
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


def judge(args):
    if args:
        args = args[0]
    else:
        args = None
    return args


def get_content():
    header = {
        'Host': 'www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
        'Referer': 'http://www.zhihu.com',
    }
    if not os.path.exists('cookies'):
        get_chrome_cookies()
    with open('cookies', 'r') as f:
        cookie = eval(f.read())
    s = requests.Session()
    s.cookies.update(cookie)
    i = 0
    for url in url_queue:
        try:
            conn = s.get(url, headers=header, timeout=2)
        except Exception as err:
            print(err)
        data = conn.text
        i += 1
        name = re.findall('<span class="name">(.*?)</span>', data)[1]
        location = judge(
            re.findall('<span class="location item" title="(.*?)">', data))
        business = judge(
            re.findall('<span class="business item" title="(.*?)">', data))
        employment = judge(
            re.findall('<span class="employment item" title="(.*?)">', data))
        position = judge(
            re.findall('<span class="position item" title="(.*?)">', data))
        education = judge(
            re.findall('<span class="education item" title="(.*?)">', data))
        education_extra = judge(
            re.findall('''<span class="education-extra item" title='(.*?)'>''', data))
        sex = judge(re.findall(
            '<span class="item gender" ><i class="icon icon-profile-(.*?)"></i></span>', data))
        question, answer = re.findall(
            '<span class="num">(.*?)</span>', data)[:2]
        agree, thanks = re.findall('<strong>(.*?)</strong>', data)[:2]
        followees, followers = re.findall(
            '<strong>(.*?)</strong>', data)[-5:-3]
        print(i, url, name, location, business, employment, position, education,
              education_extra, sex, question, answer, agree, thanks, followees, followers)


if __name__ == "__main__":
    get_queue()
    get_content()
