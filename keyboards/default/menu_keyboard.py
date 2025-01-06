from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

MENU = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📚 Course"), KeyboardButton(text="📊 Results")],
            [KeyboardButton(text="📍 Location")],
            [KeyboardButton(text="📞 Contact"), KeyboardButton(text="💬 Kursga yozilmoqchiman")]
        ],
        resize_keyboard=True
    )
