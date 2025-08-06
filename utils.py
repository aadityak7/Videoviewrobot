from datetime import datetime, timedelta
import os
import json
from config import DB_CHANNEL
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# 📦 Local DB backup (store as temp in memory/file)
DATA_FILE = "user_data.json"

# Load data from file
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        USERS = json.load(f)
else:
    USERS = {}

def get_user_data(uid):
    if str(uid) not in USERS:
        USERS[str(uid)] = {
            "credits": 0,
            "plan": "Free",
            "validity": "N/A",
            "referrals": 0,
            "hourly": 3,
            "badge": "Free"
        }
        save_data()
    return USERS[str(uid)]

def update_user_data(uid, key, value):
    get_user_data(uid)  # Ensure user exists
    USERS[str(uid)][key] = value
    save_data()

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(USERS, f)

# ⏲ Countdown Timer
async def countdown_timer(bot, msg, seconds, delete=True):
    for remaining in range(seconds, -1, -1):
        try:
            await msg.edit_caption(f"{msg.caption or ''}\n⏳ Deleting in: {remaining}s")
        except MessageNotModified:
            pass
        await bot.sleep(1)

    if delete:
        await msg.delete()

# 🎮 Menu Buttons
def main_menu(is_admin=False):
    buttons = [
        [
            InlineKeyboardButton("👤 Profile", callback_data="profile"),
            InlineKeyboardButton("🎥 Get Video", callback_data="get_video"),
        ],
        [
            InlineKeyboardButton("🎯 Tasks", callback_data="tasks"),
            InlineKeyboardButton("🎁 Referral", callback_data="referral"),
        ],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")]
    ]
    if is_admin:
        buttons.append([
            InlineKeyboardButton("⚙️ Admin Panel", callback_data="admin_panel"),
            InlineKeyboardButton("📊 Leaderboard", callback_data="leaderboard"),
        ])
    return InlineKeyboardMarkup(buttons)

