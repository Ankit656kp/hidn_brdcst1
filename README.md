<h1 align="center">📢 Telegram Broadcast Bot</h1>

<p align="center">
  A powerful, clean, and lightweight Telegram bot to broadcast messages to your users with ease.
</p>

---

## 🚀 Deploy to Heroku

1. ⚙️ Fork or upload this repo to your GitHub.  
2. 📲 Click the button below to deploy:

<p align="center">
  <a href="https://heroku.com/deploy">
    <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy to Heroku">
  </a>
</p>

3. 📌 Set the following **Environment Variables**:

| Variable           | Description                                                   |
|--------------------|---------------------------------------------------------------|
| `API_ID`           | From [my.telegram.org](https://my.telegram.org)               |
| `API_HASH`         | From [my.telegram.org](https://my.telegram.org)               |
| `BOT_TOKEN`        | From [@BotFather](https://t.me/BotFather)                     |
| `OWNER_ID`         | Your Telegram numeric user ID                                 |
| `FORCE_JOIN`       | Your channel username like `@channelname` or leave empty      |
| `FORCE_JOIN_LINK`  | Optional: Full invite link if channel is private              |

✅ Your bot will be up and running after deployment!

---

## ✨ Features

- 🔐 Force Join system with “I’ve Joined” button  
- 👑 Admin + Sudo-based command system  
- 📊 Stats panel for total users, banned, sudo  
- 🧠 Smart user logging using SQLite  
- 📤 Easy and fast message broadcasting  
- ☁️ Ready for **Heroku Deployment**  
- 📁 Clean file structure and optimized code  

---

## 👤 Admin Commands

| Command              | Access     | Description                                      |
|----------------------|------------|--------------------------------------------------|
| `/broadcast`         | Owner/Sudo | Reply to any message to broadcast to all users   |
| `/stats`             | Owner/Sudo | View total users, banned users, sudo list        |
| `/users`             | Owner/Sudo | Show list of all registered users                |
| `/ban <user_id>`     | Owner/Sudo | Ban a user from using the bot                    |
| `/unban <user_id>`   | Owner/Sudo | Unban a previously banned user                   |
| `/addsudo <user_id>` | Owner only | Grant sudo access to a user                      |
| `/delsudo <user_id>` | Owner only | Remove sudo access from a user                   |

> ⚠️ Only the bot OWNER or added SUDO users can use these commands.

---

## 🛡 Force Join System

- If `FORCE_JOIN` is set, users must join your channel to use the bot.  
- Users are shown a **Join Button** and a **Refresh Button**.  
- Skipped if `FORCE_JOIN` is not configured.

---

## 🗄 SQLite Database

Stores:

- 👥 All users (ID, username)  
- ❌ Banned users  
- 👮‍♂️ Sudo users  

Database file: `bot.db` (auto-created on first run)

---

## 📁 Project Structure

```bash
.
├── main.py           # Main bot logic
├── bot.db            # SQLite DB file (auto-generated)
├── requirements.txt  # Python dependencies
└── README.md         # Project info
