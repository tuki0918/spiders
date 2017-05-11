# spiders

機械学習用データ収集のためのスパイダー


### 使用方法

`requirements.txt`に記載されたパッケージをインストールしたDockerイメージを作成する

```
./run.sh build
```

必要なコンテナの起動（DB:mongodb）

```
./run.sh boot
```

データ収集

```
./run.sh crawl "danbooru#all -o danbooru.csv"
```

データセットを作成する

```
# DBデータをCSVに書き出す
./run.sh mongo-export

# CSVにデータを元にデータセットを作成
# scrapyの`-o ***.csv`で出力したファイルも可（フィールド名がデータ箇所にある場合は削除すること）
./run.sh dataset "--csv ***.csv"
```

データセットを解凍する

```
# 解凍後に分類クラス毎のファイル数が表示されるので要確認（偏りが激しいため）
./misc/extract.sh dataset_***.tar.gz | tee extract.txt
```

----

### 設定

下記設定ファイルを書き換える、または実行時に`-s VAL=value`で上書きする

```
danbooru/danbooru/settings.py
```

ディレクトリについて

+ `resources/cascades` ... カスケードファイル管理用
+ `resources/images` ... ダウンロード画像管理用
+ `resources/images/***` ... 顔認識した画像の切取（`IMAGES_STORE_ANIME_FACE_DIR`で指定）
+ `resources/images/full` ... ダウンロードした元画像
+ `resources/outputs` ... 収集データの出力先
+ `resources/storage` ... コンテナ内のデータ永続化用

----

### 対応サイト

+ http://danbooru.donmai.us/
+ https://chan.sankakucomplex.com/
