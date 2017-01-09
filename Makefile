WORK_DIR=/usr/src/app

.PHONY: build boot bash run crawl
build:
	docker build -t py36 .
boot:
	docker run -itd \
       --name py36-spiders \
       -v $(PWD):$(WORK_DIR) \
       -w $(WORK_DIR) \
       py36 /bin/bash
bash:
	docker exec -it py36-spiders \
       /bin/bash
run:
	docker run --rm -it \
       -v $(PWD):$(WORK_DIR) \
       -w $(WORK_DIR) \
       py36 $(RUN_ARGS)
crawl:
	docker run --rm -it \
       -v $(PWD):$(WORK_DIR) \
       -w $(WORK_DIR)/src \
       py36 scrapy crawl $(RUN_ARGS)
