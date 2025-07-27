import os

import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def send_telegram_message(telegtam_chat_id, text):
    """Отправляет сообщение в Telegram через Bot API. Принимает telegram-ID и сообщение."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": telegtam_chat_id,
        "text": text,
    }
    response = requests.post(url, data=data)
    return response.json()
