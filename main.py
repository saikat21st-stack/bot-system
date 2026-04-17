import telebot
import json
from config import TOKEN, ADMIN_ID
from telebot.types import ReplyKeyboardMarkup

bot = telebot.TeleBot(TOKEN)

def load_db():
    with open("database.json") as f:
        return json.load(f)

def save_db(data):
    with open("database.json", "w") as f:
        json.dump(data, f, indent=2)

@bot.message_handler(commands=['start'])
def start(msg):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🛒 Shop", "📦 Orders")

    bot.send_message(msg.chat.id,
    "🌐 Professional Service Bot\n\nClick Shop to start",
    reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🛒 Shop")
def shop(msg):
    db = load_db()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    for cat in db["products"]:
        markup.add(cat)

    bot.send_message(msg.chat.id, "Select Category:", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle(msg):
    db = load_db()

    if msg.text in db["products"]:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        for item, price in db["products"][msg.text].items():
            markup.add(f"{item} - {price}")

        bot.send_message(msg.chat.id, "Select Product:", reply_markup=markup)

    elif "-" in msg.text:
        db["orders"].append({
            "user": msg.from_user.id,
            "order": msg.text,
            "status": "Pending"
        })
        save_db(db)

        bot.send_message(msg.chat.id,
        "✅ Order Confirmed!\n\nSend Payment Screenshot")

        bot.send_message(ADMIN_ID,
        f"🆕 Order\nUser: {msg.from_user.id}\n{msg.text}")

bot.infinity_polling()
