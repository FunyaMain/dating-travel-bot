from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧾 Моя анкета"), KeyboardButton(text="🔎 Поиск")],
            [KeyboardButton(text="💬 Анонимные вопросы")],
            [KeyboardButton(text="📜 Соглашение"), KeyboardButton(text="💖 Поддержать нас")]
        ],
        resize_keyboard=True
    )
