import requests, telebot

# ===== بياناتك - ما تديها لزول =====
API_URL = "https://smmstone.com/api/v2"
API_KEY = "7f4affcc5c6cecdbf5d8e65df9d06421"
BOT_TOKEN = "8854534383:AAHhSB8pzt1aMrmu7jChBU9OJN9_ItQfzFQ"

BANKAK_NUMBER = "401321813"
BANKAK_NAME = "حساب تاجر - 401321813"

bot = telebot.TeleBot(BOT_TOKEN)
SERVICE_ID = 12634 # تيك توك مشاهدات

PRICE = {1000: 1500, 5000: 5000, 10000: 9000}

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, f"""
مرحبا بيك في متجر المشاهدات 👋

💰 الاسعار:
1000 مشاهدة = 1500ج
5000 مشاهدة = 5000ج
10000 مشاهدة = 9000ج

🏦 الدفع بنكك:
رقم الحساب: {BANKAK_NUMBER}

الخطوات:
1. حول المبلغ
2. رسل صورة الاشعار
3. رسل رابط فيديو التيك توك + العدد

مثال:
https://vt.tiktok.com/xxx 1000
""")

@bot.message_handler(func=lambda m: "tiktok.com" in m.text.lower() or "vt.tiktok" in m.text.lower())
def order(m):
    try:
        parts = m.text.strip().split()
        link = [p for p in parts if "tiktok" in p][0]
        qty = int([p for p in parts if p.isdigit()][0])

        if qty not in PRICE:
            bot.reply_to(m, f"الكمية المتاحة: {list(PRICE.keys())}")
            return

        # يطلب من SmmStone
        data = {
            'key': API_KEY,
            'action': 'add',
            'service': SERVICE_ID,
            'link': link,
            'quantity': qty
        }
        r = requests.post(API_URL, data=data).json()

        if 'order' in r:
            bot.reply_to(m, f"✅ تم تأكيد الدفع\nطلبك رقم {r['order']}\n{qty} مشاهدة ح تنزل في دقيقة\nشكرا لتحويلك لحساب {BANKAK_NUMBER}")
        else:
            bot.reply_to(m, f"❌ الرصيد في الموقع خلص. حولت؟ راجع الادمن\nالخطأ: {r}")

    except Exception as e:
        bot.reply_to(m, "الصيغة غلط. رسل الرابط والعدد\nمثال: https://vt.tiktok.com/xxx 1000")

print("البوت شغال...")
