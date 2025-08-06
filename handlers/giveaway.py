from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from main import app
from utils import get_user_data, update_user_data, save_data
import json
import os

GIVEAWAY_FILE = "giveaways.json"

# Load existing giveaways
if os.path.exists(GIVEAWAY_FILE):
    with open(GIVEAWAY_FILE, "r") as f:
        GIVEAWAYS = json.load(f)
else:
    GIVEAWAYS = {}

def save_giveaways():
    with open(GIVEAWAY_FILE, "w") as f:
        json.dump(GIVEAWAYS, f)

@app.on_message(filters.command("giveaway") & filters.user(app.config.ADMINS))
async def create_giveaway(client, message: Message):
    try:
        _, title, reward, criteria = message.text.split("|", 3)
        gid = str(len(GIVEAWAYS) + 1)
        GIVEAWAYS[gid] = {
            "title": title.strip(),
            "reward": reward.strip(),
            "criteria": criteria.strip(),
            "participants": []
        }
        save_giveaways()

        await message.reply(
            f"🎁 *New Giveaway Created!*\n\n📌 *{title.strip()}*\n🏆 Reward: {reward.strip()}\n📝 Criteria: {criteria.strip()}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎉 Join Giveaway", callback_data=f"join_giveaway_{gid}")]
            ])
        )
    except:
        await message.reply("❌ Usage:\n/giveaway Title | Reward | Criteria (all required)", quote=True)

@app.on_callback_query(filters.regex("join_giveaway_"))
async def join_giveaway(client, callback_query: CallbackQuery):
    gid = callback_query.data.split("_")[-1]
    user = callback_query.from_user
    uid = str(user.id)

    if gid not in GIVEAWAYS:
        await callback_query.answer("❌ Giveaway not found.", show_alert=True)
        return

    giveaway = GIVEAWAYS[gid]

    if uid in giveaway["participants"]:
        await callback_query.answer("✅ Already joined!", show_alert=True)
        return

    # Check eligibility (placeholder logic - can be advanced)
    user_data = get_user_data(user.id)
    if user_data["credits"] < 5:
        await callback_query.answer("⚠️ You need at least 5 credits to join.", show_alert=True)
        return

    giveaway["participants"].append(uid)
    save_giveaways()

    await callback_query.answer("🎉 Joined successfully!", show_alert=True)

    await callback_query.message.edit_text(
        f"🎁 *{giveaway['title']}*\n\n🏆 Reward: {giveaway['reward']}\n📝 Criteria: {giveaway['criteria']}\n👤 Participants: {len(giveaway['participants'])}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎉 Joined", callback_data="noop")]
        ])
    )

