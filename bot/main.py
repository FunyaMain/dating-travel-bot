import asyncio
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from bot.db import init_db

from bot.handlers import start, register, anon

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    await init_db()

    dp.include_router(start.router)
    dp.include_router(register.router)
    dp.include_router(anon.router)

    print("Bot started")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
