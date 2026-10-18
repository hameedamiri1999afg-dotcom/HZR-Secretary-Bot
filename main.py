import os
import logging
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession

logging.basicConfig(level=logging.INFO)
logging.getLogger("telethon").setLevel(logging.WARNING)

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]
PORT = int(os.environ.get("PORT", "10000"))

web = Flask(__name__)

client = TelegramClient(
    StringSession(SESSION_STRING),
    API_ID,
    API_HASH,
)

@web.get("/")
def home():
    return "HZR Personal Auto Reply is running."

@web.get("/health")
def health():
    return {"status": "ok"}

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def auto_reply(event):
    text = (event.raw_text or "").strip().lower()

    replies = {
        "سلام": "سلام! چطور می‌توانم کمک کنم؟",
        "سلام علیکم": "وعلیکم السلام!",
        "hello": "Hello! How can I help you?",
        "hi": "Hi! How are you?",
        "hey": "Hello! How can I help you?",
    }

    response = replies.get(text)

    if response:
        await event.reply(response)
        logging.info("Auto-replied to a private message.")

async def start_telegram():
    await client.connect()

    if not await client.is_user_authorized():
        raise RuntimeError(
            "The Telegram session is not authorized."
        )

    logging.info("Telegram client connected.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    import asyncio
    from threading import Thread

    def telegram_worker():
        asyncio.run(start_telegram())

    Thread(target=telegram_worker, daemon=True).start()
    web.run(host="0.0.0.0", port=PORT)
