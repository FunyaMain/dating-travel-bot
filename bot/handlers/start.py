from aiogram import Router, types
from db.queries import create_user

router = Router()

@router.message(commands=["start"])
async def start(msg: types.Message):
    await create_user(msg.from_user.id)

    await msg.answer(
        "👋 Привет!\nДобро пожаловать в Dating Travel 🌍"
    )
