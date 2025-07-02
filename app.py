import json
import os
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MANAGER_BOT_TOKEN = os.getenv('MANAGER_BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
CONTACT = os.getenv('CONTACT')

USERS_FILE = 'users.json'

# Load saved user tokens
def load_users():
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save updated user tokens
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

# Start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 স্বাগতম AIR BOT HOSTING BOT এ!\n\n"
        "আপনার বট হোস্ট করতে `/addtoken <your_bot_token>` লিখুন।\n"
        "✅ তারপর `/mybot` দিয়ে আপনার বট টেস্ট করুন।",
        parse_mode='Markdown'
    )

# Add bot token command
def add_token(update: Update, context: CallbackContext):
    users = load_users()
    user_id = str(update.message.from_user.id)

    if len(context.args) != 1:
        update.message.reply_text("⚠️ সঠিকভাবে লিখুন: `/addtoken <YOUR_BOT_TOKEN>`", parse_mode='Markdown')
        return

    token = context.args[0]
    if len(token) < 20 or ':' not in token:
        update.message.reply_text("❌ টোকেন ভুল। অনুগ্রহ করে সঠিক টোকেন দিন।")
        return

    users[user_id] = token
    save_users(users)
    update.message.reply_text("✅ টোকেন সংরক্ষণ করা হয়েছে। এখন `/mybot` দিয়ে টেস্ট করুন।", parse_mode='Markdown')

# Test user's bot
def mybot(update: Update, context: CallbackContext):
    users = load_users()
    user_id = str(update.message.from_user.id)

    if user_id not in users:
        update.message.reply_text("⚠️ আপনি এখনো কোনো টোকেন যুক্ত করেননি। `/addtoken <TOKEN>` দিয়ে যুক্ত করুন।", parse_mode='Markdown')
        return

    token = users[user_id]
    try:
        user_bot = Bot(token=token)
        user_bot.send_message(chat_id=update.message.chat_id, text="🤖 আপনার বট কাজ করছে!")
        update.message.reply_text("✅ টেস্ট সফল।")
    except Exception as e:
        update.message.reply_text(f"❌ ত্রুটি: {e}")

# Admin-only command
def admin_panel(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        update.message.reply_text("🚫 এই কমান্ড কেবল অ্যাডমিনের জন্য।")
        return

    users = load_users()
    total_users = len(users)
    text = (
        f"🛠️ *Admin Panel*\n\n"
        f"👥 মোট ইউজার: {total_users}\n"
        f"📞 Contact: {CONTACT}"
    )
    update.message.reply_text(text, parse_mode='Markdown')

# Main function
def main():
    updater = Updater(MANAGER_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("addtoken", add_token))
    dp.add_handler(CommandHandler("mybot", mybot))
    dp.add_handler(CommandHandler("admin", admin_panel))

    print("✅ AIR BOT HOSTING BOT is running on Render...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
