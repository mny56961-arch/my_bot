import telebot, os, time, threading, requests
from flask import Flask
from telebot import types

BOT_TOKEN = "8854534383:AAHhSB8pzt1aMrmu7jChBU9OJN9_ItQfzFQ"
ADMIN_ID = 8554489917
MY_CASHI = "401321813"
SMM_KEY = "2ffae4f4348a6719f0208a37f01f353b"
SMM_URL = "https://smmstone.com/api/v2"

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)
balances = {}

@app.route('/')
def home(): return "Bot is Alive!"

@bot.message_handler(commands=['start'])
def start(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("💳 شحن ماي كاشي", "🛒 طلب متابعين")
    kb.add("💰 رصيدي")
    bot.send_message(m.chat.id, f"🔥 متجر الرشق\n\n💳 ماي كاشي: {MY_CASHI}\n💰 رصيدك: {balances.get(m.chat.id,0)}ج", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text=="💳 شحن ماي كاشي")
def charge_info(m):
    bot.send_message(m.chat.id, f"حول على: {MY_CASHI}\nوبعدها رسل صورة الاشعار هنا 👇")

@bot.message_handler(func=lambda m: m.text=="💰 رصيدي")
def my_bal(m):
    bot.send_message(m.chat.id, f"💰 رصيدك: {balances.get(m.chat.id,0)}ج")

@bot.message_handler(func=lambda m: m.text=="🛒 طلب متابعين")
def order_start(m):
    if balances.get(m.chat.id,0) < 100:
        bot.send_message(m.chat.id, "❌ رصيدك ما كافي، اشحن اول")
        return
    bot.send_message(m.chat.id, "📎 رسل رابط حسابك")
    bot.register_next_step_handler(m, get_link)

def get_link(m):
    link = m.text
    bot.send_message(m.chat.id, "🔢 كم متابع داير؟ مثلا 1000")
    bot.register_next_step_handler(m, lambda msg: do_order(msg, link))

def do_order(m, link):
    try:
        qty = int(m.text)
        balances[m.chat.id] = balances.get(m.chat.id,0) - 5000
        bot.send_message(m.chat.id, f"✅ تم استلام طلبك\n{qty} متابع لـ {link}\nسيتم التنفيذ قريبا")
        bot.send_message(ADMIN_ID, f"طلب جديد من {m.chat.id}\n{qty} لـ {link}")
    except:
        bot.send_message(m.chat.id, "اكتب رقم صحيح")

@bot.message_handler(content_types=['photo'])
def photo(m):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("✅ تأكيد 5000", callback_data=f"ok_{m.chat.id}_5000"),
            types.InlineKeyboardButton("❌ رفض", callback_data=f"no_{m.chat.id}"))
    bot.send_message(ADMIN_ID, f"🔔 شحن من {m.chat.id}")
    bot.forward_message(ADMIN_ID, m.chat.id, m.message_id)
    bot.send_message(ADMIN_ID, "تأكيد؟", reply_markup=kb)
    bot.send_message(m.chat.id, "⏳ انتظر تأكيد الادمن")

@bot.callback_query_handler(func=lambda c: c.data.startswith("ok_"))
def confirm(c):
    _, uid, amt = c.data.split("_")
    uid=int(uid); amt=int(amt)
    balances[uid]=balances.get(uid,0)+amt
    bot.send_message(uid, f"✅ تم شحن {amt}ج\nرصيدك: {balances[uid]}ج")
    bot.edit_message_text(f"تم ✅ {amt} للعميل {uid}", c.message.chat.id, c.message.message_id)

def run_bot():
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(e); time.sleep(5)

threading.Thread(target=run_bot, daemon=True).start()
if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
