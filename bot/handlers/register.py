from aiogram import Router, types, F, Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.config import ADMIN_CHAT_ID, ADMIN_TOPIC_ID

router = Router()


# 📊 СТЕЙТЫ РЕГИСТРАЦИИ
class Register(StatesGroup):
    name = State()
    age = State()
    city = State()
    gender = State()
    looking = State()
    photo = State()


# 👤 ИМЯ
@router.message(Register.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer("🎂 Введите возраст:")


# 🎂 ВОЗРАСТ
@router.message(Register.age)
async def get_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Register.city)
    await message.answer("🌆 Введите город:")


# 🌆 ГОРОД
@router.message(Register.city)
async def get_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(Register.gender)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨 Мужчина", callback_data="g_m")],
        [InlineKeyboardButton(text="👩 Девушка", callback_data="g_f")],
        [InlineKeyboardButton(text="👫 Пара", callback_data="g_pair")],
        [InlineKeyboardButton(text="🌈 Би", callback_data="g_bi")]
    ])

    await message.answer("⚧ Выберите пол:", reply_markup=kb)


# ⚧ ПОЛ
@router.callback_query(F.data.startswith("g_"))
async def get_gender(call: types.CallbackQuery, state: FSMContext):
    gender_map = {
        "g_m": "Мужчина",
        "g_f": "Девушка",
        "g_pair": "Пара",
        "g_bi": "Би"
    }

    await state.update_data(gender=gender_map[call.data])
    await state.set_state(Register.looking)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨 Мужчину", callback_data="l_m")],
        [InlineKeyboardButton(text="👩 Девушку", callback_data="l_f")],
        [InlineKeyboardButton(text="👫 Пару", callback_data="l_pair")],
        [InlineKeyboardButton(text="🌈 Би", callback_data="l_bi")]
    ])

    await call.message.edit_text("🔍 Кого ищешь:", reply_markup=kb)


# 🔍 КОГО ИЩЕТ
@router.callback_query(F.data.startswith("l_"))
async def get_looking(call: types.CallbackQuery, state: FSMContext):
    looking_map = {
        "l_m": "Мужчину",
        "l_f": "Девушку",
        "l_pair": "Пару",
        "l_bi": "Би"
    }

    await state.update_data(looking=looking_map[call.data])
    await state.set_state(Register.photo)

    await call.message.edit_text("📸 Отправьте фото:")


# 📸 ФОТО
@router.message(Register.photo, F.photo)
async def get_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)

    data = await state.get_data()

    text = (
        f"👤 Имя: {data['name']}\n"
        f"🎂 Возраст: {data['age']}\n"
        f"🌆 Город: {data['city']}\n"
        f"⚧ Пол: {data['gender']}\n"
        f"🔍 Ищу: {data['looking']}"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm")],
        [InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit")]
    ])

    await message.answer_photo(photo=photo_id, caption=text, reply_markup=kb)


# ❌ НЕ ФОТО
@router.message(Register.photo)
async def no_photo(message: types.Message):
    await message.answer("❌ Отправьте фото")


# ✅ ПОДТВЕРЖДЕНИЕ
@router.callback_query(F.data == "confirm")
async def confirm(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    user = call.from_user

    text = (
        f"👤 Имя: {data['name']}\n"
        f"🎂 Возраст: {data['age']}\n"
        f"🌆 Город: {data['city']}\n"
        f"⚧ Пол: {data['gender']}\n"
        f"🔍 Ищу: {data['looking']}\n\n"
        f"🆔 @{user.username or 'no_username'} | {user.id}"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚙️ Настройки анкеты", callback_data="settings")]
    ])

    try:
        await call.message.delete()
    except:
        pass

    if data.get("photo"):
        await call.message.answer_photo(
            photo=data["photo"],
            caption=text,
            reply_markup=keyboard
        )
    else:
        await call.message.answer(text, reply_markup=keyboard)

    try:
        if ADMIN_TOPIC_ID:
            await bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                message_thread_id=ADMIN_TOPIC_ID,
                text=text
            )
        else:
            await bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=text
            )
    except Exception as e:
        print("ADMIN LOG ERROR:", e)

    await state.clear()


# ⚙️ НАСТРОЙКИ
@router.callback_query(F.data == "settings")
async def settings(call: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit_profile")],
        [InlineKeyboardButton(text="❌ Удалить", callback_data="delete_profile")],
        [InlineKeyboardButton(text="🔕 Отключить", callback_data="disable_profile")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_menu")]
    ])

    await call.message.edit_reply_markup(reply_markup=kb)


# 🔙 НАЗАД
@router.callback_query(F.data == "back_menu")
async def back_menu(call: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚙️ Настройки анкеты", callback_data="settings")]
    ])

    await call.message.edit_reply_markup(reply_markup=kb)


# ✏️ РЕДАКТИРОВАНИЕ (перезапуск)
@router.callback_query(F.data == "edit")
async def edit(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Register.name)
    await call.message.answer("🔁 Введите имя заново:")
