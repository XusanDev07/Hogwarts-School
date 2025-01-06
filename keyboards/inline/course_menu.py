from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_data import course_callback, book_callback

# 1-usul:
categoryMenu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🇹🇷 Turk tili', callback_data='turk'),
        ],
        [
            InlineKeyboardButton(text='💁‍♂️ Matematika', callback_data='math')
        ],
        [
            InlineKeyboardButton(text="🏴󠁧󠁢󠁥󠁮󠁧󠁿 Ingilis tili", callback_data="english"),
        ],
        [
            InlineKeyboardButton(text="📨 President maktablariga tayyorgarlik", callback_data="president"),
        ],
    ])


