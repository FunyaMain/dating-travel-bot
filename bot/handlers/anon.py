from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("anon"))
async def anon_cmd(message: types.Message):
    await message.answer("💬 Анонимные вопросы скоро будут доступны.")
