import requests, telebot, json, os

# غير التوكن هنا بس
BOT_TOKEN = "8854534383:AAHhSB8pzt1aMrmu7jChBU9OJN9_ItQfzFQ"

ADMIN_ID = 8554489917  # أيديك انت - مجان مفتوح ليك
API_KEY = "7f4affcc5c6cecdbf5d8e65df9d06421"
BANKAK = "401321813"
SERVICE_ID = 12634
FILE = "free_users.json"

bot = telebot.TeleBot(BOT_TOKEN)

if not os.path.exists(FILE):
    with open(FILE, 'w') as f:
        json.dump([], f)

def has_taken_free(uid):
    if uid == ADMIN_ID:
        return False
    try:
        with open(FILE, 'r') as f:
            return uid in json.load(f)
    except:
        return False

def add_free_user(uid):
    if uid == ADMIN_ID:
        return
    with open(FILE, 'r') as f:
        users = json.load(f)
    if uid not in users:
        users.append(uid)
        with open(FILE, 'w') as f:
            json.dump(users, f)

@bot.message_handler(commands=['start'])
def start(m):
    if m.from_user.id == ADMIN_ID:
        bot.send_message(m.chat.id, f"👑 مرحب يا صاحب البوت!\nانت الأدمن - عندك تجربة مفتوحة\nالرصيد المجاني: 1000 مقسمة 100 لكل زبون\nبنكك للدفع: {BANKAK}")
    elif not has_taken_free(m.from_user.id):
        bot.send_message(m.chat.id, f"🎉 ليك 100 مشاهدة مجان هدية!\nارسل رابط التيك توك هسع\nبعدها الشحن بنكك {BANKAK}")
    else:
        bot.send_message(m.chat.id, f"شلت مجانك قبل كده 😅\nالشحن 1000=1500ج\nبنكك: {BANKAK}")

@bot.message_handler(func=lambda m: "tiktok.com" in m.text)
def handle(m):
    if has_taken_free(m.from_user.id):
        bot.reply_to(m, f"خلصت مجانك حول على {BANKAK}")
        return

    data = {'key': API_KEY, 'action': 'add', 'service': SERVICE_ID, 'link': m.text.strip(), 'quantity': 100}
    r = requests.post("https://smmstone.com/api/v2", data=data).json()
    if 'order' in r:
        add_free_user(m.from_user.id)
        bot.reply_to(m, f"✅ تم 100 مجان!\nالطلب: {r['order']}\nلو داير تاني حول {BANKAK}")
    else:
        bot.reply_to(m, f"❌ خطأ: {r}")

bot.infinity_polling()
