# -*- coding: utf-8 -*-
import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from .page import PageSpider


class AllSpider(CrawlSpider):
    name = "danbooru#all"
    allowed_domains = ["danbooru.donmai.us"]
    start_urls = ['http://danbooru.donmai.us/posts']

    rules = (
        # 画像ページ
        Rule(LinkExtractor(allow=('/posts/\d+',)), callback=PageSpider.item_page),
    )

    def parse_start_url(self, response):
        """
        次のページが存在する場合は次へ
        :param response:
        :return:
        """

        self.logger.info('Post Page: {}'.format(response.url))

        settings = self.settings

        # 再帰探索を有効にする
        is_recursive = settings.get('RECURSIVE_SEARCH')

        next_page = response.css('div.paginator a[rel="next"]::attr(href)').extract_first()
        if is_recursive and next_page:
            yield scrapy.Request(response.urljoin(next_page))
