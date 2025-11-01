#!/bin/sh

# Ожидание доступности PostgreSQL
echo "Ожидание PostgreSQL..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "PostgreSQL запущен"

# Применение миграций
python manage.py migrate

# Сбор статических файлов
python manage.py collectstatic --no-input

# Запуск команды, переданной в CMD Dockerfile (или docker-compose)
exec "$@"