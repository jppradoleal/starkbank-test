
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
  poetry run \
  python -m debugpy --listen 0.0.0.0:5678 -m manage runserver 0.0.0.0:8000
fi
