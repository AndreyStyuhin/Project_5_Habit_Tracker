#!/bin/bash
set -e

: "${POSTGRES_HOST:?POSTGRES_HOST is not set}"
: "${POSTGRES_PORT:?POSTGRES_PORT is not set}"

echo "Ожидание PostgreSQL..."
counter=0
while ! timeout 1 bash -c "</dev/tcp/$POSTGRES_HOST/$POSTGRES_PORT"; do
  echo "PostgreSQL не готов, ждем 1 секунду..."
  sleep 1
  ((counter++))
  if [ $counter -gt 30 ]; then
    echo "❌ Timeout waiting for PostgreSQL"
    exit 1
  fi
done
echo "PostgreSQL доступен!"

# Миграции и статика только если не SKIP_MIGRATE (для celery/beat set SKIP_MIGRATE=true)
if [ -z "$SKIP_MIGRATE" ]; then
  python manage.py migrate --noinput
fi
python manage.py collectstatic --noinput

exec "$@"