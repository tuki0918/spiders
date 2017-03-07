# -*- coding: utf-8 -*-
import scrapy

from datetime import datetime
from dateutil.relativedelta import relativedelta
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urlparse, parse_qs
from .page import PageSpider


class RankingSpider(CrawlSpider):
    name = "sankaku#ranking"
    allowed_domains = ["chan.sankakucomplex.com"]
    start_urls = []

    rules = (
        # 画像ページ
        Rule(LinkExtractor(allow=('/ja/post/show/\d+',)), callback=PageSpider.item_page),
    )

    def __init__(self, *a, **kw):
        super(RankingSpider, self).__init__(*a, **kw)

        # ランキング集計期間：１ヶ月前から今日
        today = datetime.today()
        last_month = today + relativedelta(months=-1)
        period = '{:%Y-%m-%d}..{:%Y-%m-%d}'.format(last_month, today)
        url = 'https://chan.sankakucomplex.com/ja/?tags=date%3A{}%20order%3Aquality'.format(period)

        self.logger.info('Set Ranking Date: {}'.format(period))
        self.start_urls = [url]

    def parse_start_url(self, response):
        """
        次のページが存在する場合は次へ
        :param response:
        :return:
        """

        self.logger.info('Ranking Page: {}'.format(response.url))

        next_page = response.css('div.content > div::attr(next-page-url)').extract_first()
        if next_page:
            query = parse_qs(urlparse(next_page).query)
            if int(query['page'][0], 10) < 4:
                yield scrapy.Request(response.urljoin(next_page))
