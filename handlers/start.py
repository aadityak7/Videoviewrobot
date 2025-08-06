from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMINS
from main import app
from handlers.forcejoin import check_force_join

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    user = message.from_user
    chat_id = message.chat.id

    # Check Force Join
    if not await check_force_join(client, message):
        return

    # Welcome text
    welcome_text = f"""
👋 Hello, {user.first_name}!

🎬 Welcome to *VideoView Bot*

🚀 Watch videos, earn credits, complete tasks, refer friends, and unlock more!

💡 Use the menu below to get started.
"""

    # User menu
    buttons = [
        [
            InlineKeyboardButton("👤 Profile", callback_data="profile"),
            InlineKeyboardButton("🎥 Get Video", callback_data="get_video"),
        ],
        [
            InlineKeyboardButton("🎯 Tasks", callback_data="tasks"),
            InlineKeyboardButton("🎁 Referral", callback_data="referral"),
        ],
        [
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
        ]
    ]

    # Admin-only button row
    if user.id in ADMINS:
        buttons.append([
            InlineKeyboardButton("⚙️ Admin Panel", callback_data="admin_panel"),
            InlineKeyboardButton("📊 Leaderboard", callback_data="leaderboard"),
        ])

    await message.reply(
        welcome_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )


