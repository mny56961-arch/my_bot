import os, json, requests, telebot, threading
from flask import Flask

# ========== غير ديل بس ==========
BOT_TOKEN = "8854534383:AAHhSB8pzt1aMrmu7jChBU9OJN9_ItQfzFQ"
ADMIN_ID = 8554489917  # ايدك انت
# =================================

API_KEY = "7f4affcc5c6cecdbf5d8e65df9d06421"
BANKAK = "4013218-13"
SERVICE_ID = 12634
FILE = "free_users.json"

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Live - TikTok Bot"

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

@bot.message_handler(commands=['start', 'myid', 'reset', 'users'])
def commands(m):
    text = m.text.strip()
    uid = m.from_user.id
    
    if text == '/myid':
        bot.reply_to(m, f"ايدك هو: `{uid}`", parse_mode='Markdown')
        return
    
    if text == '/reset':
        if str(uid) == str(ADMIN_ID):
            with open(FILE, 'w') as f:
                json.dump([], f)
            bot.reply_to(m, "✅ تم تصفير كل الناس - اي زول ح ياخد 100 تاني")
        else:
            bot.reply_to(m, "انت ما الادمن")
        return

    if text == '/users':
        if str(uid) == str(ADMIN_ID):
            try:
                with open(FILE, 'r') as f:
                    users = json.load(f)
                bot.reply_to(m, f"عدد الناس الشالت مجان: {len(users)}")
            except:
                bot.reply_to(m, "0")
        return

    # /start
    if not has_taken(uid):
        bot.send_message(m.chat.id, f"🎉 مرحب بيك!\n\nليك هدية 100 متابع تيك توك مجان.\n\nارسل رابط حسابك في تيك توك هسع (لازم يكون فيه tiktok.com)\n\nبعد المجان، الشحن بي بنكك: {BANKAK}")
    else:
        bot.send_message(m.chat.id, f"⚠️ انت شلت الـ 100 المجان قبل كده.\n\nللشحن الاضافي حول بنكك:\n{BANKAK}\nو رسل الاشعار هنا.")

@bot.message_handler(func=lambda m: "tiktok.com" in m.text.lower() if m.text else False)
def tiktok_link(m):
    uid = m.from_user.id
    link = m.text.strip()

    if has_taken(uid):
        bot.reply_to(m, f"❌ انت استهلكت المجان.\nحول بنكك {BANKAK} ورسل الاشعار.")
        return

    bot.reply_to(m, "⏳ جاري ارسال 100 متابع... انتظر 10 ثواني")
    
    data = {
        'key': API_KEY,
        'action': 'add',
        'service': SERVICE_ID,
        'link': link,
        'quantity': 100
    }
    try:
        r = requests.post("https://smmstone.com/api/v2", data=data, timeout=20).json()
        if 'order' in r:
            add_user(uid)
            bot.send_message(m.chat.id, f"✅ تم بنجاح! طلبك رقم: {r['order']}\nالمتابعين ح يصلو خلال دقايق.\n\nللمرة الجاية الشحن بي {BANKAK}")
        else:
            bot.send_message(m.chat.id, f"❌ فشل: {r}\nاتأكد الرابط صحيح وجرب تاني.")
    except Exception as e:
        bot.send_message(m.chat.id, f"❌ خطأ في السيرفر: {e}")

@bot.message_handler(func=lambda m: True)
def other(m):
    if m.text and m.text.startswith('/'):
        return
    bot.reply_to(m, "ارسل رابط تيك توك فيهو tiktok.com")

# تشغيل البوت + السيرفر
def run_bot():
    print("Bot started...")
    bot.infinity_polling()

threading.Thread(target=run_bot, daemon=True).start()
app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
