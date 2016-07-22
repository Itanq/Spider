#!/usr/bin/python
# -*- coding: utf-8 -*-

# bug: __author__ = 'zmant'

import urllib
import urllib2
import re


class Tool():
    '''
        处理页面标签
    '''
    # 去除img标签,7位空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 删除超链接
    removeAddr = re.compile('<a.*?>|</a>')
    # 去除额外的标签
    removeExtraTag = re.compile('<.*?>')
    # 把换行的标签换为 \n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 把制表格<td>替换为\t
    replaceTD = re.compile('<td>')
    # 将段落开头替换为\n+tab
    replacePara = re.compile('<p.*?>')
    # 将换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    
    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        return x.strip()


class baidutieba():
    '''
        百度贴吧爬虫类
    '''
    def __init__(self, baseURL, seeLz, floortag):
        self.baseURL = baseURL
        # 是否只看楼主
        self.seeLz = '?see_lz='+str(seeLz)
        # header setring
        self.user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
        self.headers = {'User-Agent':self.user_agent}
        # HTML标签剔除工具类对象
        self.tool = Tool()
        # 全局file变量,文件写入操作对象
        self.file = None
        # 楼层标号
        self.floor = 1
        # 默认标题,若没有成功获取标题时使用
        self.defaulttitle = u"百度贴吧"
        # 楼层分割符
        self.floorTag = floortag

    # 获取 pageIndex页帖子的代码
    def getHtml(self, pageIndex):
        try:
            url = self.baseURL + self.seeLz + '&pn' + str(pageIndex)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read()
        except urllib2.URLErroe, e:
            if hasattr(e, "reason"):
                print u"连接百度贴吧失败,错误原因: " , e.reason
            return None

    # 获取帖子标题
    def getTitle(self, pageIndex=1):
        pagehtml = self.getHtml(pageIndex)
        if not pagehtml:
            print u"加载失败..."
            return None
        pattern = re.compile('<h3 class="core_title_txt pull-left text-overflow.*?title="(.*?)"',re.S)
        title = re.search(pattern, pagehtml)
        if title:
            return title.group(1).strip()
        else:
            return None
    
    # 获取帖子页数
    def getPageNum(self):
        page = self.getHtml(1)
        if not page:
            print u"加载失败..."
            return None
        pattern = re.compile('<li class="l_reply_num" style="margin-left:8px" ><span.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        ans = re.search(pattern, page)
        if ans:
            return ans.group(1).strip()
        else:
            return None

    # 获取page页的每个楼层的内容
    def getContent(self, page):
        pattern = re.compile('<div id="post_content.*?>(.*?)</div>', re.S)
        contents = re.findall(pattern, page)
        List_content = []
        for item in contents:
            content = "\n" + self.tool.replace(item) + "\n"
            List_content.append(content)
        return List_content

    def creatFile(self, title):
        if title is not None:
            self.file = open(title + ".txt", "w+")
        else:
            self.file = open(self.defaulttitle + ".txt", "w+")

    def writeData(self, contents):
        for item in contents:
            if self.floorTag == '1':
                floorLine = "\n" + str(self.floor) + u"-------------------------------------------------------\n"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1

    # Start
    def start(self):
        title = self.getTitle()
        pageNum = self.getPageNum()
        self.creatFile(title)
        if pageNum == None:
            print u"URL已失效,请重试"
            return
        try:
            print u"该帖子共有"+str(pageNum)+u"页"
            for count in range(1, int(pageNum)+1):
                print u"正在写入第" + str(count) + u"页数据"
                pageHtml = self.getHtml(count)
                contents = self.getContent(pageHtml)
                self.writeData(contents)
        except IOError, e:
            print u"写入异常,原因" + e.message
        finally:
            print u"写入完成"


print u"请输入帖子代号: "
baseURL = 'http://tieba.baidu.com/p/' + str(raw_input(u"http://tieba.baidu.com/p/"))
seeLZ = raw_input("是否只看楼主,是输入1,否输入0\n")
floorTag = raw_input("是否写入楼层信息,是输入1,否输入0\n")

bdtb = baidutieba(baseURL, seeLZ, floorTag)
bdtb.start()

