from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from main import app
from utils import get_user_data, update_user_data, save_data
import os

TASK_FILE = "tasks.txt"

# 🧾 Load task list
def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            return [line.strip() for line in f if line.strip()]
    return ["🧠 Follow our partner channel", "🎯 Subscribe to updates", "🗳 Vote on our next feature"]

# 📥 Save task list
def save_tasks(task_list):
    with open(TASK_FILE, "w") as f:
        for task in task_list:
            f.write(task + "\n")

@app.on_callback_query(filters.regex("tasks"))
async def show_tasks(client, callback_query: CallbackQuery):
    uid = callback_query.from_user.id
    user = get_user_data(uid)
    done_tasks = user.get("done_tasks", [])

    tasks = load_tasks()
    buttons = []

    for idx, task in enumerate(tasks):
        status = "✅ Done" if str(idx) in done_tasks else "🟢 Do"
        if str(idx) not in done_tasks:
            buttons.append([InlineKeyboardButton(f"{status} - {task}", callback_data=f"do_task_{idx}")])

    if not buttons:
        buttons = [[InlineKeyboardButton("✅ All tasks done for today!", callback_data="go_home")]]

    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="go_home")])

    await callback_query.message.edit_text(
        "**📝 Daily Tasks:**\n\nComplete tasks to earn 10 credits each.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex("do_task_"))
async def do_task_handler(client, callback_query: CallbackQuery):
    uid = callback_query.from_user.id
    user = get_user_data(uid)
    task_id = callback_query.data.split("_")[-1]

    if "done_tasks" not in user:
        user["done_tasks"] = []

    if task_id in user["done_tasks"]:
        await callback_query.answer("You already did this!", show_alert=True)
        return

    user["done_tasks"].append(task_id)
    user["credits"] += 10
    update_user_data(uid, "credits", user["credits"])
    save_data()

    await callback_query.answer("✅ Task completed! +10 credits", show_alert=True)
    await show_tasks(client, callback_query)

# ADMIN ONLY: /set_tasks Task1 | Task2 | Task3
@app.on_message(filters.command("set_tasks") & filters.user([int(x) for x in app.config.ADMINS]))
async def set_tasks(client, message):
    try:
        task_text = message.text.split(" ", 1)[1]
        task_list = [t.strip() for t in task_text.split("|")]
        save_tasks(task_list)
        await message.reply("✅ Tasks updated.")
    except:
        await message.reply("❌ Usage:\n`/set_tasks Task1 | Task2 | Task3`", quote=True)

