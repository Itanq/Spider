#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import re


class qiushibake:
    '''
        抓取糗事百科的类
    '''
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
        self.headers = {'User-Agent':self.user_agent}
        self.stories = []
        self.enable = False

    # 获取指定页面的html源码
    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex) 
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pagecode = response.read().decode('utf-8')
            return pagecode
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print u"连接糗事百科失败,错误原因",e.reason
                return None

    # 获取指定页面的所有段子的列表
    def getPageItems(self, pageIndex):
        pagecode = self.getPage(pageIndex)
        if not pagecode:
            print u"页面加载失败..."
            return None
        # 依次获取 作者 内容 点赞数 评论数
        pattern = re.compile('<div.*?author.*?>.*?<a.*?title="(.*?)">.*?'+'<div.*?>(.*?)</div>.*?'+'<span.*?><i.*?>(.*?)</i>.*?'+'<span.*?>.*?<i.*?>(.*?)</i>', re.S)
        List_items = re.findall(pattern, pagecode)
        pageStories = []
        for item in List_items:
            replaceBR = re.compile(r'<br/>')
            # 用换行替换<br/>标签
            text = re.sub(replaceBR, "\n", item[1])
            pageStories.append([item[0].strip(), text.strip(), item[2].strip(), item[3].strip()])
        return pageStories

    # 加载并提取页面的内容并加入到stories中
    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    # 按一个键显示一个段子
    def getOneStory(self, pageStories, page):
        for story in pageStories:
            inp = raw_input()
            self.loadPage()
            if inp == 'Q' or inp == 'q':
                self.enable = False
            print u"第%d页\t发布人:%s\t内容:%s\t点赞:%s\t评论:%s\t" % (page, story[0], story[1], story[2], story[3])

    def start(self):
        print u"正在读书糗事百科,按回车键查看新段子,q/Q退出"
        self.enable = True
        nowPage = 0
        self.loadPage()
        while self.enable:
            if len(self.stories)>0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories, nowPage)


spider = qiushibake()
spider.start()

