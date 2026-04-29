from aiogram import Router, types, F, Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.config import ADMIN_CHAT_ID, ADMIN_TOPIC_ID

router = Router()


# 📊 Состояния
class Register(StatesGroup):
    name = State()
    age = State()
    city = State()
    gender = State()
    looking = State()
    photo = State()


# 👤 Имя
@router.message(Register.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer("🎂 Возраст:")


# 🎂 Возраст
@router.message(Register.age)
async def get_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Register.city)
    await message.answer("🌆 Город:")


# 🌆 Город
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

    await message.answer("⚧ Выбери пол:", reply_markup=kb)


# ⚧ Пол
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


# 🔍 Кого ищет
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

    await call.message.edit_text("📸 Отправь фото:")


# 📸 Фото
@router.message(Register.photo, F.photo)
async def get_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)

    data = await state.get_data()

    text = (
        f"📋 Ваша анкета:\n\n"
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

    await message.answer_photo(photo_id, caption=text, reply_markup=kb)


# ❌ если не фото
@router.message(Register.photo)
async def no_photo(message: types.Message):
    await message.answer("❌ Отправь именно фото")


# ✅ Подтверждение + ЛОГ
@router.callback_query(F.data == "confirm")
async def confirm(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    user = call.from_user

    text = (
        f"🔥 Новая анкета\n\n"
        f"👤 {data['name']}, {data['age']}\n"
        f"🌆 {data['city']}\n"
        f"⚧ {data['gender']}\n"
        f"🔍 {data['looking']}\n\n"
        f"🆔 {user.id} | @{user.username or 'no_username'}"
    )

    # 📩 ЛОГ В АДМИН ТОПИК
    await bot.send_photo(
        chat_id=ADMIN_CHAT_ID,
        message_thread_id=ADMIN_TOPIC_ID,
        photo=data['photo'],
        caption=text
    )

    # ответ пользователю
    await call.message.edit_caption(
        caption="✅ Анкета сохранена!"
    )

    await state.clear()


# ✏️ Редактирование
@router.callback_query(F.data == "edit")
async def edit(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Register.name)
    await call.message.answer("🔁 Введи имя заново:")
