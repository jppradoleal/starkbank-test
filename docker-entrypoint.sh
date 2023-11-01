#!/bin/bash

if [ -z "$STARKBANK_PRIVATE_KEY" ]; then
  export STARKBANK_PRIVATE_KEY=$(cat $STARKBANK_PRIVATE_KEY_FILE)
fi

if ["$ENV" = "dev"]; then
  if [ "$1" = "worker" ]; then
    poetry run \
      python -m debugpy --listen 0.0.0.0:5679 -m \
        celery -A starkbank_backend worker -l INFO
  elif [ "$1" = "beat" ]; then
    poetry run \
      python -m debugpy --listen 0.0.0.0:5680 -m \
        celery -A starkbank_backend beat -l INFO
  else
    poetry run python -m manage migrate

    mkdir log
    touch /app/log/access.log

    poetry run \
      python -m debugpy --listen 0.0.0.0:5678 -m \
        gunicorn starkbank_backend.asgi:application -k uvicorn.workers.UvicornWorker -w 3 \
        -b 0.0.0.0:8000 --log-level=info --access-logfile=/app/log/access.log -t 120
  fi
fi

if [ "$1" = "worker" ]; then
  poetry run python -m celery -A starkbank_backend worker -l INFO
elif [ "$1" = "beat" ]; then
  poetry run python -m celery -A starkbank_backend beat -l INFO
else
  poetry run python -m manage migrate

  mkdir log
  touch /app/log/access.log

  poetry run python -m \
    gunicorn starkbank_backend.asgi:application -k uvicorn.workers.UvicornWorker -w 3 \
    -b 0.0.0.0:8000 --log-level=info --access-logfile=/app/log/access.log -t 120
fi