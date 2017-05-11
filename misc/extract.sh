#!/bin/bash

set -eu

# hack: space in filename
IFS="
"

# new directory
OUTPUT_DIR=./resources/outputs/dataset`date +_%Y%m%d%H%M`

# extract to "OUTPUT_DIR"
mkdir ${OUTPUT_DIR} && tar xzf $1 -C ${OUTPUT_DIR} --strip-components 1

# number of files in "OUTPUT_DIR"
for d in `find ${OUTPUT_DIR} -type d`; do echo $d,`ls "${d}" | wc -l`; done
