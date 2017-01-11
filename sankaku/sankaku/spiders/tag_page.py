# -*- coding: utf-8 -*-

from sankaku.spiders.page import PageSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


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
        tag = kw.get('Tag')
        if tag:
            url = 'https://chan.sankakucomplex.com/?tags={}%20order%3Apopular'.format(tag)
            self.logger.info('Set Tag: {}'.format(tag))
            self.start_urls = [url]
