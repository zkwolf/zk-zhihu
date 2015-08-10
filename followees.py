import sqlite3
import win32crypt
import os
import requests
import re
from bs4 import BeautifulSoup
import json
import time
import copy


zhihu_url = "http://www.zhihu.com"
zhihu_login_url = zhihu_url + "/login/email"
captcha_url = zhihu_url + "/captcha.gif?r=" + str(int(time.time()))
data_sum = set()
data_temp = set()
data_next = set()


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

def get_followees(url):
    '''
        获取关注界面，得到关注人数，确定offset的值
    '''
    global data_temp
    if not os.path.exists('cookies'):
        get_chrome_cookies()
    with open('cookies', 'r') as f:
        cookie = eval(f.read())
    s = requests.Session()
    s.cookies.update(cookie)
    r = s.get(url)
    data = r.text
    raw_hash_id = re.findall('hash_id(.*)', data)
    hash_id = raw_hash_id[0][14:46]
    raw_xsrf = re.findall('xsrf(.*)', data)
    _xsrf = raw_xsrf[0][9:-3]
    soup = BeautifulSoup(data, 'html.parser')
    people = soup.select("div.zu-main-sidebar strong")
    num = int(people[0].get_text())
    for followee in soup.select('h2.zm-list-content-title a'):
        data_temp.add(followee.attrs.get('href'))
    '''
        获取所有除第一页以外的所有关注
    '''
    if num > 20:
        offsets = []
        divi = num // 20
        header = {
            'Host': 'www.zhihu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
            'Referer': 'http://www.zhihu.com',
            'X-Requested-With': 'XMLHttpRequest',
        }
        for i in range(divi):
            offsets.append(20 * (i + 1))
        offsets.append(num)
        for index in range(divi + 1):
            offset = offsets[index]
            print(offset)
            params = json.dumps(
                {"offset": offset, "order_by": "created", "hash_id": hash_id})
            payload = {'method': 'next', 'params': params, '_xsrf': _xsrf}
            request_url = "http://www.zhihu.com/node/ProfileFolloweesListV2"
            x = s.post(request_url, data=payload, headers=header)
            temp = json.loads(x.text)
            _followee2 = temp.get('msg')
            followee2 = ''.join(_followee2)
            soup = BeautifulSoup(followee2, 'html.parser')
            for followee in soup.select('h2.zm-list-content-title a'):
                data_temp.add(followee.attrs.get('href'))
        time.sleep(0.5)


def loop(depth):
    global data_sum
    global data_next
    global data_temp
    for i in range(depth):
        if i == 0:
            url = "http://www.zhihu.com/people/zkwolf10824/followees"
            data_sum.add(url)
            get_followees(url)
            data_sum, data_temp = data_sum.union(data_temp), data_temp.difference(data_sum)
            data_next = copy.deepcopy(data_temp)
            data_temp.clear()
        else:
            print('data_next:' + str(len(data_next)))
            for url in data_next:
                print(url)
                get_followees(url + '/followees')
                time.sleep(2)
            data_sum, data_temp = data_sum.union(data_temp), data_temp.difference(data_sum)
            data_next = copy.deepcopy(data_temp)
            data_temp.clear()

if __name__ == "__main__":
    depth = int(input('请输入深度\n'))
    loop(depth)
    with open('followees.txt', 'w') as f:
        for i in data_sum:
            f.write(i + '\n')
