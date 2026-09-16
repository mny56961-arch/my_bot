# bot.py - بوت شحن العاب + رشق - ماي كاشي فقط
import telebot
from telebot import types
import sqlite3

BOT_TOKEN = "8854534383:AAHhSB8pzt1aMrmu7jChBU9OJN9_ItQfzFQ"
ADMIN_ID = 8554489917
MYCASH_NUM = "401321813" # رقم ماي كاشي بس

bot = telebot.TeleBot(BOT_TOKEN)

# --- قاعدة البيانات ---
conn = sqlite3.connect('store.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, balance INTEGER DEFAULT 0)''')
c.execute('''CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, service TEXT, player_id TEXT, status TEXT)''')
conn.commit()

def get_balance(uid):
    c.execute("SELECT balance FROM users WHERE id=?", (uid,))
    r = c.fetchone()
    if not r:
        c.execute("INSERT INTO users (id, balance) VALUES (?,0)", (uid,))
        conn.commit()
        return 0
    return r[0]

# --- الخدمات ---
SERVICES = {
    "ff_100": {"name": "💎 100 جوهرة - FF", "price": 3000, "cost": 1500},
    "ff_310": {"name": "💎 310 جوهرة - FF", "price": 6500, "cost": 3500},
    "ff_520": {"name": "💎 520 جوهرة - FF", "price": 10500, "cost": 6500},
    "ff_1060": {"name": "💎 1060 جوهرة - FF", "price": 19500, "cost": 12000},
    "pubg_60": {"name": "🎮 60 شدة - PUBG", "price": 3500, "cost": 2000},
    "pubg_325": {"name": "🎮 325 شدة - PUBG", "price": 13500, "cost": 8500},
    "pubg_660": {"name": "🎮 660 شدة - PUBG", "price": 26000, "cost": 16500},
    "ml_86": {"name": "🐉 86 جوهرة - ML", "price": 4000, "cost": 2200},
    "ml_172": {"name": "🐉 172 جوهرة - ML", "price": 7500, "cost": 4500},
    "ml_344": {"name": "🐉 344 جوهرة - ML", "price": 14500, "cost": 9000},
    "insta_1k": {"name": "📸 1000 متابع انستا", "price": 5000, "cost": 800},
    "tiktok_10k": {"name": "🎵 10K مشاهدة تيك توك", "price": 3000, "cost": 300},
    "yt_1k": {"name": "▶️ 1000 مشترك يوتيوب", "price": 15000, "cost": 6000},
}

@bot.message_handler(commands=['start'])
def start(m):
    bal = get_balance(m.chat.id)
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(
        types.InlineKeyboardButton("💎 فري فاير", callback_data="cat_ff"),
        types.InlineKeyboardButton("🎮 ببجي", callback_data="cat_pubg"),
        types.InlineKeyboardButton("🐉 MLBB", callback_data="cat_ml"),
        types.InlineKeyboardButton("🚀 رشق", callback_data="cat_smm"),
    )
    mk.add(
        types.InlineKeyboardButton(f"💰 رصيدك: {bal}ج", callback_data="balance"),
        types.InlineKeyboardButton("💳 شحن رصيد", callback_data="charge"),
    )
    bot.send_message(m.chat.id, f"🔥 متجر السودان الشامل 🔥\n\nأهلا {m.from_user.first_name}!\nرصيدك: {bal}ج\n\n👇 اختار القسم:", reply_markup=mk)

@bot.callback_query_handler(func=lambda x: x.data.startswith("cat_"))
def cats(call):
    cat = call.data.split("_")[1]
    mk = types.InlineKeyboardMarkup(row_width=1)
    for key, val in SERVICES.items():
        if cat in key or (cat=="smm" and key.startswith(("insta","tiktok","yt"))):
            mk.add(types.InlineKeyboardButton(f"{val['name']} - {val['price']}ج", callback_data=f"buy_{key}"))
    mk.add(types.InlineKeyboardButton("⬅️ رجوع", callback_data="back_home"))
    bot.edit_message_text("اختر الخدمة:", call.message.chat.id, call.message.message_id, reply_markup=mk)

@bot.callback_query_handler(func=lambda x: x.data == "back_home")
def back_home(call):
    start(call.message)

@bot.callback_query_handler(func=lambda x: x.data == "charge")
def charge(call):
    bot.send_message(call.message.chat.id, f"""
💳 **شحن الرصيد - ماي كاشي**

حول في:
`{MYCASH_NUM}`
ماي كاشي

بعد التحويل رسل صورة الاشعار هنا 👇
اقل شحن: 1000ج
""", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda x: x.data.startswith("buy_"))
def buy(call):
    key = call.data.replace("buy_", "")
    item = SERVICES[key]
    bal = get_balance(call.from_user.id)
    if bal < item['price']:
        bot.answer_callback_query(call.id, f"رصيدك {bal}ج غير كافي! المطلوب {item['price']}ج", show_alert=True)
        return
    c.execute("UPDATE users SET balance=balance-? WHERE id=?", (item['price'], call.from_user.id))
    conn.commit()
    msg = bot.send_message(call.message.chat.id, f"طلبت: {item['name']}\n\nرسل الـ ID حقك الآن:")
    bot.register_next_step_handler(msg, lambda m: process_id(m, key))

def process_id(m, service_key):
    player_id = m.text
    item = SERVICES[service_key]
    c.execute("INSERT INTO orders (user_id, service, player_id, status) VALUES (?,?,?,?)", (m.chat.id, service_key, player_id, "pending"))
    conn.commit()
    oid = c.lastrowid
    bot.send_message(m.chat.id, f"✅ تم استلام طلبك رقم {oid}\n{ item['name'] }\nID: {player_id}\n⏳ قيد التنفيذ")
    profit = item['price'] - item['cost']
    bot.send_message(ADMIN_ID, f"🔔 طلب جديد #{oid}\n👤 {m.chat.id} @{m.from_user.username}\n📦 {item['name']}\n🆔 {player_id}\n💰 ربحك: {profit}ج\n\n/done {oid}")

@bot.message_handler(content_types=['photo'])
def handle_photo(m):
    bot.forward_message(ADMIN_ID, m.chat.id, m.message_id)
    bot.send_message(ADMIN_ID, f"💳 اشعار شحن من {m.chat.id}\n/add {m.chat.id} المبلغ")
    bot.send_message(m.chat.id, "✅ تم ارسال الاشعار للأدمن، سيتم شحن رصيدك خلال 5 دقائق")

@bot.message_handler(commands=['add', 'done'])
def admin_cmd(m):
    if m.from_user.id!= ADMIN_ID: return
    try:
        if m.text.startswith("/add"):
            _, uid, amount = m.text.split()
            c.execute("UPDATE users SET balance=balance+? WHERE id=?", (int(amount), int(uid)))
            conn.commit()
            bot.send_message(int(uid), f"✅ تم شحن رصيدك {amount}ج!\nرصيدك الآن: {get_balance(int(uid))}ج")
        elif m.text.startswith("/done"):
            oid = int(m.text.split()[1])
            c.execute("SELECT user_id, service FROM orders WHERE id=?", (oid,))
            o = c.fetchone()
            if o:
                c.execute("UPDATE orders SET status='done' WHERE id=?", (oid,))
                conn.commit()
                bot.send_message(o[0], f"✅ تم تنفيذ طلبك: {SERVICES[o[1]]['name']} بنجاح!")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"خطأ: {e}")

print("Bot Running MyCash Only...")
bot.infinity_polling()
