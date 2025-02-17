import telebot
import openai
import os

# Получаем API-ключи из переменных окружения
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def get_gpt_response(user_message):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}]
    )
    return response["choices"][0]["message"]["content"]

@bot.message_handler(func=lambda message: True)
def chat_with_gpt(message):
    try:
        reply = get_gpt_response(message.text)
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка: " + str(e))

print("Бот запущен!")
from flask import Flask, request
import telebot
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
app = Flask(__name__)

@app.route("/" + TELEGRAM_BOT_TOKEN, methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

bot.remove_webhook()
bot.set_webhook(url="https://telegram-gpt-bot-xbzz.onrender.com" + TELEGRAM_BOT_TOKEN)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
