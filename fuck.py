#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'chenhao'

import requests
import gzip

s = requests.session()
login_data = {'email': 'chenhao5866@gmail.com', 'password': '***********'}
s.post('http://www.zhihu.com/login', login_data)

r = s.get('http://www.zhihu.com')
with open('x.txt', 'wb') as f:
	f.write(r.text.encode('utf-8'))