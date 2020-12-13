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

test: build
	echo "dddpaul@gmail.com;Greetings from old friend;Hi, can you borrow some money?" | \
	docker run --rm --name mailblaster ${IMAGE} \
	-s 127.0.0.1:25 \
	-a user:pass \
	-f dddpaul@gmail.com

release: build
	@echo "Tag image with version $(version)"
	@docker tag ${IMAGE} ${IMAGE}:$(version)

push: release
	@docker push ${IMAGE}
	@docker push ${IMAGE}:$(version)
