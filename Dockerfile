FROM python:3.11-slim


RUN pip3 install poetry

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.lock
COPY /bot /app/bot
COPY .env /app/.env
COPY main.py /app/main.py


RUN poetry config virtualenvs.create false && \
    poetry install --without dev


COPY run.sh /app/run.sh

CMD ["bash", "run.sh"]
