#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import re, os
import tool

'''
    bug: 无法匹配到需要的内容
'''

class taobao():
    def __init__(self, baseURL):
        self.baseURL = baseURL
        self.user_agent = ''
        self.headers = {'Useg-Agent':self.user_agent}
        self.tool = tool.Tool()

    def getPageHtml(self, pageIndex):
        url = self.baseURL + "?page=" + str(pageIndex)
        request = urllib2.Request(url, headers=self.headers)
        response = urllib2.urlopen(request)
        return response.read().decode('gbk')

    def getContents(self, page):
        if not page:
            print u"加载失败..."
            return None
        #首页地址  名字 年龄  居住地              
        pattern = re.compile('<div class="list-item".*?<a href="(.*?)".*?'+'<a class="lady-name".*?>(.*?)</a>.*?'+'<strong>(.*?)</strong>.*?'+'<span>(.*?)</span>', re.S)
        contents = re.findall(pattern, page)
        return contents

    def getDetailPage(self, infoURL):
        response = urllib2.urlopen(infoURL)
        return response.read().decode('gbk')

    def getBrief(self, page):
        pattern = re.compile('<meta name="description" content="(.*?)"', re.S)
        ans = re.search(pattern, page)
        print "ans:  ",ans
        return self.tool.replace(ans.group(0))

    def getAllImagesURL(self, page):
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)</div>', re.S)
        contents = re.search(pattern, page)
        patternImg = re.compile('img.*?src="(.*?)"', re.S)
        images = re.findall(patternImg, contents.group(1))
        return images

    def saveImage(self, imageURL, fileName):
        u = urllib2.urlopen(imageURL)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        print u"正在保存她的一张图片为",fileName
        f.close


    def saveImages(self, imagesURL, name):
        number = 1
        print u"发现",name,u"共有",len(images),u"张图片"
        for imgURL in imagesURL:
            split = img.split('.')
            ftail = split.pop()
            if len(ftail) > 3:
                fail = 'jpg'
            filename = name + "/" +str(number) + "." + ftail
            self.saveImage(imgURL, filename)    
            number += 1 

    def saveIcon(self, iconULR, name):
        spilt = iconURL.split('.')
        ftail = split.pop()
        filanme = name + "/icon." + ftail
        self.saveImage(iconURL, filename)

    def saveBrief(self, contents, name):
        filename = name + "/" + name + ".txt"
        f = open(filename, "w+")
        print u"正在保存保存她的个人信息为",filename
        f.write(contents.encode('utf-8'))
        f.close()

    def mkdir(self, fileName):
        path = fileName.strip()
        isExists = os.path.exists(fileName)
        if not isExists:
            print u"创建文件夹",fileName
            os.mkdir(fileName)
            return True
        else:
            print u"文件夹",fileName,"已存在"
            return False

    def savePageInfo(self, pageIndex):
        pageHtml = self.getPageHtml(pageIndex)
        contents = self.getContents(pageHtml)
        #首页地址  名字 年龄  居住地              
        for item in contents:
            detailURL = "http:" + item[0]
            print u"发现一位模特,名字叫",item[1],u"芳龄",item[2],u",她在",item[3]
            print u"正在保存",item[1],"的信息"
            print u"她的个人地址是",detailURL
            # 获取item[1]的个人地址主页
            # 获取个人主页代码
            detailPage = self.getDetailPage(detailURL)
            # 从个人主页代码处获取个人简介
            brief = self.getBrief(detailPage)
            print u"brief code"
            # 从个人主页代码处获取图片列表
            images = self.getAllImagesURL(detailPage)
            # 创建item[1]文件夹
            self.mkdir(item[1])
            # 保存个人简介到item[1]文件夹内
            self.saveBrief(brief, item[1])
            # 保存个人头像到item[1]文件夹内
            self.saveIcon(item[0], item[1])
            # 保存图片到item[1]文件夹内
            self.saveImages(images, item[1])

    def start(self, s, e):
        for count in range(s, e+1):
            print u"正在寻找第",count,u"页的MM"
            self.savePageInfo(count)

if __name__ == '__main__':
    baseURL = 'https://mm.taobao.com/json/request_top_list.htm'
    spider = taobao(baseURL)
    spider.start(1,4)

