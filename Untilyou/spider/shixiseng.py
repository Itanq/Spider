#-*- coding:utf-8 -*-

from untilyou import downloadImage
from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError,URLError
from bs4 import BeautifulSoup
import re

class Shixiseng():
    
    def __init__(self, number):
        self.number = number
        self.jobInfo = []
        self.jobURL = []
        #申明一个图片下载器
        self.download = downloadImage.DownloadImage() 
        self.baseURL = 'http://www.shixiseng.com'
        self.user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
        self.headers={'User_Agent':self.user_agent}
    
    # 获取某一职位jobclass所有招聘信息的网址
    def getJobPage(self,jobclass):
        '''
            输入的是一个需要查询的职位名称;
            返回的是有关此职位所有招聘信息的网址;
        '''
        pages = range(1,35)
        for page in pages:
            try:
                url = self.baseURL+'/interns?k='+jobclass+'&p='+str(page)
                html = urlopen(url)
            except(HTTPError,URLError) as e:
                print("网址输入错误")
                return None
            else:
                bsObject = BeautifulSoup(html.read(),"lxml")
                if bsObject.findAll('img',{"src":re.compile(".*?nocontent\.png")}):
                    break
                jobList = bsObject.findAll('div',{"class":"job_inf_inf"})
                for job in jobList:
                    joburl = job.find('a', {'href':re.compile(r'.*?intern.*?')})
                    self.jobURL.append(joburl)
        return self.jobURL

    # 获取某一具体职位的详细信息
    def getJobInfo(self, jobURL):
        '''
            输入的是某一个具体职位名称的网址;
            返回的是有关此招聘职位的具体信息:职位名称,职位发布时间,截至之间,职位要求等...
        '''
        try:
            url = self.baseURL + jobURL
            html = urlopen(url)
        except(HTTPError,URLError) as e:
            print("网址输入错误")
            return None
        else:
            bsObject = BeautifulSoup(html.read(),"lxml")
            # 公司名称
            jobComputer = bsObject.find("div",{"class":"jb_det_right_top"}).p
            # 职位名称
            jobName = bsObject.find("span", {"class":"job_name"})
            # 招聘信息发布时间
            jobStartTime = bsObject.find("span", {"class":"update_time"})
            # 招聘信息截止时间
            jobEndTime = bsObject.find("p", {"class":"closing_date"}).next_sibling
            # 公司地址
            jobAddress = bsObject.find("span", {"class":"city"})
            # 教育水平
            jobEducation = bsObject.find("span", {"class":"education"})
            # 职位描述
            jobContent = bsObject.find("div", {"class":"dec_content"})
            # 公司logo
            self.download.downloadImage(url, self.number)
            # 保存数据
            self.jobInfo.append([jobComputer.get_text(),jobName.get_text(),jobStartTime.get_text(),jobEndTime.get_text(),jobAddress.get_text(),jobEducation.get_text(),jobContent.get_text(), self.number])
            self.number = self.number + 1
            #print(jobName,'\n',jobStartTime,'\n', jobEndTime, '\n', jobAddress,'\n', jobAddress, '\n', jobEducation, '\n', jobContent)

    # 获得某一职位jobName的所有招聘信息
    def getJobsInfo(self, jobName):
        '''
            输入的是某一职位类别名;
            返回的是有关此类职位的所有详细招聘信息;
        '''
        jobList = self.getJobPage(jobName)
        if jobList is None:
            print("没有找到任何关于%s的招聘信息" % str(jobName))
        else:
            for job in jobList:
                if 'href' in job.attrs:
                    self.getJobInfo(job.attrs['href'])

    # 爬实习僧整个网站上的招聘信息
    def getAllInfo(self):
        jobName = ['Python']
        #jobName = ['IOS','Android','Python','Java','PHP','SEO','Node.js','C%2FC%2B%2B','Ruby%2FPerl',
        #           'Flash','2D%2F3D','Hadoop']
        for jobname in jobName:
            self.getJobsInfo(jobname)
            

    def output(self):
        count = range(0,len(self.jobInfo))
        for index in count:
            if self.jobInfo[index][0] is None:
                break
            print("公司名称: %s" % self.jobInfo[index][0])
            print("职位名称: %s" % self.jobInfo[index][1])
            print("发布日期: %s" % self.jobInfo[index][2])
            print("截至日期: %s" % self.jobInfo[index][3])
            print("公司地址: %s" % self.jobInfo[index][4])
            print("学历要求: %s" % self.jobInfo[index][5])
            print("职位描述: %s" % self.jobInfo[index][6])
            print("logo编号: %s" % self.jobInfo[index][7])
            print("\n\n")
        print("共爬取了数据 %s 条" % len(self.jobInfo))
            #print(self.jobInfo[0][0],self.jobInfo[0][1],self.jobInfo[0][2],self.jobInfo[0][3],self.jobInfo[0][4],self.jobInfo[0][5])


    def Run(self):
        self.getAllInfo();
        #self.output()


#def main():
#    spider = Shixiseng(0)
#    print("程序正在运行,请耐心耐心等待...")
#    spider.Run()
#    print("程序运行完成...")
#
#
#if __name__ == '__main__':
#    main()
#
