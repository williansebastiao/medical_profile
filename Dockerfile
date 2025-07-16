FROM python:3.13-alpine

WORKDIR /code

RUN apk add --no-cache \
    make \
    curl \
    bash \
    nano \
    git \
    tzdata && \
    cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    echo "America/Sao_Paulo" > /etc/timezone

ENV TZ=America/Sao_Paulo

RUN adduser -D appuser

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry config virtualenvs.in-project false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

RUN chown -R appuser:appuser /code

USER appuser
