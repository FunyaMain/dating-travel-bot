from aiogram import Router, types

router = Router()

@router.message(lambda m: m.text == "👤 Мой профиль")
async def profile(msg: types.Message):
    await msg.answer("📌 Ваш профиль (заглушка)")
