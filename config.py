# config.py

import os

# Bot token will be read from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN not set. Use 'export BOT_TOKEN=your_token_here' in terminal.")
