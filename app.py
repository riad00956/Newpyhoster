import json
import os
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv

load_dotenv()

MANAGER_BOT_TOKEN = os.getenv('MANAGER_BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
CONTACT = os.getenv('CONTACT')

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
        "👋 স্বাগতম!\n\n"
        "আপনার নিজস্ব টেলিগ্রাম বট হোস্ট করতে:\n"
        "`/addtoken <your_bot_token>`\n"
        "দিয়ে শুরু করুন।\n\n"
        "✅ তারপর `/mybot` দিয়ে পরীক্ষা করুন।",
        parse_mode='Markdown'
    )

def add_token(update: Update, context: CallbackContext):
    users = load_users()
    user_id = str(update.message.from_user.id)

    if len(context.args) != 1:
        update.message.reply_text("⚠️ ব্যবহার: `/addtoken <YOUR_BOT_TOKEN>`", parse_mode='Markdown')
        return

    token = context.args[0]

    if len(token) < 20 or ':' not in token:
        update.message.reply_text("❌ টোকেনটি ভুল, অনুগ্রহ করে সঠিক টোকেন দিন।")
        return

    users[user_id] = token
    save_users(users)
    update.message.reply_text("✅ টোকেন সেভ হয়েছে! এখন `/mybot` দিয়ে পরীক্ষা করুন।", parse_mode='Markdown')

def mybot(update: Update, context: CallbackContext):
    users = load_users()
    user_id = str(update.message.from_user.id)

    if user_id not in users:
        update.message.reply_text("⚠️ আপনি এখনো কোনো টোকেন যুক্ত করেননি। `/addtoken <TOKEN>` দিয়ে যুক্ত করুন।", parse_mode='Markdown')
        return

    token = users[user_id]
    try:
        user_bot = Bot(token=token)
        user_bot.send_message(chat_id=update.message.chat_id, text="🤖 আপনার বট সফলভাবে কাজ করছে!")
        update.message.reply_text("✅ টেস্ট সফল!")
    except Exception as e:
        update.message.reply_text(f"❌ বট মেসেজ পাঠাতে ব্যর্থ: {e}")

def admin_panel(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        update.message.reply_text("🚫 আপনি এই কমান্ড ব্যবহার করার অনুমতি পাননি।")
        return

    users = load_users()
    total_users = len(users)
    text = (
        "🛠️ *Admin Panel*\n\n"
        f"👥 মোট ইউজার: {total_users}\n"
        f"📞 কন্টাক্ট: {CONTACT}"
    )
    update.message.reply_text(text, parse_mode='Markdown')

def main():
    updater = Updater(MANAGER_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("addtoken", add_token))
    dp.add_handler(CommandHandler("mybot", mybot))
    dp.add_handler(CommandHandler("admin", admin_panel))

    print("🤖 Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
