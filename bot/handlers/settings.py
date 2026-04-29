from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


# ⚙️ МЕНЮ НАСТРОЕК АНКЕТЫ
@router.callback_query(F.data == "settings")
async def settings_menu(call: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Редактировать анкету", callback_data="edit_profile")],
        [InlineKeyboardButton(text="❌ Удалить анкету", callback_data="delete_profile")],
        [InlineKeyboardButton(text="🔕 Отключить анкету", callback_data="disable_profile")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_menu")]
    ])

    await call.message.edit_reply_markup(reply_markup=kb)


# 🔙 НАЗАД В ГЛАВНОЕ МЕНЮ К АНКЕТЕ
@router.callback_query(F.data == "back_menu")
async def back_menu(call: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚙️ Настройки анкеты", callback_data="settings")]
    ])

    await call.message.edit_reply_markup(reply_markup=kb)


# ✏️ РЕДАКТИРОВАНИЕ АНКЕТЫ (ПЕРЕЗАПУСК FSM)
@router.callback_query(F.data == "edit_profile")
async def edit_profile(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer("🔁 Давай заново заполним анкету. Введите имя:")
    await state.set_state("Register:name")  # если у тебя StatesGroup Register


# ❌ УДАЛЕНИЕ АНКЕТЫ (ЗАГЛУШКА ПОД БД)
@router.callback_query(F.data == "delete_profile")
async def delete_profile(call: types.CallbackQuery):
    # тут потом подключим БД удаление
    await call.message.answer("🗑 Анкета удалена (пока заглушка)")


# 🔕 ОТКЛЮЧЕНИЕ АНКЕТЫ (ЗАГЛУШКА ПОД БД)
@router.callback_query(F.data == "disable_profile")
async def disable_profile(call: types.CallbackQuery):
    # тут потом будет флаг в БД active = false
    await call.message.answer("🔕 Анкета отключена (пока заглушка)")
