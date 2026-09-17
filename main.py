import requests, telebot, json, os

BOT_TOKEN = "8854534383:AAHhSB8pzt1aMrmu7jChBU9OJN9_ItQfzFQ"
ADMIN_ID = 8554489917
API_KEY = "7f4affcc5c6cecdbf5d8e65df9d06421"
BANKAK = "401321813"
SERVICE_ID = 12634
FILE = "free_users.json"

bot = telebot.TeleBot(BOT_TOKEN)

if not os.path.exists(FILE):
    with open(FILE, 'w') as f: json.dump([], f)

def has_taken_free(uid):
    if str(uid) == str(ADMIN_ID): # انت ادمن
        return False
    try:
        with open(FILE, 'r') as f:
            data = json.load(f)
            return uid in data or str(uid) in data
    except:
        return False

def add_free_user(uid):
    if str(uid) == str(ADMIN_ID):
        return
    with open(FILE, 'r') as f:
        users = json.load(f)
    if uid not in users and str(uid) not in users:
        users.append(uid)
        with open(FILE, 'w') as f:
            json.dump(users, f)

@bot.message_handler(commands=['myid'])
def myid(m):
    bot.reply_to(m, f"الأيدي حقك: {m.from_user.id}\nرسلو لي عشان اختو كأدمن")

@bot.message_handler(commands=['reset'])
def reset(m):
    if str(m.from_user.id) == str(ADMIN_ID):
        with open(FILE, 'w') as f:
            json.dump([], f)
        bot.reply_to(m, "✅ تم تصفير كل المجان! جرب /start هسع")
    else:
        bot.reply_to(m, "انت ما الأدمن")

@bot.message_handler(commands=['start'])
def start(m):
    if not has_taken_free(m.from_user.id):
        bot.send_message(m.chat.id, f"🎉 ليك 100 مشاهدة مجان!\nارسل رابط التيك توك")
    else:
        bot.send_message(m.chat.id, f"شلت مجانك قبل كده\nالشحن 1000=1500ج بنكك {BANKAK}")

@bot.message_handler(func=lambda m: "tiktok.com" in m.text)
def handle(m):
    if has_taken_free(m.from_user.id):
        bot.reply_to(m, f"خلصت مجانك حول {BANKAK}")
        return
    data = {'key': API_KEY, 'action': 'add', 'service': SERVICE_ID, 'link': m.text.strip(), 'quantity': 100}
    r = requests.post("https://smmstone.com/api/v2", data=data).json()
    if 'order' in r:
        add_free_user(m.from_user.id)
        bot.reply_to(m, f"✅ تم 100 مجان! {r['order']}")
    else:
        bot.reply_to(m, f"❌ {r}")

bot.infinity_polling()
