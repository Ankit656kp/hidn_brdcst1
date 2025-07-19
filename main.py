import os
import sqlite3
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID"))
FORCE_JOIN = os.environ.get("FORCE_JOIN", "")  # Username like "@yourchannel"
FORCE_JOIN_LINK = os.environ.get("FORCE_JOIN_LINK", "")  # Full link like "https://t.me/..."

bot = Client("broadcast_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Database Setup
conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS banned (id INTEGER PRIMARY KEY)")
conn.commit()


def add_user(user_id, username):
    cursor.execute("INSERT OR REPLACE INTO users (id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()

def is_banned(user_id):
    return cursor.execute("SELECT 1 FROM banned WHERE id = ?", (user_id,)).fetchone() is not None

def ban_user(user_id):
    cursor.execute("INSERT OR IGNORE INTO banned (id) VALUES (?)", (user_id,))
    conn.commit()

def unban_user(user_id):
    cursor.execute("DELETE FROM banned WHERE id = ?", (user_id,))
    conn.commit()

def get_all_users():
    return cursor.execute("SELECT id, username FROM users").fetchall()

async def check_force_join(user_id):
    if not FORCE_JOIN:
        return True
    try:
        user = await bot.get_chat_member(FORCE_JOIN, user_id)
        return user.status in ["member", "administrator", "creator"]
    except:
        return False

@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "None"

    if is_banned(user_id):
        return await message.reply("🚫 You are banned from using this bot.")

    if FORCE_JOIN and not await check_force_join(user_id):
        join_url = FORCE_JOIN_LINK or f"https://t.me/{FORCE_JOIN.lstrip('@')}"
        button = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Join Channel", url=join_url)],
            [InlineKeyboardButton("✅ I've Joined", callback_data="refresh")]
        ])
        return await message.reply("🔒 Please join the channel to use the bot.", reply_markup=button)

    add_user(user_id, username)
    await message.reply("👋 Welcome! You are now subscribed to broadcasts.")

@bot.on_callback_query(filters.regex("refresh"))
async def refresh_handler(client, callback):
    user_id = callback.from_user.id
    username = callback.from_user.username or "None"
    if await check_force_join(user_id):
        add_user(user_id, username)
        await callback.message.edit("✅ Access granted. You may use the bot now.")
    else:
        await callback.answer("🚫 You still haven't joined.", show_alert=True)

@bot.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_handler(client, message: Message):
    if not message.reply_to_message:
        return await message.reply("📢 Reply to the message you want to broadcast.")

    users = get_all_users()
    success, failed = 0, 0

    for user in users:
        user_id = user[0]
        try:
            await message.reply_to_message.copy(user_id)
            success += 1
            await asyncio.sleep(0.05)
        except:
            failed += 1

    await message.reply(f"✅ Broadcast done.\n🟢 Sent: {success}\n🔴 Failed: {failed}")

@bot.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats_handler(client, message: Message):
    total = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    bans = cursor.execute("SELECT COUNT(*) FROM banned").fetchone()[0]
    await message.reply(f"📊 Total users: {total}\n🚫 Banned: {bans}")

@bot.on_message(filters.command("ban") & filters.user(OWNER_ID))
async def ban_handler(client, message: Message):
    try:
        user_id = int(message.command[1])
        ban_user(user_id)
        await message.reply(f"✅ User `{user_id}` banned.", quote=True)
    except:
        await message.reply("⚠️ Usage: /ban <user_id>")

@bot.on_message(filters.command("unban") & filters.user(OWNER_ID))
async def unban_handler(client, message: Message):
    try:
        user_id = int(message.command[1])
        unban_user(user_id)
        await message.reply(f"✅ User `{user_id}` unbanned.", quote=True)
    except:
        await message.reply("⚠️ Usage: /unban <user_id>")

@bot.on_message(filters.command("users") & filters.user(OWNER_ID))
async def users_list_handler(client, message: Message):
    users = get_all_users()
    if not users:
        return await message.reply("❌ No users found.")

    user_list = "\n".join([f"👤 `{uid}` | @{uname}" if uname != "None" else f"👤 `{uid}`" for uid, uname in users])
    parts = [user_list[i:i+4000] for i in range(0, len(user_list), 4000)]
    for part in parts:
        await message.reply(part)

bot.run()
