# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request

class ShixisengPipeline(object):
    def __init__(self):
        self.file = codecs.open('Shixiseng.json', mode='wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line.decode("unicode_escape"))
        return item

class MyImagesPipeline(ImagesPipeline):

    def get_media_request(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url, meta={'item':item,'index':item['image_urls'].index(image_url)})

    def file_path(self, request=None, info=None):
        item = request.meta['item']
        index = request.meta['index']
        image_guid = item['companyName']+item['jobName']+request.url.split('/')[-1].split('.')[-1]
        filename = u'full/{0}/{1}'.format(item['companyName'], image_guid)
        return filename

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item
