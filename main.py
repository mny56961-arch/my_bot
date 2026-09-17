import os, json, requests, telebot, threading
from flask import Flask

BOT_TOKEN = "8854534383:AAHhSB8pzt1aMrmu7jChBU9OJN9_ItQfzFQ"
ADMIN_ID = 8554489917
API_KEY = "7f4affcc5c6cecdbf5d8e65df9d06421"
SERVICE_ID = 12647  # TikTok Views [HQ]
FILE = "free_users.json"
MAX_FREE = 10

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot Live - 10 Free Only"

bot = telebot.TeleBot(BOT_TOKEN)

if not os.path.exists(FILE):
    with open(FILE, 'w') as f:
        json.dump([], f)

def get_users():
    try:
        with open(FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def has_taken(uid):
    if str(uid) == str(ADMIN_ID):
        return False
    return uid in get_users()

def add_user(uid):
    if str(uid) == str(ADMIN_ID):
        return
    users = get_users()
    if uid not in users:
        users.append(uid)
        with open(FILE, 'w') as f:
            json.dump(users, f)

@bot.message_handler(commands=['start','reset','users','myid'])
def cmds(m):
    uid = m.from_user.id
    t = m.text.strip()
    users = get_users()
    
    if t == '/myid':
        bot.reply_to(m, f"{uid}")
        return
    if t == '/reset' and str(uid) == str(ADMIN_ID):
        with open(FILE, 'w') as f:
            json.dump([], f)
        bot.reply_to(m, "✅ تم تصفير المجان - تاني 10 اشخاص يقدرو")
        return
    if t == '/users' and str(uid) == str(ADMIN_ID):
        bot.reply_to(m, f"شالو المجان: {len(users)}/10\n{users}")
        return

    # /start
    left = MAX_FREE - len(users)
    if left <= 0:
        bot.send_message(m.chat.id, "❌ عفوا انتهى العرض المجاني\nالـ 10 اشخاص الاوائل شالو الـ 100\n\nح تفتح تاني قريب.")
        return
    
    if not has_taken(uid):
        bot.send_message(m.chat.id, f"🎉 مرحب بيك!\n\nباقي {left} اشخاص بس للمجان\n\nليك 100 مشاهدة تيك توك مجان - ارسل رابط الفيديو هسع (فيهو tiktok.com)")
    else:
        bot.send_message(m.chat.id, "⚠️ انت شلت الـ 100 المجان قبل كده\nتاني ما بتقدر - العرض لـ 10 اشخاص بس.")

@bot.message_handler(func=lambda m: "tiktok.com" in m.text.lower() if m.text else False)
def link(m):
    uid = m.from_user.id
    users = get_users()
    
    if len(users) >= MAX_FREE and uid not in users and str(uid) != str(ADMIN_ID):
        bot.reply_to(m, "❌ انتهى المجان - 10 اشخاص شالو قبلك")
        return

    if has_taken(uid):
        bot.reply_to(m, "❌ انت شلتو قبل كده")
        return

    if len(users) >= MAX_FREE:
        bot.reply_to(m, "❌ خلص - 10/10")
        return

    bot.reply_to(m, f"⏳ جاري ارسال 100 مشاهدة... باقي ليك {MAX_FREE - len(users) - 1} اشخاص بعدك")
    
    data = {'key': API_KEY, 'action': 'add', 'service': SERVICE_ID, 'link': m.text.strip(), 'quantity': 100}
    try:
        r = requests.post("https://smmstone.com/api/v2", data=data, timeout=20).json()
        if 'order' in r:
            add_user(uid)
            left = MAX_FREE - len(get_users())
            bot.send_message(m.chat.id, f"✅ تم ارسال 100 مشاهدة!\nرقم الطلب: {r['order']}\n\nباقي {left} اشخاص للمجان")
        else:
            bot.send_message(m.chat.id, f"❌ فشل: {r}")
    except Exception as e:
        bot.send_message(m.chat.id, f"خطأ: {e}")

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot, daemon=True).start()
app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
