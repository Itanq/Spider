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

    def spider_closed(self, spider):
        self.file.close()

class MyImagesPipeline(ImagesPipeline):

    def get_media_request(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url, meta={'item':item,'index':item['image_urls'].index(image_url)})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('logo.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class DownloadImagesPipeline(ImagesPipeline):
    #下载图片
    def get_media_requests(self,item,info):
        for image_url in item['image_urls']:
            #添加meta是为了下面重命名文件名使用
            #yield Request(image_url, meta={'item':item})
            yield Request(image_url,meta={'item':item,'index':item['image_urls'].index(image_url)})

    def file_path(self,request,response=None,info=None):
        #通过上面的meta传递过来item
        item=request.meta['item']
        #通过上面的index传递过来列表中当前下载图片的下标
        index=request.meta['index'] 

        #图片文件名，item['carname'][index]得到汽车名称，request.url.split('/')[-1].split('.')[-1]得到图片后缀jpg,png
        image_guid = item['companyName'][index]+item['jobName'][index]+'.'+request.url.split('/')[-1].split('.')[-1]
        #图片下载目录 此处item['country']即需要前面item['country']=''.join()......,否则目录名会变成\u97e9\u56fd\u6c7d\u8f66\u6807\u5fd7\xxx.jpg
        filename = u'full/{0}/{1}'.format(item['companyName'], image_guid) 
        return filename
