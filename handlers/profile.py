from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from main import app
from utils import get_user_data

@app.on_callback_query(filters.regex("profile"))
async def show_profile(client, callback_query):
    user = callback_query.from_user
    data = get_user_data(user.id)

    profile_text = f"""
👤 **Your Profile**

🆔 ID: `{user.id}`
👨‍💼 Name: {user.first_name}
🔗 Username: @{user.username or "N/A"}

💳 Plan: {data['plan']}
📅 Valid Till: {data['validity']}
💰 Credits: {data['credits']}
🧲 Hourly Usage: {data['hourly']}
👥 Referrals: {data['referrals']}
🎖 Badge: {data['badge']}
"""

    await callback_query.message.edit_text(
        profile_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="go_home")]
        ])
    )

