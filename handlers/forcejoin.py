from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import FORCE_JOIN
from main import app

async def check_force_join(client, message):
    try:
        user = message.from_user
        await client.get_chat_member(FORCE_JOIN, user.id)
        return True  # User is in the channel
    except UserNotParticipant:
        try:
            await message.reply(
                "**🔒 Access Denied**\n\nYou must join our channel to use this bot.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{FORCE_JOIN.strip('@')}")],
                        [InlineKeyboardButton("✅ I've Joined", callback_data="refresh_start")]
                    ]
                )
            )
        except Exception:
            pass
        return False
    except Exception:
        return True  # In case the channel is private or check fails silently

# Refresh start handler
@app.on_callback_query(filters.regex("refresh_start"))
async def refresh_start(client, callback_query):
    if await check_force_join(client, callback_query.message):
        from handlers.start import start_handler
        await start_handler(client, callback_query.message)
    else:
        await callback_query.answer("🚫 You still haven't joined!", show_alert=True)

