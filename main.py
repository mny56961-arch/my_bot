import telebot
from telebot import types
import requests

BOT_TOKEN = "8854534383:AAHhSB8pzt1aMrmu7jChBU9OJN9_ItQfzFQ"
ADMIN_ID = 8554489917
MY_CASHI_NUMBER = "401321813"
SMM_API_URL = "https://smmstone.com/api/v2"
SMM_API_KEY = "2ffae4f4348a6719f0208a37f01f353b"

bot = telebot.TeleBot(BOT_TOKEN)
user_balances = {}

@bot.message_handler(commands=['start'])
def start(m):
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mk.add("💳 شحن عبر ماي كاشي", "🛒 طلب متابعين")
    mk.add("💰 رصيدي")
    bot.send_message(m.chat.id, f"🔥 متجر الرشق\n\n📱 شحن ماي كاشي: {MY_CASHI_NUMBER}\n💰 رصيدك: {user_balances.get(m.chat.id,0)} جنيه", reply_markup=mk)

@bot.message_handler(func=lambda m: m.text == "💳 شحن عبر ماي كاشي")
def charge(m):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("5000ج = 1000 متابع", callback_data="charge_5000"))
    kb.add(types.InlineKeyboardButton("10000ج = 2500 متابع", callback_data="charge_10000"))
    kb.add(types.InlineKeyboardButton("20000ج = 6000 متابع", callback_data="charge_20000"))
    bot.send_message(m.chat.id, f"حول على {MY_CASHI_NUMBER} ورسل صورة الاشعار", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("charge_"))
def charge_cb(c):
    amount = c.data.split("_")[1]
    bot.send_message(c.message.chat.id, f"تمام حول {amount} على {MY_CASHI_NUMBER} ورسل صورة الاشعار هنا 👇")
    bot.register_next_step_handler(c.message, lambda msg: wait_screenshot(msg, amount))

def wait_screenshot(m, amount):
    if m.content_type == 'photo':
        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton(f"✅ تأكيد {amount}", callback_data=f"confirm_{m.chat.id}_{amount}"),
            types.InlineKeyboardButton("❌ رفض", callback_data=f"reject_{m.chat.id}")
        )
        bot.send_message(ADMIN_ID, f"🔔 طلب شحن {amount} من {m.chat.id}")
        bot.forward_message(ADMIN_ID, m.chat.id, m.message_id)
        bot.send_message(ADMIN_ID, "أكد بعد ما تشوف MyCashi", reply_markup=kb)
        bot.send_message(m.chat.id, "⏳ انتظر التأكيد")
    else:
        bot.send_message(m.chat.id, "رسل صورة بس")

@bot.callback_query_handler(func=lambda c: c.data.startswith("confirm_"))
def confirm(c):
    _, uid, amt = c.data.split("_")
    uid=int(uid); amt=int(amt)
    user_balances[uid] = user_balances.get(uid,0)+amt
    bot.send_message(uid, f"✅ تم شحن {amt}ج - رصيدك {user_balances[uid]}")
    bot.edit_message_text(f"تم ✅ {amt} للعميل {uid}", c.message.chat.id, c.message.message_id)

@bot.message_handler(func=lambda m: m.text == "🛒 طلب متابعين")
def order(m):
    bot.send_message(m.chat.id, "رسل رابط حسابك")
    bot.register_next_step_handler(m, get_link)

def get_link(m):
    link=m.text
    bot.send_message(m.chat.id, "كم العدد؟ 1000 - 10000")
    bot.register_next_step_handler(m, lambda msg: do_order(msg, link))

def do_order(m, link):
    qty=int(m.text)
    bal=user_balances.get(m.chat.id,0)
    cost = qty*5 # 5 جنيه للمتابع مثلا
    if bal < cost:
        bot.send_message(m.chat.id, f"رصيدك ما بكفي،
