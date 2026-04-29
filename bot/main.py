from aiogram import Bot, Dispatcher
from bot.handlers import start, register, anon

dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(register.router)
dp.include_router(anon.router)
