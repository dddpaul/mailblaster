.PHONY: all build release

IMAGE=dddpaul/mailblaster

all: build

build:
	@docker build --tag=${IMAGE} .

debug: build
	@docker run -it --entrypoint=sh ${IMAGE}

help: build
	@docker run --rm --name mailblaster ${IMAGE} -h

run: build
	@docker run --rm --name mailblaster ${IMAGE}

test-prep:
	-@docker network create mailblaster
	@docker run -d --rm --name exim-sender --net mailblaster -e PRIMARY_HOST=mx.dddpaul.pw -e SMTP_PORTS=25 -e ALLOWED_HOSTS=mailblaster dddpaul/exim-sender:1.3

test: build
	echo "dddpaul@gmail.com;Greetings from old русский friend;Пожалуйста!" | \
	docker run --rm -i --net mailblaster --name mailblaster -v ${PWD}/test-template.txt:/app/template.txt ${IMAGE} \
	-v \
	-s exim-sender:25 \
	-f "Pavel Derendyaev <dddpaul@gmail.com>" \
	-m /app/template.txt

release: build
	@echo "Tag image with version $(version)"
	@docker tag ${IMAGE} ${IMAGE}:$(version)

push: release
	@docker push ${IMAGE}
	@docker push ${IMAGE}:$(version)
