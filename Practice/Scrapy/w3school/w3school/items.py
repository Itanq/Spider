# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

#project: w3school  
#file   : items.py  
#author : younghz  
#brief  : define W3schoolItem.  
  
from scrapy.item import Item,Field  
  
class W3schoolItem(Item):  
    title = Field()  
    link = Field()  
    desc = Field()  

