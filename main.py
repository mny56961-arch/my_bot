import os, json, requests, telebot, threading
from flask import Flask

# ========== غير هنا بس ==========
BOT_TOKEN = "8854534383:AAHhSB8pzt1aMrmu7jChBU9OJN9_ItQfzFQ"
ADMIN_ID = 8554489917
# =================================

API_KEY = "7f4affcc5c6cecdbf5d8e65df9d06421"
BANKAK = "4013218-13"
SERVICE_ID = 12647
FILE = "free_users.json"

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot Live - 12647"

bot = telebot.TeleBot(BOT_TOKEN)

if not os.path.exists(FILE):
    with open(FILE, 'w') as f:
        json.dump([], f)

def has_taken(uid):
    if str(uid) == str(ADMIN_ID):
        return False
    try:
        with open(FILE, 'r') as f:
            return uid in json.load(f)
    except:
        return False

def add_user(uid):
    if str(uid) == str(ADMIN_ID):
        return
    try:
        with open(FILE, 'r') as f:
            users = json.load(f)
    except:
        users = []
    if uid not in users:
        users.append(uid)
        with open(FILE, 'w') as f:
            json.dump(users, f)

@bot.message_handler(commands=['start','myid','reset','users'])
def cmds(m):
    t = m.text.strip()
    uid = m.from_user.id
    if t == '/myid':
        bot.reply_to(m, f"ايدك: {uid}")
        return
    if t == '/reset' and str(uid) == str(ADMIN_ID):
        with open(FILE, 'w') as f:
            json.dump([], f)
        bot.reply_to(m, "✅ تم التصفير")
        return
    if t == '/users' and str(uid) == str(ADMIN_ID):
        try:
            with open(FILE, 'r') as f:
                l = len(json.load(f))
            bot.reply_to(m, f"العدد: {l}")
        except:
            bot.reply_to(m, "0")
        return
    if not has_taken(uid):
        bot.send_message(m.chat.id, f"🎉 هديتك 1000 مشاهدة مجان!\n\nارسل رابط تيك توك هسع\n\nبعد المجان بنكك: {BANKAK}")
    else:
        bot.send_message(m.chat.id, f"⚠️ شلت المجان قبل كده.\nحول بنكك {BANKAK} ورسل الاشعار.")

@bot.message_handler(func=lambda m: "tiktok.com" in m.text.lower() if m.text else False)
def link(m):
    uid = m.from_user.id
    link = m.text.strip()
    if has_taken(uid):
        bot.reply_to(m, f"❌ خلصت المجان\nحول {BANKAK}")
        return
    bot.reply_to(m, "⏳ جاري ارسال 1000 مشاهدة...")
    data = {'key': API_KEY, 'action': 'add', 'service': SERVICE_ID, 'link': link, 'quantity': 1000}
    try:
        r = requests.post("https://smmstone.com/api/v2", data=data, timeout=20).json()
        if 'order' in r:
            add_user(uid)
            bot.send_message(m.chat.id, f"✅ تم! طلبك: {r['order']}\nالمشاهدات بتصل خلال دقيقة")
        else:
            bot.send_message(m.chat.id, f"❌ فشل: {r}")
    except Exception as e:
        bot.send_message(m.chat.id, f"خطأ: {e}")

@bot.message_handler(func=lambda m: True)
def other(m):
    if not m.text.startswith('/'):
        bot.reply_to(m, "ارسل رابط tiktok.com")

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot, daemon=True).start()
app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
