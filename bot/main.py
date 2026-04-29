import asyncio
from bot.loader import dp, bot
from bot.handlers import start, profile, anon, admin, moderator

async def main():
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(anon.router)
    dp.include_router(admin.router)
    dp.include_router(moderator.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
