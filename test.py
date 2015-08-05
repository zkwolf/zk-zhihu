#-*- encoding:utf-8 -*-
import os
import sqlite3
import win32crypt
import json


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

get_chrome_cookies()
with open('cookies', 'r') as f:
    print(type(eval(f.read())))
