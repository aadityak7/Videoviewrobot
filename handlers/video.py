from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import VIDEO_DB, DOWNLOAD_DELETE_TIME, VIDEO_DELETE_TIME
from utils import get_user_data, update_user_data, countdown_timer
from main import app

@app.on_callback_query(filters.regex("get_video"))
async def ask_video_code(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "**🎥 Send the video code now (e.g., 1, 2, 3...)**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="go_home")]
        ])
    )

@app.on_message(filters.text & filters.private)
async def handle_video_code(client, message):
    user = message.from_user
    uid = user.id
    text = message.text.strip()

    if not text.isdigit():
        return

    video_code = int(text)
    try:
        # Try to forward video from VIDEO_DB
        sent = await client.forward_messages(
            chat_id=message.chat.id,
            from_chat_id=VIDEO_DB,
            message_ids=video_code
        )

        # Attach buttons
        await sent.edit_reply_markup(
            InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("👍 Like", callback_data=f"like_{video_code}"),
                    InlineKeyboardButton("👎 Dislike", callback_data=f"dislike_{video_code}")
                ],
                [
                    InlineKeyboardButton("⬇️ Download (2 credits)", callback_data=f"download_{video_code}"),
                    InlineKeyboardButton("➡️ Next", callback_data="get_video")
                ],
                [
                    InlineKeyboardButton("🤖 By Community", callback_data="by_community")
                ]
            ])
        )

        # Start 10-minute delete timer
        await countdown_timer(client, sent, VIDEO_DELETE_TIME)

    except Exception as e:
        await message.reply("🚫 Invalid video code or video not found.")

@app.on_callback_query(filters.regex("download_"))
async def download_video(client, callback_query: CallbackQuery):
    user = callback_query.from_user
    uid = user.id
    code = int(callback_query.data.split("_")[1])
    data = get_user_data(uid)

    if data["credits"] < 2:
        await callback_query.answer("🚫 Not enough credits!", show_alert=True)
        return

    try:
        sent = await client.forward_messages(
            chat_id=callback_query.message.chat.id,
            from_chat_id=VIDEO_DB,
            message_ids=code
        )
        await sent.reply("📥 Downloaded! This will auto-delete in 5 minutes.")
        update_user_data(uid, "credits", data["credits"] - 2)
        await countdown_timer(client, sent, DOWNLOAD_DELETE_TIME)

    except Exception:
        await callback_query.answer("⚠️ Error sending video.", show_alert=True)

@app.on_callback_query(filters.regex("go_home"))
async def back_to_menu(client, callback_query):
    from utils import main_menu
    is_admin = callback_query.from_user.id in [int(x) for x in get_user_data(callback_query.from_user.id).get("admins", [])]
    await callback_query.message.edit_text(
        "🏠 **Main Menu:**",
        reply_markup=main_menu(is_admin)
    )

