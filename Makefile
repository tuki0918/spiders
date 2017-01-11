WORK_DIR=/usr/src/app

.PHONY: build bash run crawl
build:
	docker build -t py36 .
bash:
	docker run --rm -it \
       --name py36-spiders \
       -v $(PWD):$(WORK_DIR) \
       -w $(WORK_DIR) \
       py36 /bin/bash
run:
	docker run --rm -it \
       -v $(PWD):$(WORK_DIR) \
       -w $(WORK_DIR) \
       py36 $(RUN_ARGS)
crawl:
	docker run --rm -it \
       -v $(PWD):$(WORK_DIR) \
       -w $(WORK_DIR)/sankaku \
       py36 scrapy crawl $(RUN_ARGS)
