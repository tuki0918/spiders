#!/bin/sh

# コンテナ内のホームディレクトリ
WORK_DIR="/usr/src/app"

usage() {
    cat <<-EOF
    Usage: $0 {build|boot|bash|mongo|mongo-export|dataset|run|crawl}
EOF
    exit 1
}

case "$1" in
    # 構築
    build)
        docker build -t py36 .
        ;;
    # 起動
    boot)
        docker run --rm -it \
            --name py36-mongo \
            -v ${PWD}/resources/storage:/data/db \
            -v ${PWD}:${WORK_DIR} \
            -w ${WORK_DIR} \
            -d mongo
        ;;
    # 接続
    bash)
        docker run --rm -it \
            --name py36-spiders \
            --link py36-mongo:mongo \
            -v ${PWD}:${WORK_DIR} \
            -w ${WORK_DIR} \
            py36 /bin/bash
        ;;
    # 接続（mongodb）
    mongo)
        docker exec -it \
            py36-mongo mongo
        ;;
    # DBダンプ（mongodb）
    mongo-export)
        docker exec -it \
            py36-mongo misc/export.sh
        ;;
    # データセット作成
    dataset)
        docker run --rm -it \
            --name py36-spiders \
            --link py36-mongo:mongo \
            -v ${PWD}:${WORK_DIR} \
            -w ${WORK_DIR} \
            py36 python misc/dataset.py $2
        ;;
    # スクリプトの実行
    run)
        docker run --rm -it \
            --link py36-mongo:mongo \
            -v ${PWD}:${WORK_DIR} \
            -w ${WORK_DIR} \
            py36 $2
        ;;
    # クローラーの実行
    crawl)
        docker run --rm -it \
            --link py36-mongo:mongo \
            -v ${PWD}:${WORK_DIR} \
            -w ${WORK_DIR}/danbooru \
            py36 scrapy crawl $2
        ;;
    *)
        usage
        ;;
esac
