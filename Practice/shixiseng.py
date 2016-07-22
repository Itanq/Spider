#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import sys

# 解决数据写入文件是的编码不匹配问题
reload(sys)
sys.setdefaultencoding('utf-8')

class Tool():
    '''
        清除html的各种标签类
    '''
    removeImg = re.compile('<img.*?>| {7}')
    removeAddr = re.compile('<a.*?>|</a>')
    removeNBSP = re.compile('&nbsp')
    removeExtraTag = re.compile('<.*?>')

    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD = re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br><br>|<br>')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.removeNBSP, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        return x.strip()


class shixiseng():
    '''
        根据你输入的职位来爬取招聘信息的爬虫类
    '''
    def __init__(self):
        self.baseURL = "http://www.shixiseng.com"
        self.job_content = []
        self.user_agent = ''
        self.headers = {'User-Agent':self.user_agent}
        self.tool = Tool()

    def getPage(self, URL):
        try:
            request = urllib2.Request(URL)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"爬取信息错误,错误原因:",e.reason
            return None

    def getJobList(self, page):
        if not page:
            print u"加载失败..."
            return None
        pattern = re.compile('<div class="job_head">.*?<a href="(.*?)" title="(.*?)"',re.S)
        items = re.findall(pattern, page)
        jobList = []
        for item in items:
            jobList.append([item[0].strip(),item[1].strip()])
        return jobList

    def getJobContents(self, URL):
        page = self.getPage(URL)
        if not page:
            print u'加载失败...'
            return None
        pattern = re.compile('<span class="job_name".*?>(.*?)</span>.*?'+'<span class="daymoney">(.*?)</span>.*?'+'<span class="city".*?>(.*?)</span>.*?'+'<div class="dec_content">(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        for item in items:
            self.job_content.append([item[0].strip(),item[1].strip(),item[2].strip(),item[3].strip()])

    def output(self, fileName):
        f = open(fileName, 'w+')
        line = u"\n--------------------------------------------------\n\n\n"
        enter = '\n'
        for item in self.job_content:
            f.write("职位名称: ")
            f.write(self.tool.replace(item[0]))
            f.write("\n日薪: ")
            f.write(self.tool.replace(item[1]))
            f.write("\n地点: ")
            f.write(self.tool.replace(item[2]))
            f.write("\n职位描述: \n")
            f.write(self.tool.replace(item[3]))
            f.write(line)
        f.close()


def main():
    job = raw_input('请输入你要爬取的职位(默认是C/C++): ')
    spider_job = shixiseng()
    URL = spider_job.baseURL + "/interns?k=" + str(job) + "&p=1"
    print u"正在建立连接..."
    basePage = spider_job.getPage(URL)
    print u"正在获取职位列表..."
    job_list = spider_job.getJobList(basePage)
    job_content = []
    count = 0
    print u"共获取到",len(job_list),u"个职位,如下: "
    for item in job_list:
        count += 1
        URL = spider_job.baseURL + item[0]
        print 'job', count, ': ', item[1]
        spider_job.getJobContents(URL)
    print u"结果保存到当前目录下ans_shixiseng.txt文件中."
    spider_job.output('ans_shixiseng.txt')

if __name__ == '__main__':
    main()
