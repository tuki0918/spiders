import argparse
import ast
import json
import math
import os
import pandas as pd
import shutil
import tarfile
from datetime import datetime
from PIL import Image, ImageOps
from tqdm import tqdm

work_dir = '/tmp/dataset'
FLAGS = None

# data/train
#     dir/***.jpg
#     dir/***.jpg


def dataset_path(step='train'):
    """
    :param step:
    :return:
    """
    if step == 'validation':
        path = os.path.join(work_dir, 'validation')
    elif step == 'test':
        path = os.path.join(work_dir, 'test')
    else:
        path = os.path.join(work_dir, 'train')
    return path


def json_decode(content):
    try:
        return json.loads(content)
    except json.decoder.JSONDecodeError:
        # single quote json data
        return ast.literal_eval(content)


def resize(path, img_size=64):
    """
    :param path:
    :param img_size:
    :return:
    """
    img = Image.open(path, 'r')
    img = ImageOps.fit(img, (img_size, img_size), Image.ANTIALIAS)

    w, h = img.size
    p1 = math.floor((img_size - w) / 2)
    p2 = math.floor((img_size - h) / 2)

    canvas = Image.new('RGB', (img_size, img_size), (255, 255, 255))
    canvas.paste(img, (p1, p2))
    return canvas


def save_path(tag='etc', step='train'):
    # データセット保存先パス
    path = os.path.join(dataset_path(step), tag)
    # データセットディレクトリが存在しない場合作成する
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def dataset_archive():
    # ディレクトリ名
    tar_name = 'dataset_{:%Y%m%d%H%M}.tar.gz'.format(datetime.today())
    path = os.path.join(os.getcwd(), 'resources', 'outputs', tar_name)

    # 圧縮処理
    archive = tarfile.open(path, mode='w:gz')
    archive.add(work_dir)
    archive.close()
    # 削除処理
    shutil.rmtree(work_dir)


def process(csv_file):
    df = pd.read_csv(csv_file)
    print('{} file load.'.format(csv_file))

    # progress bar
    pbar = tqdm(total=len(df.index))
    for i, v in df.iterrows():
        pbar.update(1)

        # image
        image = json_decode(v['images'])
        if len(image) < 1:
            continue

        # tag
        tags = json_decode(v['tags'])
        if FLAGS.category not in tags:
            continue

        # data
        img_path = os.path.join(os.getcwd(), 'resources', 'images', image[0]['path'])
        tags = tags[FLAGS.category]

        try:
            # image load
            canvas = resize(img_path)
        except FileNotFoundError:
            continue

        # image copy
        for tag in tags:
            path = save_path(tag)
            file_name = '{}.jpg'.format(os.path.join(path, str(v['id'])))
            canvas.save(file_name, 'JPEG', quality=100, optimize=True)
    pbar.close()


def main():
    # CSVをロード
    csv_file = os.path.join(os.getcwd(), 'resources', 'outputs', FLAGS.csv)
    process(csv_file)

    # データセットファイルを作成
    dataset_archive()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', type=str, default='output.csv',
                        help='***')
    parser.add_argument('--category', type=str, default='character',
                        help='*** (copyright, character, artist, general)')
    FLAGS, unparsed = parser.parse_known_args()
    main()
