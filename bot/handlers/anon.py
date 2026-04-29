from aiogram import Router, types
from aiogram.fsm.context import FSMContext

router = Router()

ANON_PRICE = 15

@router.message(lambda m: m.text == "💌 Анонимное сообщение")
async def anon_start(msg: types.Message, state: FSMContext):
    await msg.answer("✍️ Напишите анонимное сообщение (только текст)")
    await state.set_state("anon_text")

@router.message(lambda m: True)
async def anon_text(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(text=msg.text)

    await msg.answer(
        f"💳 Стоимость: {ANON_PRICE} ⭐\nПодтвердить?"
    )
    await state.set_state("anon_pay")
