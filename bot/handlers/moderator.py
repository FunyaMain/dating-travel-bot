from aiogram import Router, types

router = Router()

@router.message(lambda m: m.text == "📢 Публикации")
async def post(msg: types.Message):
    await msg.answer("📢 Выберите топик и создайте пост")
