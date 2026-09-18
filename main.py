import telebot
from telebot import types
import requests

# ========== الاعدادات - غيرهم ==========
BOT_TOKEN = "8854534383:AAHhSB8pzt1aMrmu7jChBU9OJN9_ItQfzFQ"
SMM_API_URL = "https://your-smm-site.com/api/v2"
SMM_API_KEY = "6abc35554c254fd901cc12bd1eeef799"
ADMIN_ID = 8554489917 # حط الايدي حقك في تليجرام
# =====================================

bot = telebot.TeleBot(BOT_TOKEN)

# قاعدة بيانات مؤقتة (بعدين بنربطها ب Google Sheet)
users_wallet = {}
orders = {}

# /start
@bot.message_handler(commands=['start'])
def start(message):
    ref = message.text.split()
    if len(ref) > 1:
        # نظام احالات
        referrer = ref[1]
        bot.send_message(message.chat.id, f"مرحب بيك! جيت عن طريق {referrer} حتاخد خصم 10%")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🛒 متجر الرشق", "🎮 شحن العاب")
    markup.add("📈 ترند السودان", "💰 محفظتي", "📦 طلباتي")

    bot.send_message(message.chat.id, f"""
أهلا {message.from_user.first_name} في بوت الرشق الاوتوماتيك 🔥

الدولار اليوم: 8800 جنيه
الدفع: بنكك - ماي كاشي

اختار من القائمة:
""", reply_markup=markup)

# زر الرشق
@bot.message_handler(func=lambda m: m.text == "🛒 متجر الرشق")
def shop(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("1000 متابع تيك توك - 3500ج", callback_data="buy_1000_tiktok"))
    markup.add(types.InlineKeyboardButton("1000 متابع انستا - 4000ج", callback_data="buy_1000_insta"))
    markup.add(types.InlineKeyboardButton("10000 مشاهدة تيك توك - 2000ج", callback_data="buy_views"))
    bot.send_message(message.chat.id, "اختار الخدمة:", reply_markup=markup)

# لما يضغط شراء - يربط اوتوماتيك بموقع الرشق
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def handle_buy(call):
    bot.send_message(call.message.chat.id, "رسل رابط حسابك (مثال:
