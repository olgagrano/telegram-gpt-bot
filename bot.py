import os
import telebot
import openai
from flask import Flask, request
from waitress import serve  # Используем стабильный сервер

# Получаем API-ключи из переменных окружения
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Проверяем, заданы ли API-ключи
if not OPENAI_API_KEY or not TELEGRAM_BOT_TOKEN:
    raise ValueError("Отсутствуют API-ключи. Проверьте переменные окружения.")

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
app = Flask(__name__)

# Функция для общения с OpenAI
def get_gpt_response(user_message):
    try:
        client = openai.OpenAI()  # Создаём новый клиент OpenAI
        import openai

client = openai.OpenAI(api_key="ТВОЙ_API_КЛЮЧ")

response = client.chat.completions.create(
    model="gpt-4o",  # Или gpt-3.5-turbo
    messages=[{"role": "user", "content": "Привет, как дела?"}]
)
            model="gpt-4o",
            messages=[{"role": "user", "content": user_message}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка OpenAI: {str(e)}"

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
    return "!", 200

# Устанавливаем вебхук
bot.remove_webhook()
bot.set_webhook(url=f"https://telegram-gpt-bot-xbzz.onrender.com/{TELEGRAM_BOT_TOKEN}")

print("Бот запущен!".encode('utf-8').decode('utf-8'))

# Запуск стабильного сервера Waitress
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
