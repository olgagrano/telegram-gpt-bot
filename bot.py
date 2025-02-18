import os
import telebot
import openai
import time
from flask import Flask, request
from waitress import serve  # Используем стабильный сервер

# Получаем API-ключи из переменных окружения
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Проверяем, заданы ли API-ключи
if not OPENAI_API_KEY or not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ Ошибка: Отсутствуют API-ключи. Проверьте переменные окружения.")

# Инициализация OpenAI API
openai.api_key = OPENAI_API_KEY

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
app = Flask(__name__)

# Функция для общения с OpenAI
def get_gpt_response(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Используем GPT-4o
            messages=[{"role": "user", "content": user_message}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Ошибка OpenAI: {str(e)}"

# Обработчик сообщений в Telegram
@bot.message_handler(func=lambda message: True)
def chat_with_gpt(message):
    reply = get_gpt_response(message.text)
    bot.send_message(message.chat.id, reply)

# Вебхук Flask
@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "✅", 200

# Удаляем старый вебхук
bot.remove_webhook()
time.sleep(3)  # Даем немного времени перед установкой нового вебхука

# Устанавливаем вебхук
WEBHOOK_URL = f"https://telegram-gpt-bot-xbzz.onrender.com/{TELEGRAM_BOT_TOKEN}"
bot.set_webhook(url=WEBHOOK_URL)

# Вывод в логи Render
app.logger.info(f"✅ Бот запущен! Вебхук: {WEBHOOK_URL}")

# Запуск стабильного сервера Waitress
if __name__ == "__main__":
    if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    serve(app, host="0.0.0.0", port=port)
