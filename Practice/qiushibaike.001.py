#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import cookielib
import re

'''

根据你输入的页数来抓取糗事百科的段子,显示段子的作者和内容

'''
page = input("please input a number: ")
url = "http://www.qiushibaike.com/hot/page/" + str(page)
user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
headers = {'User-Agent':user_agent}

try:
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    content = response.read()
    pattern  = re.compile('<div.*?author.*?>.*?<a.*?title="(.*?)">.*?'+'<div.*?>(.*?)</div>.*?', re.S)
    items = re.findall(pattern, content)
    for item in items:
        print "Author: ", item[0], "\n", "Content: ", item[1]
except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hashattr(e,"reason"):
        print e.reason
