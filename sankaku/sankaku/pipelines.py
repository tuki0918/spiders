# -*- coding: utf-8 -*-

import cv2
import numpy as np
import math
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
            # 画像は１つの前提
            for image in item['images']:
                image_path = os.path.join(image_base_path, image['path'])

                # 画像の読込
                image = cv2.imread(image_path)

                # グレースケール画像に変換
                image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                image_gray = cv2.equalizeHist(image_gray)

                # numpy.ndarray
                faces = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=5, minSize=(24, 24))
                if isinstance(faces, np.ndarray):
                    item['faces'] = faces.tolist()

            return item


class ImageTrimmingFacePipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, Image):
            settings = spider.settings
            image_base_path = settings.get('IMAGES_STORE')
            output_dir = os.path.join(image_base_path, settings.get('IMAGES_STORE_ANIME_FACE_DIR'))

            # ディレクトリを再帰的に作成
            os.makedirs(output_dir, exist_ok=True)

            for i, (x, y, w, h) in enumerate(item['faces']):
                # 画像は１つの前提
                image_path = os.path.join(image_base_path, item['images'][0]['path'])

                # 画像ファイル名の拡張子を除いた部分を取得する。
                image_name = os.path.splitext(os.path.basename(image_path))[0]
                # 出力先のファイルパスを組み立てる。
                output_path = os.path.join(output_dir, '{0}_{1}.jpg'.format(image_name, i))

                # 画像の読込
                image = cv2.imread(image_path)

                # 抽出範囲を大きく取る
                p1 = math.ceil(y * 0.5)
                p2 = math.ceil(y * 0.75 + h)
                p3 = math.ceil(x * 1)
                p4 = math.ceil(x * 1 + w)

                # トリミング
                # cv2.imwrite(output_path, image[y:y + h, x:x + w])
                cv2.imwrite(output_path, image[p1:p2, p3:p4])

            return item
