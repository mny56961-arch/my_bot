import os, time, json, random, threading
from flask import Flask
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

TAHFIZ = [
    "يا عسكر استمر 💪 انت ماشي صح",
    "كل يوم بيدا بقربك لحلمك 🔥",
    "ما تقيف، الاستمرارية هي السر ✨",
    "انت أقوى من الكسل 👊",
    "بيدا اليوم = نجاح بكرة 🚀"
]

app = Flask(__name__)
@app.route('/')
def home(): return "Bot Live ✅"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

threading.Thread(target=run_flask, daemon=True).start()

@bot.message_handler(commands=['start','bida'])
def start(m):
    bot.send_message(m.chat.id, f"""يا {m.from_user.first_name} مرحب بيك 🔥

 /bida - بيدا
 /tahfiz - تحفيز
 /my - رسائلي

أرسل أي شي أحفظو ليك ✅""")

@bot.message_handler(commands=['tahfiz'])
def tah(m):
    bot.send_message(m.chat.id, random.choice(TAHFIZ))

@bot.message_handler(func=lambda x: True)
def all_msg(m):
    bot.send_message(m.chat.id, f"✅ حفظت: {m.text}\n{random.choice(TAHFIZ)}")

while True:
    try:
        bot.polling(none_stop=True, timeout=60)
    except:
        time.sleep(5)
