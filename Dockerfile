# Этап 1: Базовый образ
FROM python:3.11-slim-bullseye

# Установка системных переменных
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Установка системных зависимостей
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev netcat-openbsd \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копирование скрипта точки входа
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Создание пользователя
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Копирование всего проекта
COPY . .

# Указание, что Gunicorn будет слушать этот порт
EXPOSE 8000

# Запуск entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "habit_tracker.wsgi:application", "--bind", "0.0.0.0:8000"]