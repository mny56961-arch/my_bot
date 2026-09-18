import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ===== عدل هنا بس =====
BOT_TOKEN = "8854534383:AAHhSB8pzt1aMrmu7jChBU9OJN9_ItQfzFQ"

# ===== جاهز ما تهبشو =====
SMM_API_URL = "https://smmkings.com/api/v2" # لو موقعك مختلف غير الرابط ده بس
SMM_API_KEY = "6abc35554c254fd901cc12bd1eeef799"
ADMIN_ID = 8554489917
LOG_GROUP = "https://t.me/+5P92bf4JMbExYjA0" # البوت بيرسل فيها الطلبات

SERVICES = {
    "ig_follow": {"name": "متابعين انستا 👥 1K", "price": 5000, "api_id": 100, "qty": 1000},
    "ig_likes": {"name": "لايكات انستا ❤️ 1K", "price": 2000, "api_id": 101, "qty": 1000},
    "tt_follow": {"name": "متابعين تيك توك 🎵 1K", "price": 6000, "api_id": 200, "qty": 1000},
    "tt_views": {"name": "مشاهدات تيك توك 👀 10K", "price": 1500, "api_id": 201, "qty": 10000},
    "tt_likes": {"name": "لايكات تيك توك ❤️ 1K", "price": 2500, "api_id": 202, "qty": 1000},
    "free_100": {"name": "فري فاير 100 جوهرة 💎", "price": 5500, "api_id": 300, "qty": 1},
    "free_310": {"name": "فري فاير 310 جوهرة 💎", "price": 15000, "api_id": 301, "qty": 1},
    "pubg_60": {"name": "ببجي 60 شدة 🔫", "price": 6000, "api_id": 400, "qty": 1},
}

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 رشق متابعين", callback_data="cat_rashq"), InlineKeyboardButton("🎮 شحن العاب", callback_data="cat_games")],
        [InlineKeyboardButton("🔥 هاشتاقات ترند", callback_data="cat_trends")],
        [InlineKeyboardButton("💳 دفع بنكك - ماي كاشي", callback_data="cat_pay")],
        [InlineKeyboardButton("📞 تواصل مع الادارة", url="https://t.me/UshshhwhxBot")],
    ])

def make_order(api_id, link, qty):
    data = {"key": SMM_API_KEY, "action": "add", "service": api_id, "link": link, "quantity": qty}
    try:
        r = requests.post(SMM_API_URL, data=data, timeout=15).json()
        return r.get("order")
    except:
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"ارح يا {update.effective_user.first_name} 🔥\n\n"
        "مرحب بيك في **يونكو شوب - امدرمان**\n"
        "💵 الدولار: 8800 جنيه\n"
        "⚡️ البوت اوتوماتيك 24 ساعة\n\n"
        "اختار خدمتك من تحت:",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == "cat_rashq":
        kb = [[InlineKeyboardButton(f"{v['name']} | {v['price']}ج", callback_data=f"buy_{k}")] for k,v in SERVICES.items() if k.startswith("ig") or k.startswith("tt")]
        kb.append([InlineKeyboardButton("⬅️ رجوع", callback_data="back")])
        await q.edit_message_text("🚀 اختار خدمة الرشق:", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "cat_games":
        kb = [[InlineKeyboardButton(f"{v['name']} | {v['price']}ج", callback_data=f"buy_{k}")] for k,v in SERVICES.items() if "free" in k or "pubg" in k]
        kb.append([InlineKeyboardButton("⬅️ رجوع", callback_data="back")])
        await q.edit_message_text("🎮 اختار شحن اللعبة:", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "cat_trends":
        txt = "🔥 **ترند السودان الليلة:**\n\n#السودان #امدرمان #الخرطوم #السودان_ترند\n#تيك_توك_السودان #fyp #viral #foryou\n#اغاني_سودانية #ضحك_سوداني"
        await q.edit_message_text(txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ رجوع", callback_data="back")]]))

    elif data == "cat_pay":
        txt = "💳 **الدفع:**\n\nبنكك: 1234567 - محمد\nماي كاشي: 0912345678\n\nبعد تحول رسل الاشعار هنا"
        await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ رجوع", callback_data="back")]]))

    elif data.startswith("buy_"):
        key = data.replace("buy_", "")
        context.user_data["sel"] = key
        s = SERVICES[key]
        await q.edit_message_text(f"✅ اخترت: {s['name']}\n💰 السعر: {s['price']}ج\n
