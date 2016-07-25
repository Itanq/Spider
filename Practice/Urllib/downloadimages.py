#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import os

class ImagesSpider():
    '''
        自动爬取游迅网上图片的爬虫类
    '''
    def __init__(self):
        self.baseURL = 'http://pic.yxdown.com'
        self.user_agent = ''
        self.headers = {'User-Agent':self.user_agent}

    def getPage(self, URL):
        try:
            request = urllib2.Request(URL)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接网站失败,错误原因: ",e.reason
            return None


    def getImagesURL(self, page):
        if not page:
            print u"加载失败..."
            return None
        pattern = re.compile('<div class="cbmiddle">.*?<a.*?href="(.*?)".*?>',re.S)
        item = re.findall(pattern, page)
        return item

    def getImages(self, URL):
        page = self.getPage(URL)
        if not page:
            print 'URL:', URL , u"加载失败..."
            return None
        pattern = re.compile('"original":"(.*?)"', re.S)
        data = re.findall(pattern, page)
        List = []
        for item in data:
            List.append(item.strip())
        return List
    
    def creatFile(self, count):
        fileName = str('./Images/')+str(count) + '.jpg'
        return fileName

    def saveImages(self, imageURL, fileName):
        u = urllib2.urlopen(imageURL)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        print u"保存图片: ",fileName
        f.close()
    



def main():
    image_spider = ImagesSpider()
    URL = image_spider.baseURL + '/list/0_0_1.html'
    pageHtml = image_spider.getPage(URL)
    images_list = image_spider.getImagesURL(pageHtml)
    count = 1
    for item in images_list:
        URL = image_spider.baseURL + item
        images = image_spider.getImages(URL)
        for img in images:
            fileName = image_spider.creatFile(count)
            image_spider.saveImages(img, fileName)
            count += 1

if __name__ == '__main__':
    main()


