import requests, telebot, json, os

API_KEY = "7f4affcc5c6cecdbf5d8e65df9d06421"
BOT_TOKEN = os.getenv("BOT_TOKEN")
BANKAK = "401321813"

bot = telebot.TeleBot(8854534383:AAHhSB8pzt1aMrmu7jChBU9OJN9_ItQfzFQ)
SERVICE_ID = 12634

# ملف يحفظ الناس الشالت مجان عشان ما تشيل تاني
FILE = "free_users.json"
if not os.path.exists(FILE):
    with open(FILE, 'w') as f: json.dump([], f)

def has_taken_free(user_id):
    with open(FILE, 'r') as f:
        users = json.load(f)
    return user_id in users

def add_free_user(user_id):
    with open(FILE, 'r') as f:
        users = json.load(f)
    users.append(user_id)
    with open(FILE, 'w') as f:
        json.dump(users, f)

@bot.message_handler(commands=['start'])
def start(m):
    if not has_taken_free(m.from_user.id):
        bot.send_message(m.chat.id, f"""
🎉 ليك 100 مشاهدة مجاان هدية!

ارسل رابط فيديو التيك توك هسع
مثال:
https://vt.tiktok.com/ZSj...

⚠️ المجان مرة واحدة بس لكل زول
بعدها الشحن:
1000 = 1500ج على بنكك {BANKAK}
""")
    else:
        bot.send_message(m.chat.id, f"""
انت شلت المجان قبل كده 😅

هسع الشحن بقروش:
1000 مشاهدة = 1500ج
حول بنكك: {BANKAK}
ورسل الاشعار + الرابط
""")

@bot.message_handler(func=lambda m: "tiktok.com" in m.text)
def handle_link(m):
    user_id = m.from_user.id
    
    # لو ما شال مجان قبل كده
    if not has_taken_free(user_id):
        link = m.text.strip()
        data = {
            'key': API_KEY,
            'action': 'add',
            'service': SERVICE_ID,
            'link': link,
            'quantity': 100
        }
        r = requests.post("https://smmstone.com/api/v2", data=data).json()
        if 'order' in r:
            add_free_user(user_id)
            bot.reply_to(m, f"✅ تم! 100 مشاهدة مجان اترسلت\nرقم طلبك: {r['order']}\n\nعجبتك الخدمة؟ اشحن تاني على {BANKAK}")
        else:
            bot.reply_to(m, f"❌ خطأ: {r}")
    else:
        bot.reply_to(m, f"انت استخدمت المجان قبل كده\nحول 1500ج على {BANKAK} لـ 1000 مشاهدة")

bot.infinity_polling()
