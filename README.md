# spiders

機械学習用データ収集のためのスパイダー


### 使用方法

`requirements.txt`に記載されたパッケージをインストールしたDockerイメージを作成する

```
make build
```

必要なコンテナの起動（DB:mongodb）

```
make boot
```

データ収集

```
make crawl RUN_ARGS="danbooru#all -o danbooru.csv"
```

データセットを作成する

```
# DBデータをCSVに書き出す
make mongo-export

# CSVにデータを元にデータセットを作成
# scrapyの`-o ***.csv`で出力したファイルも可（フィールド名がデータ箇所にある場合は削除すること）
make dataset RUN_ARGS="--csv ***.csv"
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
