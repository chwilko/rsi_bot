# RSI Discord Bot
This project implements a Discord bot . 
The bot is designed to analyze data from [bybit](https://www.bybit.com/trade/usdt/SOLUSDT). It calculates the relative strength index (RSI) and if the index is not within the specified range, it sends information about it on the specified channel on discord.

## author
Bartłomiej Chwiłkowski (github: chwilko)

## license
MIT license

# Table of content
- [RSI Discord Bot](#rsi-discord-bot)
  - [author](#author)
  - [license](#license)
- [Table of content](#table-of-content)
- [Installation](#installation)
  - [set bot and channel](#set-bot-and-channel)
  - [run](#run)
- [For developers](#for-developers)
  - [setup environment](#setup-environment)
  - [linting](#linting)
  - [test](#test)


# Installation
## set bot and channel
First, set the bot token to be handled by the code and the ID of the channel to which messages are to be sent.

These variables should be set in the env file
```
BOT_TOKEN=YOUR_BOT_TOKEN
CHANNEL_ID=YOUR_CHANNEL_ID
```
replace _YOUR_BOT_TOKEN_ and _YOUR_CHANNEL_ID_ respectively.

## run
To run the application, first build the image
```
docker build -t bot_image .
```
and then run the container. 

```
docker run bot_image
```

Also, you can use the makefile.
```
make build
make run
```

# For developers

## setup environment
For the virtual environment, use poetry.
```
python -m pip install poetry
```

Next start virtual environment
```
poetry shell
```
and install dependencies.
```
poetry install
```

## linting
To use a linter call
```
bash lint.sh .
```

Also, you can use the makefile.
```
make lint
```

## test
To test the code first run the virtual environment
```
poetry shell
```
Then run `pytest`.
```
pytest
```
