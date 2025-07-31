# bot.py

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from handlers.register import register_router
# Future routers like balance, funds, etc. can be added here

from config import BOT_TOKEN

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    # Register routers
    dp.include_router(register_router)

    # Set bot commands
    await bot.set_my_commands([
        BotCommand(command="start", description="Welcome message"),
        BotCommand(command="register", description="Open a new bank account"),
        # Future commands can be added here
    ])

    print("🏦 Yash Private Bank bot is now running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
