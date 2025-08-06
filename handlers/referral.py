from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from main import app
from utils import get_user_data, update_user_data, save_data
from config import BOT_TOKEN

@app.on_callback_query(filters.regex("referral"))
async def show_referral(client, callback_query: CallbackQuery):
    uid = callback_query.from_user.id
    user = get_user_data(uid)

    ref_link = f"https://t.me/{(await client.get_me()).username}?start={uid}"
    total_refs = user.get("referrals", 0)
    badge = user.get("badge", "Free")

    # Upgrade badges
    if total_refs >= 11:
        badge = "Top Referrer"
    elif total_refs >= 6:
        badge = "Premium"

    update_user_data(uid, "badge", badge)

    text = f"""
👥 **Your Referral Info**

🔗 Link: [Click to Copy]({ref_link})
👤 Total Referred: {total_refs}
🎖 Badge: {badge}

💰 You earn `7 credits` per successful referral (when they view a video).
"""

    await callback_query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="go_home")]
        ]),
        disable_web_page_preview=True
    )

@app.on_message(filters.command("start"))
async def referral_check(client, message):
    parts = message.text.split()
    uid = message.from_user.id

    if len(parts) == 2 and parts[1].isdigit():
        ref_id = int(parts[1])

        if ref_id != uid:
            ref_user = get_user_data(ref_id)
            referred = get_user_data(uid)

            if "ref_by" not in referred:
                referred["ref_by"] = ref_id
                ref_user["referrals"] += 1
                update_user_data(ref_id, "referrals", ref_user["referrals"])
                save_data()

                try:
                    await client.send_message(
                        ref_id,
                        f"🎉 You referred [{message.from_user.first_name}](tg://user?id={uid})!\nYou've earned +7 credits!"
                    )
                except:
                    pass

                ref_user["credits"] += 7
                update_user_data(ref_id, "credits", ref_user["credits"])

