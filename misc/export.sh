#!/bin/bash

set -eux

DB_HOST=localhost
DB_NAME=scrapy
DB_COLLECTION=images
OUTPUT_FILE=./resources/outputs/output`date +_%Y%m%d%H%M`.csv

mongoexport -h ${DB_HOST} --db ${DB_NAME} \
    --collection ${DB_COLLECTION} \
    --csv --out ${OUTPUT_FILE} \
    --fields 'id,images,tags'
