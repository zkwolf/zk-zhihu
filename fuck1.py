#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zkwolf'

import requests
import gzip
from bs4 import BeautifulSoup
import json
import re

s = requests.session()
login_data = {'email': 'chenhao5866@gmail.com', 'password': 'hacker97976442'}
s.post('http://www.zhihu.com/login', login_data)

r = s.get('http://www.zhihu.com/people/chen-hao-12-95/followees')
with open('followees.html', 'wb') as f:
	data = r.text
	raw_hash_id = re.findall('hash_id(.*)', data)
	hash_id = raw_hash_id[0][14:46]
	raw_xsrf = re.findall('xsrf(.*)', data)
	_xsrf = raw_xsrf[0][9:-3]
	f.write(r.text.encode('utf-8'))

try:
	followees = open('followees.html', 'rb')
	soup = BeautifulSoup(followees)
	people = soup.select("div.zu-main-sidebar strong")
	global num 
	num = int(people[0].get_text())

	for followee in soup.select('h2.zm-list-content-title a'):
		print(followee.attrs.get('href'), followee.attrs.get('title'))
finally:
	if followees:
		followees.close()

offsets = []
divi = num//20
for i in range(divi):
	offsets.append(20*(i+1))
offsets.append(num)
for index in range(divi+1):
	offset = offsets[index] 
	header = { 
		'Host': 'www.zhihu.com',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
		'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
		'Referer': 'http://www.zhihu.com/people/chen-hao-12-95/followees',
		'Connection': 'keep-alive',
		'Origin': 'http://www.zhihu.com',
	}
	params = json.dumps({"offset":offset, "order_by":"created", "hash_id":hash_id,})
	payload = {"method":"next", "params":params, "_xsrf":_xsrf,}
	request_url = "http://www.zhihu.com/node/ProfileFolloweesListV2"
	x = s.post(request_url, data=payload, headers=header)
	temp = json.loads(x.text)
	_followee2 = temp.get('msg')
	followee2 = ''.join(_followee2)



	with open('followees' + str(offset) + '.html', 'wb') as f:
		f.write(followee2.encode('utf-8'))
	try:
		followees = open('followees' + str(offset) + '.html', 'rb')
		soup = BeautifulSoup(followees)
		for followee in soup.select('h2.zm-list-content-title a'):
			print(followee.attrs.get('href'), followee.attrs.get('title'))
	finally:
		if followees:
			followees.close()