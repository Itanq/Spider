#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

filename = './qiushibaike.html'
f = open(filename, 'r')
Str = f.read()

pattern = re.compile('<div.*?author.*?>.*?<a.*?title="(.*?)">.*?'+'<div.*?>(.*?)</div>.*?', re.S)

m = re.findall(pattern, Str)

for item in m:
    print item[0], item[1]
