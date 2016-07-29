# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from Shixiseng.items import ShixisengItem

from bs4 import BeautifulSoup
import re

class ShixisengSpider(Spider):
    name = "shixiseng"
    allowed_domains = ["shixiseng.com"]
    start_urls = [
        'http://www.shixiseng.com/',
    ]

    # 爬取整个实习僧网站上的招聘信息的展示链接
    def parse(self, response):
        sel = Selector(response)
        urls = sel.xpath('//div[@class="center_btm"]/a[@class="look_more"]/@href').extract()
        urlPage = urls[0][0:len(urls[0])-1]
        for number in range(1,101):
            job_url = 'http://www.shixiseng.com' + urlPage + str(number)
            yield Request(job_url, callback=self.parse_job_url)

    # 解析出当前分类职业的所有招聘信息的链接
    def parse_job_url(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@id="load_box_item"]')
        for site in sites:
            urls = site.xpath('//div[@class="job_head"]/a/@href').extract()
            for index in range(0, len(urls)):
                url = 'http://www.shixiseng.com' + str(urls[index])
                yield Request(url, callback=self.parse_item)

    # 处理每一个招聘职位的页面
    def parse_item(self, response):
        sel = Selector(response)
        item = ShixisengItem()
        sites = sel.xpath('//div[@class="jb_det_left"]')
        for site in sites:

            companyName = sel.xpath('//div[@class="jb_det_right"]/div[@class="jb_det_right_top"]/p[1]/a/text()').extract()
            companyUrl = sel.xpath('//div[@class="jb_det_right"]/div[@class="jb_det_right_top"]/p[@class="web_url"]/a/@href').extract()
            jobClass = sel.xpath('//div[@class="jb_det_right"]/div[@class="jb_det_right_top"]/p[@class="domain"]/span/text()').extract()
            jobName = site.xpath('.//div[@class="jb_det_left_top"]/span[@class="job_name"]/text()').extract()
            companyAddress = site.xpath('.//div[@class="jb_det_left_mid"]/span[@class="city"]/@title').extract()
            workTime = site.xpath('.//div[@class="jb_det_left_mid"]/span[@class="month"]/text()').extract()
            educationRequest = site.xpath('.//div[@class="jb_det_left_mid"]/span[@class="education"]/text()').extract()
            money = site.xpath('.//div[@class="jb_det_left_mid"]/span[@class="daymoney"]/text()').extract()
            publicDate = site.xpath('.//div[@class="jb_det_left_top"]/span[@class="update_time"]/text()').extract()
            endDate = site.xpath('.//p[@class="date"]/text()').extract()

            item['companyName'] = [c.encode('utf-8') for c in companyName]
            item['companyUrl'] = [c.encode('utf-8') for c in companyUrl]
            item['jobClass'] = [j.encode('utf-8') for j in jobClass]
            item['jobName'] = [j.encode('utf-8') for j in jobName]
            item['companyAddress'] = [c.encode('utf-8') for c in companyAddress]
            item['workTime'] = [w.encode('utf-8') for w in workTime]
            item['educationRequest'] = [e.encode('utf-8') for e in educationRequest]
            item['money'] = [m.encode('utf-8') for m in money]
            item['publicDate'] = [p.encode('utf-8') for p in publicDate]
            item['endDate'] = [e.encode('utf-8') for e in endDate]
        return item


