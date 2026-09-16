import telebot, os, threading, requests
from flask import Flask
from telebot import types

BOT_TOKEN = "8854534383:AAHhSB8pzt1aMrmu7jChBU9OJN9_ItQfzFQ"
ADMIN_ID = 8554489917
MY_CASHI = "401321813"
SMM_KEY = "2ffae4f4348a6719f0208a37f01f353b"
SMM_URL = "https://smmstone.com/api/v2"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)
balances = {}

@app.route('/')
def home(): return "Bot running"

@bot.message_handler(commands=['start'])
def start(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("💳 شحن ماي كاشي", "🛒 طلب متابعين")
    kb.add("💰 رصيدي", "📞 تواصل")
    bot.send_message(m.chat.id, f"🔥 مرحبا بيك في متجر الرشق\n\n💳 شحن: {MY_CASHI}\n💰 رصيدك: {balances.get(m.chat.id,0)}ج", reply_markup=kb)

@bot.message_handler(func=lambda x: x.text=="💳 شحن ماي كاشي")
def charge(m):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("5000ج = 1000 متابع", callback_data="c_5000"))
    kb.add(types.InlineKeyboardButton("10000ج = 2500 متابع", callback_data="c_10000"))
    kb.add(types.InlineKeyboardButton("20000ج = 6000 متابع", callback_data="c_20000"))
    bot.send_message(m.chat.id, f"حول على ماي كاشي:\n{MY_CASHI}\n\nبعد تحول رسل صورة الاشعار 👇", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("c_"))
def c_cb(c):
    amt = c.data.split("_")[1]
    bot.send_message(c.message.chat.id, f"تمام حول {amt}ج على {MY_CASHI} ورسل صورة الاشعار هنا")

@bot.message_handler(content_types=['photo'])
def photo(m):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("✅ تأكيد الشحن", callback_data=f"ok_{m.chat.id}_5000"),
            types.InlineKeyboardButton("❌ رفض", callback_data=f"no_{m.chat.id}"))
    bot.send_message(ADMIN_ID, f"🔔 طلب شحن جديد من ID: {m.chat.id}")
    bot.forward_message(ADMIN_ID, m.chat.id, m.message_id)
    bot.send_message(ADMIN_ID, "هل تم التحويل في ماي كاشي؟", reply_markup=kb)
    bot.send_message(m.chat.id, "⏳ تم استلام الاشعار، انتظر تأكيد الادمن")

@bot.callback_query_handler(func=lambda c: c.data.startswith("ok_"))
def ok(c):
    _, uid, amt = c.data.split("_")
    uid=int(uid); amt=int(amt)
    balances[uid]=balances.get(uid,0)+amt
    bot.send_message(uid, f"✅ تم شحن {amt}ج\nرصيدك الحالي: {balances[uid]}ج")
    bot.edit_message_text(f"تم الشحن ✅ {amt} للعميل {uid}", c.message.chat.id, c.message.message_id)

@bot.message_handler(func=lambda x: x.text=="💰 رصيدي")
def bal(m):
    bot.send_message(m.chat.id, f"💰 رصيدك: {balances.get(m.chat.id,0)}ج")

def run_bot(): bot.infinity_polling()
threading.Thread(target=run_bot).start()
if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
