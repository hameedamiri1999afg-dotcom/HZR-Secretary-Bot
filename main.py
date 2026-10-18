
import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")


def get_reply(text: str) -> str:
    message = text.strip().lower()

    if not message:
        return "لطفاً یک پیام بنویس."

    # Persian and Dari
    if any(word in message for word in ["سلام", "درود", "صبح بخیر"]):
        return "سلام! به HZR Secretary خوش آمدی. چطور می‌توانم کمک کنم؟"

    if "نامت چیست" in message or "اسمت چیست" in message:
        return "من HZR Secretary هستم؛ یک ربات تلگرام ساخته‌شده با پایتون."

    if "حالت چطور" in message or "خوبی" in message:
        return "تشکر، آماده‌ام! تو چطور هستی؟"

    if "کمک" in message or "راهنما" in message:
        return (
            "راهنمای HZR Secretary:\n"
            "• سلام: شروع گفتگو\n"
            "• نامت چیست: معرفی ربات\n"
            "• help: راهنمای انگلیسی\n\n"
            "می‌توانی پرسش‌های دیگر را هم امتحان کنی."
        )

    # English
    if any(word in message for word in ["hello", "hi", "hey", "good morning"]):
        return "Hello! Welcome to HZR Secretary. How can I help you?"

    if "what is your name" in message or "who are you" in message:
        return "I am HZR Secretary, a Telegram bot built with Python."

    if "how are you" in message:
        return "I am running and ready to help. How are you?"

    if message in ["help", "/help"]:
        return (
            "HZR Secretary Help\n"
            "• Say hello to start a conversation.\n"
            "• Ask my name to learn about me.\n"
            "• Send other messages to test my responses."
        )

    if "thank you" in message or message == "thanks":
        return "You're welcome!"

    return (
        "هنوز پاسخ مشخصی برای این پیام ندارم.\n"
        "لطفاً پرسش دیگری مطرح کن.\n\n"
        "I don't have a predefined answer for that yet. "
        "Please try another question."
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! به HZR Secretary خوش آمدی.\n\n"
        "Hello! Welcome to HZR Secretary.\n"
        "برای راهنما /help را بفرست."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "دستورات:\n"
        "/start - شروع ربات\n"
        "/help - راهنما\n\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/help - Show help"
    )


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if update.message and update.message.text:
        reply = get_reply(update.message.text)
        await update.message.reply_text(reply)


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is missing.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    logging.info("HZR Secretary Bot is starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
