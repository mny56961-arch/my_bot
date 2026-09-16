import os, time, telebot
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, f"البوت شغال ✅ يا {m.from_user.first_name}")
@bot.message_handler(func=lambda m: True)
def all_msg(m):
    bot.send_message(m.chat.id, f"استلمت: {m.text}")
while True:
    try:
        bot.polling(none_stop=True, timeout=60)
    except:
        time.sleep(5)
