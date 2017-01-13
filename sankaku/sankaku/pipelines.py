# -*- coding: utf-8 -*-

from sankaku.items import Image
from scrapy.exceptions import DropItem


class ImageValidationPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, Image):
            settings = spider.settings

            image_urls = item['image_urls']
            score = item['score']

            # 画像URLが設定されていないものは破棄
            if not len(image_urls) > 0:
                raise DropItem('Missing image_urls: {}'.format(image_urls))

            # 評価値が最低評価値未満のものは破棄
            min_score = settings.get('ITEM_MIN_SCORE')
            if score and float(score) > min_score:
                return item
            else:
                raise DropItem('Missing score: {}'.format(score))
