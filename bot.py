import json
import os
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv

load_dotenv()

MANAGER_BOT_TOKEN = os.getenv('7913791680:AAHmO83t1vF7GzTi80msCLloSV7cAufWbKo')
ADMIN_ID = int(os.getenv('7832264582'))
CONTACT = os.getenv('@rahbro22')

USERS_FILE = 'users.json'

def load_users():
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "স্বাগতম! আপনার বট হোস্ট করার জন্য /addtoken <your_bot_token> কমান্ডটি ব্যবহার করুন।
"
        "আপনার বট টোকেন জমা দেওয়ার পরে /mybot দিয়ে বট টেস্ট করুন।"
    )

def add_token(update: Update, context: CallbackContext):
    users = load_users()
    user_id = str(update.message.from_user.id)

    if len(context.args) != 1:
        update.message.reply_text("ব্যবহার: /addtoken <YOUR_BOT_TOKEN>")
        return

    token = context.args[0]

    # সহজ যাচাই - টোকেন কমপক্ষে 20 ক্যারেক্টার
    if len(token) < 20 or ':' not in token:
        update.message.reply_text("❌ টোকেনটি সঠিক মনে হচ্ছে না, দয়া করে সঠিক টোকেন দিন।")
        return

    users[user_id] = token
    save_users(users)
    update.message.reply_text("✅ আপনার বট টোকেন সেভ হয়েছে! এখন /mybot কমান্ড দিয়ে পরীক্ষা করুন।")

def mybot(update: Update, context: CallbackContext):
    users = load_users()
    user_id = str(update.message.from_user.id)

    if user_id not in users:
        update.message.reply_text("আপনার বট টোকেন পাওয়া যায়নি। আগে /addtoken কমান্ড দিয়ে টোকেন দিন।")
        return

    token = users[user_id]
    try:
        user_bot = Bot(token=token)
        user_bot.send_message(chat_id=update.message.chat_id, text="✅ আপনার বট সঠিকভাবে কাজ করছে!")
        update.message.reply_text("আপনার বট সফলভাবে মেসেজ পাঠিয়েছে।")
    except Exception as e:
        update.message.reply_text(f"বট মেসেজ পাঠাতে সমস্যা হয়েছে: {e}")

def admin_panel(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        update.message.reply_text("❌ আপনি এই কমান্ড ব্যবহার করার অনুমতি পাননি।")
        return

    users = load_users()
    total_users = len(users)
    text = f"🛠️ *Admin Panel*

👥 মোট ইউজার: {total_users}

📞 Contact: {CONTACT}"
    update.message.reply_text(text, parse_mode='Markdown')

def main():
    updater = Updater(MANAGER_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("addtoken", add_token))
    dp.add_handler(CommandHandler("mybot", mybot))
    dp.add_handler(CommandHandler("admin", admin_panel))

    updater.start_polling()
    print("Bot started...")
    updater.idle()

if __name__ == '__main__':
    main()
