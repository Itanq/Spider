#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib, urllib2
import re, os, tool

class doubanmovie():
    def __init__(self, URL):
        self.URL = "http://movie.douban.com/nowplaying/" + str(URL) + '/'
        self.user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
        self.headers = {'User-Agent':self.user_agent}

    def getPage(self):
        try:
            print 'url: ',self.URL
            request = urllib2.Request(self.URL)
            response = urllib2.urlopen(request)
            return response.read()
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接豆瓣电影失败。错误原因：",e.reason
            return None

    def getMoveList(self, page):
        if not page:
            print u"加载失败..."
            return None
        else:
            # 电影名称 评分 时长 国家 导演 演员
            pattern = re.compile('<li.*?data-title="(.*?)".*?'+'data-score="(.*?)".*?'+'duration="(.*?)".*?'+'region="(.*?)".*?'+'director="(.*?)".*?'+'actors="(.*?)".*?>', re.S)
            contents = re.findall(pattern, page)
            List = []
            for item in contents:
                List.append([item[0].strip(),item[1].strip(),item[2].strip(),item[3].strip(),item[4].strip(),item[5].strip()])
            return List


def main():
    local = raw_input('请输入你所在的城市来查询热映电影(城市用汉语拼音): ')
    spider_movie = doubanmovie(local)
    print u"正在连接豆瓣电影..."
    page = spider_movie.getPage()
    print u"正在获取电影列表..."
    List = spider_movie.getMoveList(page)
    f = open('doubanmovie.txt', 'w')
    print u"正在保存文件..."
    count = 1
    for item in List:
        Line = u"\n----------------------- %s -------------------------------\n" % count
        count += 1
        f.write(Line)
        data =  '电影名称: '+item[0]+'\n'+'评分: '+item[1]+'\n'+'时长: '+item[2]+'\n'+'国家: '+item[3]+'\n'+'导演: '+item[4]+'\n'+'演员: '+item[5]+'\n'
        f.write(data)
    f.close()
    print u"成功爬取",local,"市的热映电影,输出文件保存在当前文件夹的doubanmovie.txt中"


if __name__ == '__main__':
    main()
