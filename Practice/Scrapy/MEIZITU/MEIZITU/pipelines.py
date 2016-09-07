# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
import json
import codecs

class MeizituPipeline(object):
    def __init__(self):
        self.file = codecs.open("Meizitu.json", mode="wb", encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['imageurl']:
            yield Request(image_url, meta={'item':item,'index':item['imageurl'].index(image_url)})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        index = request.meta['index']

        image_guid = item['meiziname'][index] + '.' + request.url.split('/')[-1].split('.')[-1]
        filename = u'full/{0}/{1}'.format(item['tags'], image_guid)
