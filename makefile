NAME=bot:latest

build:
	docker build -t $(NAME) .

run:
	docker run $(NAME)

lint:
	bash lint.sh .
