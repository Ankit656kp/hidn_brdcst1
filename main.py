import os
import sqlite3
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID"))
FORCE_JOIN = os.environ.get("FORCE_JOIN", "")
FORCE_JOIN_LINK = os.environ.get("FORCE_JOIN_LINK", "")

bot = Client("broadcast_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Database Setup
conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS banned (id INTEGER PRIMARY KEY)")
cursor.execute("CREATE TABLE IF NOT EXISTS sudo (id INTEGER PRIMARY KEY)")
cursor.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
conn.commit()

# User functions
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

def add_sudo(user_id):
    cursor.execute("INSERT OR IGNORE INTO sudo (id) VALUES (?)", (user_id,))
    conn.commit()

def remove_sudo(user_id):
    cursor.execute("DELETE FROM sudo WHERE id = ?", (user_id,))
    conn.commit()

def is_sudo(user_id):
    return cursor.execute("SELECT 1 FROM sudo WHERE id = ?", (user_id,)).fetchone() is not None

def is_admin(user_id):
    return user_id == OWNER_ID or is_sudo(user_id)

# Settings table functions
def set_setting(key, value):
    cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()

def get_setting(key):
    result = cursor.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    return result[0] if result else None

def del_setting(key):
    cursor.execute("DELETE FROM settings WHERE key = ?", (key,))
    conn.commit()

# Force Join Checker
async def check_force_join(user_id):
    if not FORCE_JOIN:
        return True
    try:
        user = await bot.get_chat_member(FORCE_JOIN, user_id)
        return user.status in ["member", "administrator", "creator"]
    except:
        return False

# /start
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

    chnl_link = get_setting("channel_link") or "https://t.me/example_channel"
    group_link = get_setting("group_link") or "https://t.me/example_group"
    owner_link = "https://t.me/Crack_by_Aizen"

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Join Channel", url=chnl_link)],
        [InlineKeyboardButton("👥 Join Group", url=group_link)],
        [InlineKeyboardButton("👤 Owner", url=owner_link)]
    ])

    await message.reply("👋 Welcome! You are now subscribed to broadcasts.", reply_markup=buttons)

# Refresh Button
@bot.on_callback_query(filters.regex("refresh"))
async def refresh_handler(client, callback):
    user_id = callback.from_user.id
    username = callback.from_user.username or "None"
    if await check_force_join(user_id):
        add_user(user_id, username)
        await callback.message.edit("✅ Access granted. You may use the bot now.")
    else:
        await callback.answer("🚫 You still haven't joined.", show_alert=True)

# Broadcast
@bot.on_message(filters.command("broadcast"))
async def broadcast_handler(client, message: Message):
    if not is_admin(message.from_user.id): return
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

# Stats
@bot.on_message(filters.command("stats"))
async def stats_handler(client, message: Message):
    if not is_admin(message.from_user.id): return
    total = cursor.execute("SELECT COUNT() FROM users").fetchone()[0]
    bans = cursor.execute("SELECT COUNT() FROM banned").fetchone()[0]
    sudos = cursor.execute("SELECT COUNT(*) FROM sudo").fetchone()[0]
    await message.reply(f"📊 Total users: {total}\n🚫 Banned: {bans}\n👮‍♂️ Sudo users: {sudos}")

# Ban/Unban
@bot.on_message(filters.command("ban"))
async def ban_handler(client, message: Message):
    if not is_admin(message.from_user.id): return
    try:
        user_id = int(message.command[1])
        ban_user(user_id)
        await message.reply(f"✅ User {user_id} banned.")
    except:
        await message.reply("⚠️ Usage: /ban <user_id>")

@bot.on_message(filters.command("unban"))
async def unban_handler(client, message: Message):
    if not is_admin(message.from_user.id): return
    try:
        user_id = int(message.command[1])
        unban_user(user_id)
        await message.reply(f"✅ User {user_id} unbanned.")
    except:
        await message.reply("⚠️ Usage: /unban <user_id>")

# List Users
@bot.on_message(filters.command("users"))
async def users_list_handler(client, message: Message):
    if not is_admin(message.from_user.id): return
    users = get_all_users()
    if not users:
        return await message.reply("❌ No users found.")
    user_list = "\n".join([f"👤 `{uid}` | @{uname}" if uname != "None" else f"👤 `{uid}`" for uid, uname in users])
    parts = [user_list[i:i+4000] for i in range(0, len(user_list), 4000)]
    for part in parts:
        await message.reply(part)

# Add/Remove Sudo
@bot.on_message(filters.command("addsudo"))
async def add_sudo_handler(client, message: Message):
    if message.from_user.id != OWNER_ID: return
    try:
        user_id = int(message.command[1])
        add_sudo(user_id)
        await message.reply(f"✅ User {user_id} added as sudo.")
    except:
        await message.reply("⚠️ Usage: /addsudo <user_id>")

@bot.on_message(filters.command("delsudo"))
async def del_sudo_handler(client, message: Message):
    if message.from_user.id != OWNER_ID: return
    try:
        user_id = int(message.command[1])
        remove_sudo(user_id)
        await message.reply(f"❌ User {user_id} removed from sudo.")
    except:
        await message.reply("⚠️ Usage: /delsudo <user_id>")

# Channel/Group Link Set/Delete
@bot.on_message(filters.command("addchnllink"))
async def add_channel_link_handler(client, message: Message):
    if not is_admin(message.from_user.id): return
    if len(message.command) < 2:
        return await message.reply("⚠️ Usage: /addchnllink <URL>")
    set_setting("channel_link", message.command[1])
    await message.reply("✅ Channel link saved.")

@bot.on_message(filters.command("delchnllink"))
async def delete_channel_link_handler(client, message: Message):
    if not is_admin(message.from_user.id): return
    del_setting("channel_link")
    await message.reply("❌ Channel link removed.")

@bot.on_message(filters.command("addgrouplink"))
async def add_group_link_handler(client, message: Message):
    if not is_admin(message.from_user.id): return
    if len(message.command) < 2:
        return await message.reply("⚠️ Usage: /addgrouplink <URL>")
    set_setting("group_link", message.command[1])
    await message.reply("✅ Group link saved.")

@bot.on_message(filters.command("delgrouplink"))
async def delete_group_link_handler(client, message: Message):
    if not is_admin(message.from_user.id): return
    del_setting("group_link")
    await message.reply("❌ Group link removed.")

bot.run()
