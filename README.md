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

月刊ランキングページを解析する

```
make crawl RUN_ARGS="ranking -o ranking.jl"
```

指定したTAGの画像を収集/解析する

```
# 通常
make crawl RUN_ARGS="tag -a TAG=矢吹健太朗"

# 顔抽出処理を追加
make crawl RUN_ARGS="tag -a TAG=矢吹健太朗 -s IMAGES_STORE_ANIME_FACE_DIR=矢吹健太朗"
```

指定したページを解析する

```
make crawl RUN_ARGS="page -a URL=https://chan.sankakucomplex.com/ja/post/show/5597890"
```

収集データをファイルに書き出す

```
# csvにデータを出力
make mongo-export

# csvにデータを元にデータセットを作成
make dataset RUN_ARGS="--csv output_***.csv"
```

----

### 設定

下記設定ファイルを書き換える、または実行時に`-s VAL=value`で上書きする

```
sankaku/sankaku/settings.py
```

ディレクトリについて

+ `resources/cascades` ... カスケードファイル管理用
+ `resources/images` ... ダウンロード画像管理用
+ `resources/images/***` ... 顔認識した画像の切取（`IMAGES_STORE_ANIME_FACE_DIR`で指定）
+ `resources/images/full` ... ダウンロードした元画像
+ `resources/outputs` ... 収集データの出力先
+ `resources/storage` ... コンテナ内のデータ永続化用

----

### 備考

不適切な内容を含む場合があるため、18歳未満はご利用をお控えください。

### 対応サイト

+ https://chan.sankakucomplex.com/
