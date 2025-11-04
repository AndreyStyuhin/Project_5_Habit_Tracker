

# Project 5: Habit Tracker: Backend 🚀

## Описание

**Habit Tracker** — это мощное **backend-приложение** для отслеживания и управления привычками, построенное на **Django** и **Django REST Framework **Приложение реализует полноценный **REST API**, который обеспечивает создание, управление и валидацию привычек, а также отправку **асинхронных напоминаний** через **Telegram-бот** с помощью **Celery** и **Redis**. Проект разработан с учетом требований к современным API: использует **JWT-аутентификацию**, имеет полную **документацию (Swagger/ReDoc)** и покрыт **юнит-тестами** (pytest).


| **Ключевые особенности**          | **Валидация привычек**                                                 |
| :-------------------------------- |:-----------------------------------------------------------------------|
| 🛡️ JWT-аутентификация            | ⏱️ Длительность выполнения: **$\le 120$ секунд**                       |
| 🔔 Telegram-напоминания (Celery)  | 🗓️ Периодичность: **$\ge 1$ раза в 7 дней**                           |
| 🐳 Контейнеризация (Docker/Nginx) | 🤝 Исключение конфликта вознаграждения и связанной привычки            |
| 🔄 CI/CD (GitHub Actions)         | 🚫 Ограничения для "приятных" привычек (нет вознаграждения/связанной)  |

**Адрес развернутого приложения (Production):**
> http://212.22.70.98/ 

-----

## Используемые технологии 🛠️

| Категория           | Технология                                    | Описание                                          |
| :------------------ | :-------------------------------------------- |:--------------------------------------------------|
| **Основной стек**   | **Python 3.11**, **Django 5.x**, **DRF**      | Язык программирования и фреймворки для создания API. |
| **Контейнеризация** | **Docker**, **Docker Compose**, **Nginx**     | Контейнеризация сервисов (App, DB, Redis, Celery, Nginx). |
| **Аутентификация**  | **djangorestframework-simplejwt**             | Реализация JWT-токенов.                           |
| **База данных**     | **PostgreSQL**                                | Реляционная БД для production-окружения.          |
| **Асинхронность**   | **Celery**, **Redis**, **django-celery-beat** | Брокер сообщений, бэкенд и планировщик для асинхронных задач. |
| **CI/CD**           | **GitHub Actions**                            | Автоматическое тестирование, сборка и деплой проекта. |
| **Документация**    | **drf-yasg** (Swagger/ReDoc)                  | Генерация интерактивной документации API.         |
| **Тестирование**    | **pytest-django**, **pytest-cov**             | Юнит-тестирование с целью покрытия $\ge 80\%$.    |

-----

## Установка и запуск (Локально через Docker) 🐳

Проект полностью контейнеризирован, поэтому для запуска локально вам понадобятся только **Docker** и **Docker Compose**.

1.  **Клонирование репозитория:**
    ```bash
    git clone [https://github.com/AndreyStyuhin/Project_5_Habit_Tracker.git](https://github.com/AndreyStyuhin/Project_5_Habit_Tracker.git)
    cd Project_5_Habit_Tracker
    ```

2.  **Настройка переменных окружения:**
    Скопируйте файл с примерами переменных и заполните его.
    ```bash
    cp .env.example .env
    ```
    Вам нужно **обязательно** заполнить `SECRET_KEY` и `TELEGRAM_BOT_TOKEN` в файле `.env`. Остальные (Postgres, Redis) уже настроены для Docker.

3.  **Сборка и запуск контейнеров:**
    Эта команда скачает образы (Postgres, Redis, Nginx), соберет образ Django (со всеми `requirements.txt`) и запустит все 5 сервисов в фоновом режиме.
    ```bash
    docker-compose up --build -d
    ```

4.  **Применение миграций:**
    После первого запуска нужно применить миграции к базе данных (сервис `db`).
    ```bash
    docker-compose exec app python manage.py migrate
    ```

5.  **Создание суперпользователя (опционально):**
    ```bash
    docker-compose exec app python manage.py createsuperuser
    ```

