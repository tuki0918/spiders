# -*- coding: utf-8 -*-

from sankaku.items import Image
from scrapy.exceptions import DropItem


class ImageValidationPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, Image):
            settings = spider.settings
            min_score = settings.get('ITEM_MIN_SCORE')
            score = item['score']
            if score and float(score) > min_score:
                return item
            else:
                raise DropItem('Missing score: {}'.format(score))
