# -*- coding: utf-8 -*-
import scrapy

from datetime import datetime
from dateutil.relativedelta import relativedelta
from sankaku.spiders.page import PageSpider
from urllib.parse import urlparse, parse_qs


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

        # 集計期間：今日から１ヶ月前
        today = datetime.today()
        last_month = today + relativedelta(months=-1)
        period = '{:%Y-%m-%d}..{:%Y-%m-%d}'.format(last_month, today)

        self.logger.info('Set Ranking Date: {}'.format(period))

        url = 'https://chan.sankakucomplex.com/ja/?tags=date%3A{0}%20order%3Aquality'.format(period)
        yield scrapy.Request(url, callback=self.rank_page)

    def rank_page(self, response):
        """
        ランキングページを解析し、画像ページURLを投げる
        :param response:
        :return:
        """

        self.logger.info('Ranking Page: {}'.format(response.url))

        # 画像ページ
        for href in response.css('div.content a::attr(href)').re('/ja/post/show/\d+'):
            yield scrapy.Request(response.urljoin(href), callback=PageSpider.item_page)

        next_page = response.css('div.content > div::attr(next-page-url)').extract_first()
        if next_page:
            query = parse_qs(urlparse(next_page).query)
            if int(query['page'][0], 10) < 4:
                yield scrapy.Request(response.urljoin(next_page), callback=self.rank_page)
