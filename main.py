
import os
import logging
import asyncio
from threading import Thread

from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
PORT = int(os.environ.get("PORT", "10000"))

web = Flask(__name__)
telegram_app = None


@web.get("/")
def home():
    return "HZR Secretary Bot is running."


@web.get("/health")
def health():
    return {"status": "ok"}


def get_reply(text):
    message = text.strip().lower()

    if any(word in message for word in ["سلام", "درود", "صبح بخیر"]):
        return "سلام! به HZR Secretary خوش آمدی. چطور می‌توانم کمک کنم؟"

    if "نامت چیست" in message or "اسمت چیست" in message:
        return "من HZR Secretary هستم؛ یک ربات تلگرام ساخته‌شده با پایتون."

    if "خوبی" in message or "حالت چطور" in message:
        return "تشکر، آماده‌ام! تو چطور هستی؟"

    if any(word in message for word in ["hello", "hi", "hey"]):
        return "Hello! Welcome to HZR Secretary. How can I help you?"

    if "what is your name" in message or "who are you" in message:
        return "I am HZR Secretary, a Telegram bot built with Python."

    if "how are you" in message:
        return "I am running and ready to help. How are you?"

    if message in ["help", "/help"]:
        return (
            "HZR Secretary Help\n"
            "• /start - Start the bot\n"
            "• /help - Show help\n"
            "Send سلام or hello to test me."
        )

    if "تشکر" in message or "ممنون" in message:
        return "خواهش می‌کنم!"

    if "thank you" in message or message == "thanks":
        return "You're welcome!"

    return (
        "برای این پیام هنوز پاسخ تعریف نشده است.\n"
        "I don't have a predefined answer for that yet."
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! به HZR Secretary خوش آمدی.\n"
        "Hello! Welcome to HZR Secretary.\n"
        "برای راهنما /help را بفرست."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "دستورات:\n/start - شروع ربات\n/help - راهنما\n\n"
        "Commands:\n/start - Start\n/help - Help"
    )


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if update.message and update.message.text:
        await update.message.reply_text(get_reply(update.message.text))


async def telegram_worker():
    global telegram_app

    telegram_app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("help", help_command))
    telegram_app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    await telegram_app.initialize()
    await telegram_app.start()

    await telegram_app.updater.start_polling()

    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        await telegram_app.updater.stop()
        await telegram_app.stop()
        await telegram_app.shutdown()


def run_telegram():
    asyncio.run(telegram_worker())


if __name__ == "__main__":
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is missing.")

    Thread(target=run_telegram, daemon=True).start()
    web.run(host="0.0.0.0", port=PORT)
