from pyrogram import Client
from config import BOT_TOKEN
import logging

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Pyrogram App setup
app = Client("videobot", bot_token=BOT_TOKEN)

# Import all handlers
import start
import profile
import video
import referral
import tasks
import redeem
import giveaway
import admin

if __name__ == "__main__":
    print("✅ Bot is starting...")
    app.run()

