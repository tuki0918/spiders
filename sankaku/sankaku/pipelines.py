# -*- coding: utf-8 -*-

import cv2
import os
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


class ImageFacePointPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, Image):
            settings = spider.settings
            cascade_file = settings.get('CASCADE_ANIME_FACE_PATH')
            image_base_path = settings.get('IMAGES_STORE')

            item['faces'] = []

            # ファイルを見つからない場合は処理を継続しない
            if not os.path.isfile(cascade_file):
                return item

            cascade = cv2.CascadeClassifier(cascade_file)

            # 特徴データを追加する
            for image in item['images']:
                image_path = image_base_path + '/' + image['path']

                # 画像の読込
                image = cv2.imread(image_path)

                # グレースケール画像に変換
                image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                image_gray = cv2.equalizeHist(image_gray)

                # numpy.ndarray
                faces = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=5, minSize=(24, 24))
                item['faces'] = faces.tolist()

            return item
