from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("register"))
async def register_cmd(message: types.Message):
    await message.answer("📝 Регистрация анкеты пока в разработке.")
