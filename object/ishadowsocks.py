#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import re

class shadowsocks():
    '''
        shadowsocks 类
        用于自动从ishadowsocks站点获取账号并自动更改本地的shadowsocks的配置文件
    '''
    def __init__(self):
        self.tag = False
        self.username = ''
        self.password = ''
        self.user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"
        self.headers = {'User-Agent':self.user_agent}

    def getHtml(self):
        try:
            url = 'http://www.ishadowsocks.net/'
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            return response.read()
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print u"连接失败,错误原因",e.reason
                return None

    def getData(self):
        html = self.getHtml()
        if not html:
            print u"页面加载失败..."
            return None
        pattern = re.compile(r'<div.*?-lg-4.*?>.*?<h4>.*?服务器地址:(.*?)</h4>.*?'+':(.*?)</h4>.*?'+':(.*?)</h4>.*?'+':(.*?)</h4>.*?', re.S)
        Items = re.findall(pattern, html)
        List = []
        for item in Items:
            List.append([item[0].strip(), item[1].strip(), item[2].strip(), item[3].strip()])
        return List
    
    def start(self):
        print u"自动获取ishadowsocks的免费账号."
        result = self.getData()
        for i in result:
            print "address:%s\tpost:%s\tpassword:%s\tpassway:%s\t" % (i[0], i[1], i[2], i[3])


item = shadowsocks()
item.start()

