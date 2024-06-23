FROM python:3.11-slim

RUN pip3 install poetry

# # -- Install Application into container:
WORKDIR /app

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry config virtualenvs.create false && poetry install

COPY /bot /app

CMD ["python", "/app/main.py"]
