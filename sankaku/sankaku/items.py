# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Image(scrapy.Item):
    id = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    tags = scrapy.Field()
    score = scrapy.Field()
    vote = scrapy.Field()
