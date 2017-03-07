# -*- coding: utf-8 -*-

from ..items import Image
from scrapy.spiders import CrawlSpider


def category_name(num):
    if num == '0':
        return 'general'
    elif num == '1':
        return 'artist'
    # elif num == '2':
    #     return ''
    elif num == '3':
        return 'copyright'
    elif num == '4':
        return 'character'
    return 'undefined'


class PageSpider(CrawlSpider):
    name = "danbooru#page"
    allowed_domains = ["danbooru.donmai.us"]
    start_urls = []

    def __init__(self, *a, **kw):
        super(PageSpider, self).__init__(*a, **kw)

        # オプションを取得
        url = kw.get('URL')
        if url:
            self.logger.info('Set URL: {}'.format(url))
            self.start_urls = [url]

    def parse_start_url(self, response):
        return self.item_page(response)

    @staticmethod
    def item_page(response):
        """
        アイテムページを解析し、データを抽出
        :param response:
        :return:
        """

        # タグデータ
        tags = {}
        for tag in response.css('#tag-list li[class^="category-"]'):
            num = tag.css('::attr(class)').re_first('category-(\d)')
            name = category_name(num)
            keyword = tag.css('a.search-tag::text').extract_first()
            if name in tags.keys():
                tags[name].append(keyword)
            else:
                tags[name] = []
                tags[name].append(keyword)

        # 投稿ID
        post_id = response.css('meta[name="post-id"]::attr(content)').extract_first()

        # 画像情報
        image = Image()
        image['id'] = post_id
        image['image_urls'] = []
        image['tags'] = tags

        link = response.css('img#image::attr(src)').extract_first()

        if link is not None:
            image['image_urls'].append(response.urljoin(link))

        yield image
