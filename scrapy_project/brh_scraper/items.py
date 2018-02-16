# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

class WSJData(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    value = scrapy.Field()

class WSJDataLoader(ItemLoader):
    deafult_output_processor = TakeFirst()
