import telebot
import json
import os
from telebot.types import ReplyKeyboardMarkup

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

bot = telebot.TeleBot(TOKEN)

def load_db():
    try:
        with open("database.json") as f:
            return json.load(f)
    except:
        return {"products": {}, "orders": []}

def save_db(data):
    with open("database.json", "w") as f:
        json.dump(data, f, indent=2)

@bot.message_handler(commands=['start'])
def start(msg):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🛒 Shop", "📦 Orders")

    bot.send_message(
        msg.chat.id,
        "🌐 Professional Service Bot\n\nClick Shop to start",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == "🛒 Shop")
def shop(msg):
    db = load_db()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    for cat in db.get("products", {}):
        markup.add(cat)

    bot.send_message(msg.chat.id, "Select Category:", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle(msg):
    db = load_db()

    if msg.text in db.get("products", {}):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        for item, price in db["products"][msg.text].items():
            markup.add(f"{item} - {price}")

        bot.send_message(msg.chat.id, "Select Product:", reply_markup=markup)

    elif "-" in msg.text:
        db.setdefault("orders", []).append({
            "user": msg.from_user.id,
            "order": msg.text,
            "status": "Pending"
        })
        save_db(db)

        bot.send_message(
            msg.chat.id,
            "✅ Order Confirmed!\n\nSend Payment Screenshot"
        )

        if ADMIN_ID:
            bot.send_message(
                ADMIN_ID,
                f"🆕 Order\nUser: {msg.from_user.id}\n{msg.text}"
            )

print("Bot running...")
bot.infinity_polling()
