from celery import shared_task
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Habit
from .services import send_telegram_message


@shared_task
def send_habit_reminders():
    """
    Периодическая задача Celery.
    Отправляет напоминания о привычках пользователям в Telegram.
    """
    print("Запуск задачи send_habit_reminders...")

    # Получаем текущее время с учетом часового пояса
    now = timezone.now()
    current_time = now.time()
    today = now.date()

    # Ищем привычки, которые должны выполниться *примерно* в эту минуту
    # (минута в минуту) и не являются приятными
    habits_to_send = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute,
        is_pleasant=False
    ).select_related('user')

    print(f"Найдено {habits_to_send.count()} привычек для проверки.")

    for habit in habits_to_send:
        user = habit.user
        if not user or not user.telegram_id:
            print(f"У привычки {habit.id} нет пользователя или telegram_id.")
            continue

        # Проверяем периодичность
        needs_sending = False
        if habit.last_sent_time is None:
            # Если никогда не отправляли
            needs_sending = True
        else:
            # Если отправляли, проверяем, прошло ли достаточно дней
            days_since_last_sent = (today - habit.last_sent_time.date()).days
            if days_since_last_sent >= habit.periodicity:
                needs_sending = True

        if needs_sending:
            message = (
                f"🔔 *Напоминание о привычке!*\n\n"
                f"Пора выполнить: *{habit.action}*\n"
                f"Где: *{habit.place}*\n"
                f"Время на выполнение: *{habit.duration} сек.*\n\n"
            )

            if habit.reward:
                message += f"🏆 Вознаграждение: *{habit.reward}*"
            elif habit.related_habit:
                message += f"🧘 Связанная приятная привычка: *{habit.related_habit.action}*"

            print(f"Отправка сообщения пользователю {user.telegram_id} для привычки {habit.id}")
            send_telegram_message(user.telegram_id, message)

            # Обновляем время последней отправки
            habit.last_sent_time = now
            habit.save(update_fields=['last_sent_time'])
        else:
            print(f"Привычка {habit.id} сегодня уже отправлялась или еще не время.")

    return f"Задача выполнена. Обработано {habits_to_send.count()} привычек."