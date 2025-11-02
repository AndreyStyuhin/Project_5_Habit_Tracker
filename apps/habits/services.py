import requests
from django.conf import settings


def send_telegram_message(chat_id, message):
    """
    Отправляет сообщение в Telegram указанному chat_id.
    Использует простой HTTP-запрос, чтобы не усложнять.
    """
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        print("Ошибка: TELEGRAM_BOT_TOKEN не задан.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()  # Вызовет исключение для плохих ответов (4xx, 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")
        return None
