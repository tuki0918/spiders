# -*- coding: utf-8 -*-
import scrapy


class RankingSpider(scrapy.Spider):
    name = "ranking"
    allowed_domains = ["chan.sankakucomplex.com"]
    start_urls = ['http://chan.sankakucomplex.com/']

    def parse(self, response):
        pass
