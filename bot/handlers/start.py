from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot
from aiogram.fsm.context import FSMContext

from bot.config import CHANNEL_ID, CHAT_ID
from bot.handlers.register import Register

router = Router()


# 🔍 Проверка подписки
async def check_sub(bot: Bot, user_id: int):
    try:
        ch = await bot.get_chat_member(CHANNEL_ID, user_id)
        chat = await bot.get_chat_member(CHAT_ID, user_id)

        return (
            ch.status in ["member", "administrator", "creator"]
            and chat.status in ["member", "administrator", "creator"]
        )
    except:
        return False


# 🚀 /start
@router.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id

    # ❌ не подписан
    if not await check_sub(bot, user_id):
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Канал", url=f"https://t.me/{CHANNEL_ID.replace('@','')}")],
            [InlineKeyboardButton(text="💬 Чат", url="https://t.me/your_chat_link")],
            [InlineKeyboardButton(text="✅ Проверить", callback_data="check_sub")]
        ])

        await message.answer(
            "🌍 Добро пожаловать в Dating Travel\n\n"
            "Здесь ты можешь найти людей для общения и путешествий ✈️\n\n"
            "❗ Для доступа подпишись на канал и чат:",
            reply_markup=kb
        )
        return

    # ✅ сразу регистрация
    await state.set_state(Register.name)
    await message.answer("👤 Введите имя:")


# 🔁 кнопка проверки
@router.callback_query(F.data == "check_sub")
async def recheck(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    if await check_sub(bot, call.from_user.id):
        await call.message.delete()

        await state.set_state(Register.name)
        await call.message.answer("👤 Введите имя:")
    else:
        await call.answer("❌ Подпишись сначала", show_alert=True)
