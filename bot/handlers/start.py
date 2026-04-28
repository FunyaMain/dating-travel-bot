from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "👋 Привет! Добро пожаловать в Dating Travel бот.\n\n"
        "📌 Здесь ты можешь создать анкету и найти людей."
    )
