import os
import time
import telebot
from flask import Flask
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Alive!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask).start()

@bot.message_handler(commands=['start','bida'])
def start(m):
    bot.send_message(m.chat.id, f"يا {m.from_user.first_name} البوت شغال ✅")

@bot.message_handler(func=lambda m: True)
def all_msg(m):
    bot.send_message(m.chat.id, f"احفظت: {m.text}")

while True:
    try:
        bot.polling(none_stop=True, timeout=60)
    except:
        time.sleep(5)
