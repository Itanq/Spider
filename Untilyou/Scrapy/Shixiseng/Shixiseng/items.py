# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ShixisengItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    companyName = Field()
    companyUrl = Field()
    jobDesc = Field()
    jobClass = Field()
    jobName = Field()
    companyAddress = Field()
    workTime = Field()
    educationRequest = Field()
    money = Field()
    publicDate = Field()
    endDate = Field()

