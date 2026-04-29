from aiogram import Router, types

router = Router()

@router.message(lambda m: m.text == "🖼 Фото анонимок")
async def admin_photo(msg: types.Message):
    await msg.answer("📸 Отправьте фото для анонимных сообщений")
