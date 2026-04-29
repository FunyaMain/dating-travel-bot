import asyncio
from aiogram import Bot, Dispatcher
from loader import bot, dp
from db.connection import init_db
import handlers  # noqa

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
