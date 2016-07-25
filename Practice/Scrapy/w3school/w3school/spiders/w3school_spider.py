#!/usr/bin/python  
# -*- coding:utf-8 -*-  
  
from scrapy.spider import Spider  
from scrapy.selector import Selector  
from scrapy import log  
  
from w3school.items import W3schoolItem  
  
  
class W3schoolSpider(Spider):  
    """爬取w3school标签"""  
    #log.start("log",loglevel='INFO')  
    name = "w3school"  
    allowed_domains = ["w3school.com.cn"]  
    start_urls = [  
        "http://www.w3school.com.cn/xml/xml_syntax.asp"  
    ]  
  
    def parse(self, response):  
  
        sel = Selector(response)  
        sites = sel.xpath('//div[@id="navsecond"]/div[@id="course"]/ul[1]/li')
        #print("sistes: %s " % len(sites))
        items = []  
  
        for site in sites:
            item = W3schoolItem()
            #print("site: ===> %s " % site)

            title = site.xpath('a/text()').extract()
            #print("title %s " % title)
            link = site.xpath('a/@href').extract()
            #print("link %s " % link)
            desc = site.xpath('a/@title').extract()
            #print("desc %s " % desc)

            item['title'] = [t.encode('utf-8') for t in title]
            item['link'] = [l.encode('utf-8') for l in link]
            item['desc'] = [d.encode('utf-8') for d in desc]

            items.append(item)
            print("items: %s " % items)
            #记录

        return items


