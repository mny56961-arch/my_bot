@bot.message_handler(func=lambda m: m.text == "🛒 طلب متابعين")
def order_followers(m):
    if balances.get(m.chat.id,0) < 5000:
        bot.send_message(m.chat.id, "❌ رصيدك ما كافي، اشحن اول")
        return
    bot.send_message(m.chat.id, "📎 رسل رابط حسابك الانستا / تيك توك")
    bot.register_next_step_handler(m, get_link)

def get_link(m):
    bot.send_message(m.chat.id, "🔢 كم متابع داير؟ (مثلا 1000)")
    bot.register_next_step_handler(m, lambda msg: do_order(msg, m.text))

def do_order(m, link):
    try:
        qty = int(m.text)
        # خصم الرصيد
        cost = 5000 # سعر ثابت
        if balances.get(m.chat.id,0) < cost:
            bot.send_message(m.chat.id, "رصيدك ما كافي")
            return
        # طلب من SMM
        data = {"key": SMM_KEY, "action":"add", "service": 1234, "link": link, "quantity": qty}
        r = requests.post(SMM_URL, data=data).json()
        
        balances[m.chat.id] -= cost
        bot.send_message(m.chat.id, f"✅ تم استلام طلبك\nالكمية: {qty}\nالرابط: {link}\nID الطلب: {r.get('order')}")
        bot.send_message(ADMIN_ID, f"طلب جديد من {m.chat.id}\n{qty} متابع لـ {link}")
    except:
        bot.send_message(m.chat.id, "❌ اكتب رقم صحيح")
