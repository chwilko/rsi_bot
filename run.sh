#!/bin/sh
export $(grep -v '^#' .env | xargs)

exec poetry run python main.py
