IMAGE_NAME=bot_image
SECRETS_ID=bot_token channel_id


build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run $(IMAGE_NAME)

lint:
	bash lint.sh .
