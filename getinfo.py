# !/usr/bin/env python
# coding:utf-8
import os
import requests
from bs4 import BeautifulSoup


class GetInfo():

    def __init__(self):
        self.url_queue = []
        self.requests = requests.Session()

    def get_queue(self):
        if os.path.exists('followees.txt'):
            with open('followees.txt', 'r') as f:
                for line in f.readlines():
                    self.url_queue.append(line.strip('\n'))

    def judge(self, args):
        '''
        judge the args if agrs is null, if it is null return None else return x.get_text()
        '''
        if args:
            args = args.get_text()
        else:
            args = None
        return args

    def get_content(self):
        self.get_queue()
        header = {
            'Host': 'www.zhihu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
            'Referer': 'http://www.zhihu.com',
        }
        with open('cookies.json', 'r') as f:
            cookie = eval(f.read())
        s = self.requests
        s.cookies.update(cookie)
        i = 0
        for url in self.url_queue:
            try:
                conn = s.get(url, headers=header, timeout=5)
            except Exception as err:
                print(err)
            data = conn.text
            i += 1
            soup = BeautifulSoup(data, 'lxml')
            profile = soup.find('div', class_='zm-profile-header')
            name = self.judge(profile.find('span', class_='name'))
            location = self.judge(profile.find('span', class_='location item'))
            business = self.judge(profile.find('span', class_='business item'))
            employment = self.judge(profile.find('span', class_='employment item'))
            position = self.judge(profile.find('span', class_='position item'))
            education = self.judge(profile.find('span', class_='education item'))
            education_extra = self.judge(profile.find('span', class_='education-extra item'))
            # sex = self.judge(re.findall(
            #     '<span class="item gender" ><i class="icon icon-profile-(.*?)"></i></span>', data))
            # question, answer = re.findall(profile.
            #     '<span class="num">(.*?)</span>', data)[:2]
            # agree, thanks = re.findall('<strong>(.*?)</strong>', data)[:2]
            # followees, followers = re.findall(
            #     '<strong>(.*?)</strong>', data)[-5:-3]
            print(i, url, name, location, business, employment, position, education, education_extra)


if __name__ == "__main__":
    get_info = GetInfo()
    get_info.get_content()
