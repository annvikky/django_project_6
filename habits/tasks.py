import os

import requests
from celery import shared_task
from django.utils.timezone import now

from .models import Habit

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


@shared_task
def send_habit_reminders():
    current_time = now().time()
    habits = Habit.objects.filter(
        time__hour=current_time.hour, time__minute=current_time.minute
    )
    for habit in habits:
        user = habit.user
        if user.telegram_chat_id:
            text = f"Напоминание: {habit.action} в {habit.place}"
            requests.post(
                TELEGRAM_API_URL.format(token=BOT_TOKEN),
                data={
                    "chat_id": user.telegram_chat_id,
                    "text": text,
                },
            )


@shared_task
def send_test_message(chat_id):
    """Проверка отправки сообщения. Но боту пишем первыми, бот сам не может начинать диалог."""
    data = {"chat_id": chat_id, "text": "👋 Привет! Это тестовое сообщение от Celery."}
    try:
        response = requests.post(TELEGRAM_API_URL, data=data)
        print(f"[Telegram response] Status: {response.status_code}")
        print(f"[Telegram response] Body: {response.text}")
    except Exception as e:
        print(f"[Telegram ERROR]: {e}")
