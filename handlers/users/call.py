from aiogram.types import CallbackQuery

from loader import dp


@dp.callback_query_handler(lambda call: call.data == 'button_1')
async def handle_button_1(callback_query: CallbackQuery):
    # Send a response when Button 1 is clicked
    print('Keldi')
    await callback_query.answer("You clicked Button 1!")
    await callback_query.message.answer("This is the response for Button 1.")

@dp.callback_query_handler(lambda call: call.data == 'button_2')
async def handle_button_2(callback_query: CallbackQuery):
    print('Keldi 2')
    # Send a response when Button 2 is clicked
    await callback_query.answer("You clicked Button 2!")
    await callback_query.message.answer("This is the response for Button 2.")