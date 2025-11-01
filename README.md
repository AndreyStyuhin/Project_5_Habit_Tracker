

# Project 5: Habit Tracker: Backend 🚀

## Описание

[cite_start]**Habit Tracker** — это мощное **backend-приложение** для отслеживания и управления привычками, построенное на **Django** и **Django REST Framework**[cite: 109]. [cite_start]Приложение реализует полноценный **REST API**, который обеспечивает создание, управление и валидацию привычек, а также отправку **асинхронных напоминаний** через **Telegram-бот** с помощью **Celery** и **Redis**[cite: 109]. [cite_start]Проект разработан с учетом требований к современным API: использует **JWT-аутентификацию** [cite: 110][cite_start], имеет полную **документацию (Swagger/ReDoc)** [cite: 110] [cite_start]и покрыт **юнит-тестами** (pytest)[cite: 110].


| **Ключевые особенности**          | **Валидация привычек**                                                                        |
| :-------------------------------- | :-------------------------------------------------------------------------------------------- |
| 🛡️ JWT-аутентификация            | [cite_start]⏱️ Длительность выполнения: **$\le 120$ секунд** [cite: 112]                      |
| 🔔 Telegram-напоминания (Celery)  | [cite_start]🗓️ Периодичность: **$\ge 1$ раза в 7 дней** [cite: 113]                          |
| 🐳 Контейнеризация (Docker/Nginx) | [cite_start]🤝 Исключение конфликта вознаграждения и связанной привычки [cite: 114]           |
| 🔄 CI/CD (GitHub Actions)         | [cite_start]🚫 Ограничения для "приятных" привычек (нет вознаграждения/связанной) [cite: 115] |

**Адрес развернутого приложения (Production):**
> [cite_start]http://212.22.70.98/ [cite: 161]

-----

## Используемые технологии 🛠️

| Категория           | Технология                                    | Описание                                                                              |
| :------------------ | :-------------------------------------------- | :------------------------------------------------------------------------------------ |
| **Основной стек**   | **Python 3.11**, **Django 5.x**, **DRF**      | [cite_start]Язык программирования и фреймворки для создания API. [cite: 123]          |
| **Контейнеризация** | **Docker**, **Docker Compose**, **Nginx**     | Контейнеризация сервисов (App, DB, Redis, Celery, Nginx).                             |
| **Аутентификация**  | **djangorestframework-simplejwt**             | [cite_start]Реализация JWT-токенов. [cite: 124]                                       |
| **База данных**     | **PostgreSQL**                                | [cite_start]Реляционная БД для production-окружения. [cite: 125]                      |
| **Асинхронность**   | **Celery**, **Redis**, **django-celery-beat** | [cite_start]Брокер сообщений, бэкенд и планировщик для асинхронных задач. [cite: 126] |
| **CI/CD**           | **GitHub Actions**                            | Автоматическое тестирование, сборка и деплой проекта.                                 |
| **Документация**    | **drf-yasg** (Swagger/ReDoc)                  | [cite_start]Генерация интерактивной документации API. [cite: 127]                     |
| **Тестирование**    | **pytest-django**, **pytest-cov**             | [cite_start]Юнит-тестирование с целью покрытия $\ge 80\%$. [cite: 128]                |

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
    [cite_start]Вам нужно **обязательно** заполнить `SECRET_KEY` и `TELEGRAM_BOT_TOKEN` в файле `.env`[cite: 132]. Остальные (Postgres, Redis) уже настроены для Docker.

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
    * [cite_start]**Приложение / Swagger**: [http://localhost/swagger/](http://localhost/swagger/) [cite: 140]
    * [cite_start]**ReDoc**: [http://localhost/redoc/](http://localhost/redoc/) [cite: 140]
    * **Админка**: [http://localhost/admin/](http://localhost/admin/)

-----

## Настройка CI/CD и Деплоя на Сервер 🤖

[cite_start]Этот проект настроен на автоматический деплой на удаленный сервер при каждом пуше в ветку `main`[cite: 153, 162].

### Шаг 1: Подготовка Удаленного Сервера

1.  **Настройте сервер** (например, Ubuntu 22.04) с публичным IP-адресом.
2.  [cite_start]**Установите Docker и Docker Compose**[cite: 152]:
    
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
    * [cite_start]**Lint & Test**: Запустит `flake8` и `pytest`[cite: 157].
    * [cite_start]**Build Check**: Проверит, что Docker-образ успешно собирается[cite: 157].
    * **Deploy**: При успехе предыдущих шагов:
        * [cite_start]Подключится к вашему серверу по SSH[cite: 158].
        * Выполнит `git pull origin main`.
        * Создаст актуальный `.env` файл из GitHub Secrets.
        * [cite_start]Запустит `docker-compose up -d --build` для пересборки и перезапуска сервисов[cite: 159].
        * Применит миграции и соберет статику.

-----

## Использование API и Документация 📖

### Основные Endpoints

Для всех защищенных эндпоинтов используйте заголовок: `Authorization: Bearer <access_token>`.

| Категория | Метод | Endpoint | Описание |
| :--- | :--- | :--- | :--- |
| **Аутентификация** | `POST` | `/api/v1/token/` | [cite_start]Получение JWT-токенов (логин). [cite: 137] |
| | `POST` | `/api/v1/users/register/` | Регистрация нового пользователя. |
| **Привычки** | `GET, POST` | `/api/v1/habits/` | [cite_start]Список своих привычек / Создание новой. [cite: 138] |
| | `GET, PUT, PATCH, DELETE` | `/api/v1/habits/<id>/` | [cite_start]Детальные операции над привычкой. [cite: 139] |
| **Публичные** | `GET` | `/api/v1/habits/public/` | [cite_start]Список общедоступных привычек (пагинация). [cite: 140] |

### Документация

Вы можете взаимодействовать с API и просматривать все эндпоинты через интерактивную документацию (доступна после запуска `docker-compose up`):

  - **Swagger UI**: [http://127.0.0.1/swagger/](http://127.0.0.1/swagger/)
  - **ReDoc**: [http://127.0.0.1/redoc/](http://127.0.0.1/redoc/)


-----