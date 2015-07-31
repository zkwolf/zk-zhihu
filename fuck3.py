import sqlite3
import win32crypt
import os
import requests
import re
from bs4 import BeautifulSoup
import json

zhihu_url = "http://www.zhihu.com"
zhihu_login_url = zhihu_url + "/login/email"

bitch = []

def get_chrome_cookies(url):
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
    return ret_dict

def get_followees(cookie):
    '''
        获取关注界面，得到关注人数，确定offset的值
        x = requests.get(zhihu_login_url, cookies=get_chrome_cookies(".zhihu.com"))

    '''
    r = requests.get('http://www.zhihu.com/people/zkwolf10824/followees', cookies=cookie)
    with open('followees.html', 'wb') as f:
        data = r.text
        raw_hash_id = re.findall('hash_id(.*)', data)
        hash_id = raw_hash_id[0][14:46]
        raw_xsrf = re.findall('xsrf(.*)', data)
        _xsrf = raw_xsrf[0][9:-3]
        f.write(r.text.encode('utf-8'))

    try:
        followees = open('followees.html', 'rb')
        soup = BeautifulSoup(followees, 'html.parser')
        people = soup.select("div.zu-main-sidebar strong")
        num = int(people[0].get_text())
        print('folowee' + str(num))
        for followee in soup.select('h2.zm-list-content-title a'):
            bitch.append(followee.attrs.get('href'))
    finally:
        if followees:
            followees.close()


    '''
        获取所有除第一页以外的所有关注
    '''
    # offsets = []
    # divi = num//20
    # for i in range(divi):
    #     offsets.append(20*(i+1))
    # offsets.append(num)
    # for index in range(divi+1):
    #     offset = offsets[index] 
    #     header = { 
    #         'Host': 'www.zhihu.com',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
    #         'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    #         'Referer': 'http://www.zhihu.com/people/chen-hao-12-95/followees',
    #         'Connection': 'keep-alive',
    #         'Origin': 'http://www.zhihu.com',
    #         'X-Requested-With': 'XMLHttpRequest',
    #     }
    #     params = json.dumps({"offset":offset, "order_by":"created", "hash_id":hash_id,})
    #     payload = {"method":"next", "params":params, "_xsrf":_xsrf,}
    #     request_url = "http://www.zhihu.com/node/ProfileFolloweesListV2"
    #     x = requests.post(request_url, data=payload, headers=header, cookies=cookie)
    #     print(x.text)
        # temp = json.loads(x.text)
        # _followee2 = temp.get('msg')
        # followee2 = ''.join(_followee2)

        # with open('followees' + str(offset) + '.html', 'wb') as f:
        #     f.write(followee2.encode('utf-8'))
        # try:
        #     followees = open('followees' + str(offset) + '.html', 'rb')
        #     soup = BeautifulSoup(followees, 'html.parser')
        #     for followee in soup.select('h2.zm-list-content-title a'):
        #         bitch.append(followee.attrs.get('href'))
        # finally:
        #     if followees:
        #         followees.close()
    '''
        写入txt文件，用来后续分析
    '''
    with open('followees.txt', 'w') as f:
        for i in range(len(bitch)):
            f.write(bitch[i]+'\n')

if __name__ == "__main__":
    cookie = get_chrome_cookies('.zhihu.com')
    get_followees(cookie)
