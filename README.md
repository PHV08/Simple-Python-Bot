# Discord Bot

A lightweight Discord bot built with `discord.py`.
Includes a small SQLite-backed economy system and is designed to be easy to extend.

The project is intentionally kept in a single file for simplicity.

---

## Features

- Slash commands only
- SQLite database for persistent storage
- Basic economy system (balance, daily rewards)
- Utility and fun commands
- Clean embed-based UI
- Minimal dependencies
- Easy to extend

---

## Requirements

- Python 3.10+
- discord.py 2.3+
- A Discord bot application with:
  - applications.commands scope enabled

---

## Installation

1. Clone the repository
   git clone <repo-url>
   cd <repo-folder>

2. Install dependencies
   pip install -U discord.py

3. Set your bot token as an environment variable

   Linux / macOS:
   export bot_token=YOUR_BOT_TOKEN

   Windows:
   set bot_token=YOUR_BOT_TOKEN

4. Run the bot
   python bot.py

On first run, a local SQLite database (bot.db) will be created automatically.

---

## Commands

Utility
- /ping
- /uptime
- /help

Economy
- /balance
- /daily

Fun
- /flip
- /roll NdN
- /joke

---

## Database

The bot uses SQLite (bot.db) to store persistent data.

Stored data:
- User ID
- Coin balance
- Daily cooldown timestamp

Only Discord IDs are stored. Usernames and avatars are fetched dynamically.

---

## Project Structure

bot.py    - Main bot file
bot.db    - SQLite database (auto-generated)
README.md