6.  **Готово!**
    Проект доступен по адресу:
    * **Приложение / Swagger**: [http://localhost/swagger/](http://localhost/swagger/)
    * **ReDoc**: [http://localhost/redoc/](http://localhost/redoc/)
    * **Админка**: [http://localhost/admin/](http://localhost/admin/)

-----

## Настройка CI/CD и Деплоя на Сервер 🤖

Этот проект настроен на автоматический деплой на удаленный сервер при каждом пуше в ветку `Course_9_The_final_task`.

### Шаг 1: Подготовка Удаленного Сервера

1.  **Настройте сервер** (например, Ubuntu 22.04) с публичным IP-адресом.
2.  **Установите Docker и Docker Compose**:
    
    # Установка Docker
```bash
    sudo apt update
    sudo apt install docker.io -y
    sudo systemctl start docker
    sudo systemctl enable docker
```


# Установка Docker Compose
```bash

sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname](https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname) -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

# Добавление пользователя в группу docker

```bash
    sudo usermod -aG docker $USER
    # !!! Важно: Перезайдите на сервер, чтобы изменения вступили в силу
```
3.  **Клонируйте репозиторий** на сервер:
    ```bash
    git clone [https://github.com/AndreyStyuhin/Project_5_Habit_Tracker.git](https://github.com/AndreyStyuhin/Project_5_Habit_Tracker.git)
    cd Project_5_Habit_Tracker
    ```

### Шаг 2: Настройка GitHub Secrets

Для того чтобы GitHub Actions мог подключиться к вашему серверу и запустить деплой, ему нужны "секреты". Перейдите в **Settings > Secrets and variables > Actions** вашего репозитория на GitHub и добавьте следующие `Repository secrets`:

**1. Секреты для SSH-доступа к серверу:**
* `SERVER_HOST`: Публичный IP-адрес вашего сервера.
* `SERVER_USERNAME`: Имя пользователя на сервере (например, `ubuntu`).
* `SSH_PRIVATE_KEY`: Приватный SSH-ключ (содержимое `~/.ssh/id_rsa`), который имеет доступ к серверу.
* `SERVER_PORT`: SSH-порт (обычно `22`).

**2. Секреты для `.env` файла (конфигурация приложения):**
* `SECRET_KEY`: Ваш Django `SECRET_KEY`.
* `DEBUG`: `False` (для production).
* `ALLOWED_HOSTS`: `ваш_IP_адрес,ваш_домен`
* `POSTGRES_DB`: `habit_db`
* `POSTGRES_USER`: `habit_user`
* `POSTGRES_PASSWORD`: `ваш_супер_надежный_пароль_для_бд`
* `TELEGRAM_BOT_TOKEN`: `ВАШ:ТОКЕН_БОТА_ИЗ_BOTFATHER`

### Шаг 3: Процесс деплоя

1.  Сделайте коммит и пуш в ветку `main`.
2.  GitHub Actions автоматически запустит рабочий процесс (см. `.github/workflows/ci-cd.yml`):
    * **Lint & Test**: Запустит `flake8` и `pytest`.
    * **Build Check**: Проверит, что Docker-образ успешно собирается.
    * **Deploy**: При успехе предыдущих шагов:
        * Подключится к вашему серверу по SSH.
        * Выполнит `git pull origin main`.
        * Создаст актуальный `.env` файл из GitHub Secrets.
        * Запустит `docker-compose up -d --build` для пересборки и перезапуска сервисов.
        * Применит миграции и соберет статику.

----

## Использование API и Документация 📖

### Основные Endpoints

Для всех защищенных эндпоинтов используйте заголовок: `Authorization: Bearer <access_token>`.

| Категория | Метод | Endpoint | Описание |
| :--- | :--- | :--- | :--- |
| **Аутентификация** | `POST` | `/api/v1/token/` | Получение JWT-токенов (логин).  |
| | `POST` | `/api/v1/users/register/` | Регистрация нового пользователя. |
| **Привычки** | `GET, POST` | `/api/v1/habits/` | Список своих привычек / Создание новой.  |
| | `GET, PUT, PATCH, DELETE` | `/api/v1/habits/<id>/` | Детальные операции над привычкой.  |
| **Публичные** | `GET` | `/api/v1/habits/public/` | Список общедоступных привычек (пагинация).  |

### Документация

Вы можете взаимодействовать с API и просматривать все эндпоинты через интерактивную документацию (доступна после запуска `docker-compose up`):

  - **Swagger UI**: [http://127.0.0.1/swagger/](http://127.0.0.1/swagger/)
  - **ReDoc**: [http://127.0.0.1/redoc/](http://127.0.0.1/redoc/)


-----