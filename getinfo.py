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
        judge the args if agrs is null, if null return None else return x.get_text()
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
        index = 0
        for url in self.url_queue:
            conn = s.get(url, headers=header, timeout=5)
            data = conn.text
            index += 1
            soup = BeautifulSoup(data, 'lxml')
            profile = soup.find('div', class_='zm-profile-header')
            sidebar = soup.find('div', class_='zu-main-sidebar')
            name = self.judge(profile.find('span', class_='name'))
            location = self.judge(profile.find('span', class_='location item'))
            business = self.judge(profile.find('span', class_='business item'))
            employment = self.judge(profile.find('span', class_='employment item'))
            position = self.judge(profile.find('span', class_='position item'))
            education = self.judge(profile.find('span', class_='education item'))
            education_extra = self.judge(profile.find('span', class_='education-extra item'))
            _sex = profile.find('span', class_='item gender')
            if _sex:
                sex = _sex.find('i')['class'][1][13:]
            else:
                sex = None
            question, answer, post, *x = profile.find('div', class_='profile-navbar clearfix').find_all('span', class_='num')
            agree, thanks = profile.find('div', class_='zm-profile-header-info-list').find_all('strong')
            followees, followers = sidebar.find('div', class_='zm-profile-side-following zg-clear').find_all('strong')
            print(index, url, name, sex, location, business, employment, position, education, education_extra, followees.get_text(), followers.get_text(), question.get_text(), answer.get_text(), post.get_text(), agree.get_text(), thanks.get_text())


if __name__ == "__main__":
    get_info = GetInfo()
    get_info.get_content()
