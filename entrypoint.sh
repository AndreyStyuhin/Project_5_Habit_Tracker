#!/bin/bash
set -e

: "${POSTGRES_HOST:?POSTGRES_HOST is not set}"
: "${POSTGRES_PORT:?POSTGRES_PORT is not set}"

echo "Ожидание PostgreSQL..."

while ! timeout 1 bash -c "</dev/tcp/$POSTGRES_HOST/$POSTGRES_PORT"; do
  echo "PostgreSQL не готов, ждем 1 секунду..."
  sleep 1
done

echo "PostgreSQL доступен!"

# Выполняем миграции и собираем статику
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Запускаем Gunicorn
exec gunicorn habit_tracker.wsgi:application --bind 0.0.0.0:8000
