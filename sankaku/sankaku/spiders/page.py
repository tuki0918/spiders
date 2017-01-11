# -*- coding: utf-8 -*-
import scrapy

from sankaku.items import Image


class PageSpider(scrapy.Spider):
    name = "page"
    allowed_domains = ["chan.sankakucomplex.com"]
    start_urls = ['http://chan.sankakucomplex.com/']

    def parse(self, response):
        pass

    @staticmethod
    def item_page(response):
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
        image['image_urls'] = [response.urljoin(link)]
        image['tags'] = tags
        image['score'] = response.css('span#post-score-'+post_id+'::text').extract_first()
        image['vote'] = response.css('span#post-vote-count-'+post_id+'::text').extract_first()
        yield image
