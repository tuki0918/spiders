WORK_DIR=/usr/src/app

.PHONY: build bash mongo mongo-export dataset run crawl
build:
	docker build -t py36 .
boot:
	docker run --rm -it \
        --name py36-mongo \
        -v $(PWD)/resources/storage:/data/db \
        -v $(PWD):$(WORK_DIR) \
        -w $(WORK_DIR) \
        -d mongo
bash:
	docker run --rm -it \
        --name py36-spiders \
        --link py36-mongo:mongo \
        -v $(PWD):$(WORK_DIR) \
        -w $(WORK_DIR) \
        py36 /bin/bash
mongo:
	docker exec -it \
        py36-mongo mongo
mongo-export:
	docker exec -it \
        py36-mongo misc/export.sh
dataset:
	docker run --rm -it \
        --name py36-spiders \
        --link py36-mongo:mongo \
        -v $(PWD):$(WORK_DIR) \
        -w $(WORK_DIR) \
        py36 python misc/dataset.py $(RUN_ARGS)
run:
	docker run --rm -it \
        --link py36-mongo:mongo \
        -v $(PWD):$(WORK_DIR) \
        -w $(WORK_DIR) \
        py36 $(RUN_ARGS)
crawl:
	docker run --rm -it \
        --link py36-mongo:mongo \
        -v $(PWD):$(WORK_DIR) \
        -w $(WORK_DIR)/danbooru \
        py36 scrapy crawl $(RUN_ARGS)
