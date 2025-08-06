from pyrogram import filters
from pyrogram.types import Message
from main import app
from utils import USERS, get_user_data, update_user_data, save_data
import json

@app.on_message(filters.command("add_credit") & filters.user(app.config.ADMINS))
async def add_credit(client, message: Message):
    try:
        _, uid, amount = message.text.split()
        uid = str(uid)
        amount = int(amount)

        data = get_user_data(uid)
        data["credits"] += amount
        update_user_data(uid, "credits", data["credits"])
        save_data()

        await message.reply(f"✅ Added {amount} credits to {uid}")
    except:
        await message.reply("❌ Usage: /add_credit <user_id> <amount>")

@app.on_message(filters.command("broadcast") & filters.user(app.config.ADMINS))
async def broadcast_message(client, message: Message):
    if not message.reply_to_message:
        return await message.reply("❌ Reply to the message you want to broadcast.")

    sent = 0
    failed = 0
    for uid in USERS.keys():
        try:
            await client.copy_message(
                chat_id=int(uid),
                from_chat_id=message.chat.id,
                message_id=message.reply_to_message.message_id
            )
            sent += 1
        except:
            failed += 1

    await message.reply(f"📢 Broadcast sent to {sent} users.\n❌ Failed: {failed}")

@app.on_message(filters.command("user_stats") & filters.user(app.config.ADMINS))
async def show_user_stats(client, message: Message):
    total_users = len(USERS)
    premium = sum(1 for u in USERS.values() if u.get("plan") == "Premium")
    free = total_users - premium
    top_refs = sorted(USERS.items(), key=lambda x: x[1].get("referrals", 0), reverse=True)[:5]

    stats = f"""
📊 **User Stats:**

👥 Total Users: {total_users}
💎 Premium: {premium}
🆓 Free: {free}

🏅 **Top Referrers:**
"""

    for i, (uid, data) in enumerate(top_refs, 1):
        stats += f"{i}. {data.get('referrals', 0)} refs – {data.get('name', 'User')} ({uid})\n"

    await message.reply(stats)

@app.on_message(filters.command("set_plan") & filters.user(app.config.ADMINS))
async def set_plan(client, message: Message):
    try:
        _, uid, plan, days = message.text.split()
        uid = str(uid)
        days = int(days)

        user = get_user_data(uid)
        user["plan"] = plan
        user["validity"] = f"{days} days"
        update_user_data(uid, "plan", plan)
        update_user_data(uid, "validity", f"{days} days")
        save_data()

        await message.reply(f"✅ Set plan {plan} for {uid} valid for {days} days.")
    except:
        await message.reply("❌ Usage:\n/set_plan <user_id> <PlanType> <days>")

