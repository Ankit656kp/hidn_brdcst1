# 📢 Telegram Broadcast Bot

A fast and lightweight Telegram broadcast bot to send messages to all your users with ease. Includes admin-only commands, force join system, and Heroku deploy support.

---

## 🚀 Deploy to Heroku

1. Upload this repo to your GitHub account.
2. Click the button below to deploy:

   [![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

3. Set the following environment variables during deployment:

   - `API_ID` – Get from [my.telegram.org](https://my.telegram.org)
   - `API_HASH` – Get from [my.telegram.org](https://my.telegram.org)
   - `BOT_TOKEN` – Get from [@BotFather](https://t.me/BotFather)
   - `OWNER_ID` – Your Telegram user ID
   - `FORCE_JOIN` – Channel username (like `@yourchannel`) or blank

4. Done! Your bot is now live.

---

## 🔧 Features

- Force join system to require users to join your channel.
- Admin commands for broadcasting, user stats, and logs.
- Heroku deploy ready.
- Lightweight and easy to manage.

---

## 👤 Admin Commands

| Command      | Description                                  |
|--------------|----------------------------------------------|
| `/broadcast` | Reply to a message to send it to all users   |
| `/logs`      | Check log messages in the log channel        |
| `/stats`     | Show total number of users                   |
| `/start`     | Show welcome message with force join check   |

> Only the bot owner (as set in `OWNER_ID`) can use these commands.

---

## 👑 Developed By

**👨‍💻 Developer:** *Devil*  
**📬 Contact:** [@Ankitgupta2143](https://t.me/Ankitgupta2143)

For more information, feel free to contact me on Telegram.

---

## 📜 License

**MIT License** – Free to use, share, and modify with credit.

---
