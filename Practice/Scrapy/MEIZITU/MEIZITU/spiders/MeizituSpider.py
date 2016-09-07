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

    # 提取主页上的妹子图的个人页面链接
    def parse(self, response):
        sel = Selector(response)
        links = sel.xpath('//div[@id="maincontent"]/div[@class="postContent"]/div[@id="picture"]/p')
        print("Links: %s " % len(links))
        for link in links:
            href = link.xpath('.//a/@href').extract()[0]
            print("href: %s " % href)
            yield Request(href, callback=self.parse_item)

    # 处理个人页面上的图片
    def parse_item(self, response):
        sel = Selector(response)
        item = MeizituItem()
        site = sel.xpath('//div[@id="maincontent"]/div/div[@class="metaRight"]')
        item['meiziname'] = site.xpath('.//h2/a/text()').extract()
        item['tags'] = site.xpath('.//p/text()').extract()
        item['imageurl'] = sel.xpath('//div[@class="postContent"]/div[@id="picture"]/p/img/@src').extract()
        return item
