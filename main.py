import os, threading, json, time
from flask import Flask
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8554489917 # <-- Change this to your Telegram ID from @userinfobot
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

SERVICES = {
    "insta_follow": {"name": "👥 Instagram Followers [Guaranteed]", "price": 3000},
    "tiktok_views": {"name": "👁️ TikTok Views", "price": 500},
    "telegram_members": {"name": "👤 Telegram Members", "price": 2000},
}

DATA_FILE = "users.json"
def load():
    return json.load(open(DATA_FILE,'r',encoding='utf-8')) if os.path.exists(DATA_FILE) else {}
def save(d):
    json.dump(d, open(DATA_FILE,'w',encoding='utf-8'), ensure_ascii=False, indent=2)

# Flask for Render
app = Flask(__name__)
@app.route('/')
def home(): return "Rashq Bot Live ✅"
threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))), daemon=True).start()

def main_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🛒 Services"), KeyboardButton("💰 My Balance"))
    kb.add(KeyboardButton("📦 New Order"), KeyboardButton("📞 Support"))
    return kb

@bot.message_handler(commands=['start'])
def start(m):
    users = load()
    uid = str(m.chat.id)
    if uid not in users:
        users[uid] = {"balance": 0, "orders": []}
        save(users)
    bot.send_message(m.chat.id, f"Welcome {m.from_user.first_name} 🔥\n\nProfessional SMM Services Bot\nYour Balance: {users[uid]['balance']} SDG\n\nChoose from menu:", reply_markup=main_kb())

@bot.message_handler(func=lambda m: m.text == "🛒 Services")
def services(m):
    text = "📋 <b>Service List:</b>\n\n"
    markup = InlineKeyboardMarkup()
    for key, s in SERVICES.items():
        text += f"{s['name']} - {s['price']} SDG / 1K\n"
        markup.add(InlineKeyboardButton(s['name'], callback_data=f"order_{key}"))
    bot.send_message(m.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "💰 My Balance")
def balance(m):
    users = load()
    b = users.get(str(m.chat.id), {}).get("balance", 0)
    bot.send_message(m.chat.id, f"💰 Your Balance: {b} SDG\n\nTo recharge contact admin: @Askar", reply_markup=main_kb())

@bot.message_handler(func=lambda m: m.text == "📦 New Order")
def new_order(m):
    bot.send_message(m.chat.id, "Send account/post link, then choose service from 🛒 Services")

@bot.callback_query_handler(func=lambda c: c.data.startswith("order_"))
def handle_order(c):
    key = c.data.replace("order_", "")
    s = SERVICES[key]
    bot.send_message(c.message.chat.id, f"✅ You selected: {s['name']}\nPrice: {s['price']}\n\nNow send link like this:\n<code>{key} https://instagram.com/username</code>")

@bot.message_handler(func=lambda m: True)
def all_text(m):
    if m.text.startswith(tuple(SERVICES.keys())):
        users = load()
        uid = str(m.chat.id)
        parts = m.text.split()
        if len(parts) < 2:
            bot.send_message(m.chat.id, "Missing link. Send: service + link")
            return
        service_key, link = parts[0], parts[1]
        order_id = f"#{int(time.time())}"
        users[uid]["orders"].append({"id": order_id, "service": service_key, "link": link, "status": "Pending"})
        save(users)
        bot.send_message(m.chat.id, f"✅ Order Received {order_id}\nService: {SERVICES[service_key]['name']}\nLink: {link}\nWill be processed in few hours")
        try: bot.send_message(ADMIN_ID, f"New Order 🔥\nFrom: {m.from_user.first_name} @{m.from_user.username}\n{service_key}\n{link}")
        except: pass
    elif m.text == "📞 Support":
        bot.send_message(m.chat.id, "Contact Admin: @Askar")
    else:
        if m.text not in ["📞 Support", "🛒 Services", "💰 My Balance", "📦 New Order"]:
            bot.send_message(m.chat.id, "Choose from menu below 👇", reply_markup=main_kb())

while True:
    try: bot.polling(none_stop=True, timeout=60)
    except: time.sleep(5)
