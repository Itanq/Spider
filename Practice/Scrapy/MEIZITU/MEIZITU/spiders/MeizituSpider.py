#-*- coding:utf-8 -*-

import scrapy

from scrapy import optional_features
optional_features.remove('boto')

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.loader import ItemLoader, Identity
from MEIZITU.items import MeizituItem

class MeizituSpider(scrapy.Spider):
    name = "Meizi"
    allowed_domains = ["meizitu.com"]
    start_urls = [
            'http://www.meizitu.com/',
    ]

    def parse(self, response):
        sel = Selector(response)
        links = sel.xpath('//div[@id="maincontent"]/div[@class="postContent"]')
        print("Links: %s " % len(links))
        for link in links:
            href = link.xpath('.//div[@id="picture"]/p/a/@href').extract()[0]
            print("href: %s " % href)
            yield Request(link, callback=self.parse_item)

    def parse_item(self, response):
        print("Start parse_item")
        sel = Selector(response)
        images = sel.xpath('//div[@class="postContent"]/div[@id="picture"]')
        print("len: %s" % len(images))
