# -*- coding: utf-8 -*-

from ..items import Image
from scrapy.spiders import CrawlSpider


class PageSpider(CrawlSpider):
    name = "sankaku#page"
    allowed_domains = ["chan.sankakucomplex.com"]
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

        # 画像情報
        image = Image()
        image['id'] = post_id
        image['image_urls'] = []
        image['tags'] = tags
        image['score'] = response.css('span#post-score-'+post_id+'::text').extract_first()
        image['vote'] = response.css('span#post-vote-count-'+post_id+'::text').extract_first()

        # 拡大画像がある場合はリンク先、無い場合は画像リソース
        link = response.css('a#image-link::attr(href)').extract_first()

        if link is None:
            link = response.css('a#image-link > img::attr(src)').extract_first()

        if link is not None:
            image['image_urls'].append(response.urljoin(link))

        yield image
