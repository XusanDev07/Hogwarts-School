from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.menu_keyboard import MENU
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=MENU)


# @dp.callback_query_handler(lambda c: c.data)
# async def process_callback(callback_query: types.CallbackQuery):
#     if callback_query.data == "button_1":
#         response_text = "You clicked Button 1!"
#     elif callback_query.data == "button_2":
#         response_text = "You clicked Button 2!"
#
#     # Javobni yuborish
#     await bot.answer_callback_query(callback_query.id)
#     await bot.send_message(callback_query.from_user.id, response_text)
