# -*- coding: utf-8 -*-
import scrapy

from sankaku.spiders.page import PageSpider


class RankingSpider(scrapy.Spider):
    name = "ranking"
    allowed_domains = ["chan.sankakucomplex.com"]
    start_urls = ['http://chan.sankakucomplex.com/']

    def parse(self, response):
        """
        ページを解析し、ランキングページURLを投げる
        :param response:
        :return:
        """

        url = 'https://chan.sankakucomplex.com/ja/?tags=date%3A2017-01-01..2017-02-01%20order%3Aquality'
        yield scrapy.Request(url, callback=self.rank_page)

    @staticmethod
    def rank_page(response):
        """
        ランキングページを解析し、アイテムページURLを投げる
        :param response:
        :return:
        """

        url = 'https://chan.sankakucomplex.com/ja/post/show/5415670'
        yield scrapy.Request(url, callback=PageSpider.item_page)

        # next_page = response.css("div.page-link-option > a::attr('href')")
        # if next_page:
        #     url = response.urljoin(next_page[0].extract())
        #     yield scrapy.Request(url, callback=self.parse)
