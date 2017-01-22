# -*- coding: utf-8 -*-
import scrapy

from sankaku.spiders.page import PageSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse, parse_qs


class TagPageSpider(CrawlSpider):
    name = "tag"
    allowed_domains = ["chan.sankakucomplex.com"]
    start_urls = []

    rules = (
        # 画像ページ
        Rule(LinkExtractor(allow=('/ja/post/show/\d+',)), callback=PageSpider.item_page),
    )

    def __init__(self, *a, **kw):
        super(TagPageSpider, self).__init__(*a, **kw)

        # オプションを取得
        tag = kw.get('TAG')
        if tag:
            url = 'https://chan.sankakucomplex.com/?tags={}%20order%3Apopular'.format(tag)
            self.logger.info('Set Tag: {}'.format(tag))
            self.start_urls = [url]

    def parse_start_url(self, response):
        """
        次のページが存在する場合は次へ
        :param response:
        :return:
        """

        self.logger.info('Tag Page: {}'.format(response.url))

        settings = self.settings

        # 再帰探索を有効にする
        is_recursive = settings.get('RECURSIVE_SEARCH')

        next_page = response.css('div.content > div::attr(next-page-url)').extract_first()
        if is_recursive and next_page:
            yield scrapy.Request(response.urljoin(next_page))
