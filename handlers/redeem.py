from pyrogram import filters
from pyrogram.types import Message
from main import app
from utils import get_user_data, update_user_data, save_data
import json
import os
import random
import string

REDEEM_FILE = "redeem_codes.json"

# Load redeem codes
if os.path.exists(REDEEM_FILE):
    with open(REDEEM_FILE, "r") as f:
        CODES = json.load(f)
else:
    CODES = {}

def save_codes():
    with open(REDEEM_FILE, "w") as f:
        json.dump(CODES, f)

@app.on_message(filters.command("redeem"))
async def redeem_command(client, message: Message):
    await message.reply("🔐 Please send your 16-character redeem code:")

@app.on_message(filters.text & filters.private)
async def redeem_check(client, message: Message):
    code = message.text.strip().upper()
    uid = message.from_user.id
    user = get_user_data(uid)

    if code in CODES:
        if CODES[code]["used"]:
            await message.reply("❌ This code has already been used.")
        else:
            credits = CODES[code]["credits"]
            user["credits"] += credits
            update_user_data(uid, "credits", user["credits"])
            CODES[code]["used"] = True
            save_codes()
            await message.reply(f"✅ Code redeemed successfully!\n💰 You got {credits} credits.")
    elif len(code) == 16 and all(c in string.ascii_uppercase + string.digits for c in code):
        await message.reply("❌ Invalid code or expired.")
    else:
        pass  # Let other message handlers work

# ADMIN ONLY — Generate redeem code
@app.on_message(filters.command("gen_code") & filters.user(app.config.ADMINS))
async def gen_redeem_code(client, message: Message):
    try:
        credits = int(message.text.split()[1])
    except:
        await message.reply("❌ Usage: `/gen_code 50`", quote=True)
        return

    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    CODES[code] = {"credits": credits, "used": False}
    save_codes()
    await message.reply(f"🎁 Redeem code generated:\n`{code}`\nWorth: {credits} credits")

