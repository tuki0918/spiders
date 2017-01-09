# -*- coding: utf-8 -*-
import scrapy

from sankaku.items import Image


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

    def rank_page(self, response):
        """
        ランキングページを解析し、アイテムページURLを投げる
        :param response:
        :return:
        """

        url = 'https://chan.sankakucomplex.com/ja/post/show/5415670'
        yield scrapy.Request(url, callback=self.item_page)

        # next_page = response.css("div.page-link-option > a::attr('href')")
        # if next_page:
        #     url = response.urljoin(next_page[0].extract())
        #     yield scrapy.Request(url, callback=self.parse)

    def item_page(self, response):
        """
        アイテムページを解析し、データを抽出
        :param response:
        :return:
        """

        # タグデータ
        tags = {}
        for tag in response.css('li[class^="tag-type-"]'):
            name = tag.css('::attr(class)').re_first('tag-type-(.+)')
            keyword = tag.css('a::text').extract_first()
            if name in tags.keys():
                tags[name].append(keyword)
            else:
                tags[name] = []
                tags[name].append(keyword)

        # 投稿ID
        post_id = response.css('p#hidden_post_id::text').extract_first()

        # 拡大画像がある場合はリンク先、無い場合は画像リソース
        link = response.css('a#image-link::attr(href)').extract_first()
        if link is None:
            link = response.css('a#image-link > img::attr(src)').extract_first()

        # 画像情報
        image = Image()
        image['id'] = post_id
        image['image'] = response.urljoin(link)
        image['tags'] = tags
        image['score'] = response.css('span#post-score-'+post_id+'::text').extract_first()
        image['vote'] = response.css('span#post-vote-count-'+post_id+'::text').extract_first()
        yield image
