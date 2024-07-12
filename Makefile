.PHONY: build run test clean

build:
	docker-compose build

run:
	docker-compose up -d

test:
	docker-compose run test-runner

clean:
	docker-compose down -v