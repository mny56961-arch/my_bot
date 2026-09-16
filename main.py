import telebot, os, threading
from flask import Flask

BOT_TOKEN = "8854534383:AAHhSB8pzt1aMrmu7jChBU9OJN9_ItQfzFQ"
ADMIN_ID = 8554489917

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)
user_balances = {}

@app.route('/')
def home():
    return "Bot is running!"

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, f"🔥 البوت شغال\nرصيدك: {user_balances.get(m.chat.id,0)}")

@bot.message_handler(content_types=['photo'])
def photo(m):
    bot.send_message(ADMIN_ID, f"طلب شحن من {m.chat.id}")
    bot.forward_message(ADMIN_ID, m.chat.id, m.message_id)
    bot.send_message(m.chat.id, "⏳ انتظر التأكيد")

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
