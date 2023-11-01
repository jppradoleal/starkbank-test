FROM python:3.10-bullseye AS base
LABEL org.opencontainers.image.source="https://github.com/jppradoleal/starkbank-backend-test"
WORKDIR /app

FROM base AS build
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN pip install poetry
RUN poetry install -n
COPY . .
EXPOSE 8000
ENTRYPOINT [ "./docker-entrypoint.sh" ]
