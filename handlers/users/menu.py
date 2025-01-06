import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, MediaGroup, InputFile

from keyboards.default.menu_keyboard import MENU
# Ташкент, улица Дурмон йули, 46
from loader import dp



class RegistrationStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_surname = State()
    waiting_for_contact = State()
    confirmation = State()

# Step 2: Handle "Do you want to enroll in a course?" button
@dp.message_handler(text='💬 Kursga yozilmoqchiman')
async def start_registration(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for course_name in course_details.keys():
        button = InlineKeyboardButton(text=course_name.upper(), callback_data=f"register:{course_name}")
        keyboard.add(button)

    await message.answer("Qaysi kursga yozilmoqchisiz? Tanlang:", reply_markup=keyboard)

# Step 3: Handle course selection
@dp.callback_query_handler(lambda c: c.data.startswith("register:"))
async def course_selected(callback_query: types.CallbackQuery, state: FSMContext):
    course_name = callback_query.data.split(":")[1]
    await state.update_data(course_name=course_name)
    await callback_query.message.edit_text(f"Tanlangan kurs: {course_name}. Ismingizni kiriting:")
    await RegistrationStates.waiting_for_name.set()
    await callback_query.answer()

# Step 4: Collect user's name
@dp.message_handler(state=RegistrationStates.waiting_for_name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Familiyangizni kiriting:")
    await RegistrationStates.waiting_for_surname.set()

# Step 5: Collect user's surname
@dp.message_handler(state=RegistrationStates.waiting_for_surname)
async def get_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    contact_button = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
        types.KeyboardButton(text="📞 Kontaktni ulashish", request_contact=True)
    )
    await message.answer("Telefon raqamingizni ulashing yoki kiriting:", reply_markup=contact_button)
    await RegistrationStates.waiting_for_contact.set()

# Step 6: Collect user's contact
@dp.message_handler(content_types=types.ContentType.CONTACT, state=RegistrationStates.waiting_for_contact)
async def get_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.contact.phone_number)
    data = await state.get_data()
    course_name = data['course_name']
    name = data['name']
    surname = data['surname']
    contact = data['contact']

    await message.answer(
        f"Quyidagi ma'lumotlar qabul qilindi:\n"
        f"👤 Ism: {name}\n"
        f"👥 Familiya: {surname}\n"
        f"📞 Telefon: {contact}\n"
        f"📚 Kurs: {course_name}\n\n"
        f"Hammasi to'g'rimi?",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("✅ Ha", callback_data="confirm"),
            InlineKeyboardButton("❌ Yo'q", callback_data="cancel")
        )
    )
    await RegistrationStates.confirmation.set()

# Step 7: Confirm registration
@dp.callback_query_handler(lambda c: c.data in ["confirm", "cancel"], state=RegistrationStates.confirmation)
async def confirm_registration(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "confirm":
        data = await state.get_data()
        course_name = data['course_name']
        name = data['name']
        surname = data['surname']
        contact = data['contact']

        # Send a notification to your user ID
        admin_user_id = int(os.getenv("ADMINS"))  # Replace with your actual user ID
        await dp.bot.send_message(
            admin_user_id,
            f"Yangi ro'yxatga olish:\n"
            f"👤 Ism: {name}\n"
            f"👥 Familiya: {surname}\n"
            f"📞 Telefon: {contact}\n"
            f"📚 Kurs: {course_name}"
        )

        await callback_query.message.edit_text("Ro'yxatdan muvaffaqiyatli o'tdingiz! 😊")
    else:
        await callback_query.message.edit_text("Ro'yxatdan o'tish bekor qilindi.")

    await state.finish()
    await callback_query.message.answer("Bosh menyu: 👇", reply_markup=MENU)
    await callback_query.answer()

course_details = {
    "Turk tili 🇹🇷": {
        "individual": "Turk tili (Individual) - Bu kursda siz individual ravishda o'rganasiz. \nDavomiylik: 3 oy 📆. \nKitoblar markaz tomonidan taminlanadi!",
        "group": "Turk tili (Guruh bilan) - Bu kursda siz guruh bilan o'rganasiz. \nDavomiylik: 5 oy 📆. \nKitoblar markaz tomonidan taminlanadi!"
    },
    "Matematika 🧮": {
        "individual": "Matematika (Individual) - Bu kursda siz individual ravishda o'rganasiz. \nDavomiylik: 1 yil 📆. \nKitoblar markaz tomonidan taminlanadi!",
        "group": "Matematika (Guruh bilan) - Bu kursda siz guruh bilan o'rganasiz. \nDavomiylik: 15 oy 📆. \nKitoblar markaz tomonidan taminlanadi!"
    },
    "Ingiliz tili 🏴󠁧󠁢󠁥󠁮󠁧󠁿": {
        "individual": "Ingliz tili (Individual) - Bu kursda siz individual ravishda o'rganasiz. \nDavomiylik: 5 oy 📆. \nKitoblar markaz tomonidan taminlanadi!",
        "group": "Ingliz tili (Guruh bilan) - Bu kursda siz guruh bilan o'rganasiz. \nDavomiylik: 8 oy 📆. \nKitoblar markaz tomonidan taminlanadi!"
    },
    "President maktablariga tayyorgarlik 📨": {
        "group": "President maktablari (Guruh bilan) - Bu kursda siz guruh bilan o'rganasiz.\nDavomiylik: 1 yil 📆.\nDarslar haftasiga 6 kun.\n3 kun Ingiliz tili 1:30 soatdan.\n3 kun Matematika (Mantiq) 1:30 soatdan.\nKitoblar markaz tomonidan taminlanadi!"
    }
}

# Callback data constants
COURSES_CALLBACK = "course:"
DETAILS_CALLBACK = "details:"
BACK_CALLBACK = "back:"

@dp.message_handler(text='📚 Course')
async def show_courses(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for course_name in course_details.keys():
        button = InlineKeyboardButton(text=course_name.upper(), callback_data=f"{COURSES_CALLBACK}{course_name}")
        keyboard.add(button)

    await message.answer("Bizdagi mavjud kurslar:", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data.startswith(COURSES_CALLBACK))
async def show_course_options(callback_query: types.CallbackQuery):
    course_name = callback_query.data[len(COURSES_CALLBACK):]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("Individual", callback_data=f"{DETAILS_CALLBACK}individual:{course_name}"),
        InlineKeyboardButton("Guruh bilan", callback_data=f"{DETAILS_CALLBACK}group:{course_name}"),
        InlineKeyboardButton("⬅️ Orqaga", callback_data=BACK_CALLBACK)
    )

    await callback_query.message.edit_text(f"'{course_name}' kursi uchun tanlang:", reply_markup=keyboard)
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data.startswith(DETAILS_CALLBACK))
async def show_course_details(callback_query: types.CallbackQuery):
    _, option, course_name = callback_query.data.split(':')
    details = course_details.get(course_name, {}).get(option, "Kurs ma'lumotlari topilmadi.")

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("⬅️ Orqaga", callback_data=f"{COURSES_CALLBACK}{course_name}"))

    await callback_query.message.edit_text(details, reply_markup=keyboard)
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == BACK_CALLBACK)
async def back_to_courses(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for course_name in course_details.keys():
        button = InlineKeyboardButton(text=course_name.upper(), callback_data=f"{COURSES_CALLBACK}{course_name}")
        keyboard.add(button)

    await callback_query.message.edit_text("Bizdagi mavjud kurslar:", reply_markup=keyboard)
    await callback_query.answer()

@dp.message_handler(text='📍 Location')
async def send_link(message: types.Message):
    latitude = 41.35526544551561
    longitude = 69.37879131253294

    await message.answer("Bu bizning manizlimiz 👇🏻")
    await message.answer_location(latitude=latitude, longitude=longitude)



@dp.message_handler(text='📊 Results')
async def send_link(message: types.Message):
    image_paths = [
        "media/photo_2024-04-27_09-37-02.jpg",
        "media/photo_2024-04-27_09-37-11.jpg",
        "media/photo_2024-06-05_13-14-36.jpg",
        "media/photo_2024-06-25_18-38-55.jpg",
        "media/photo_2024-06-27_11-57-14.jpg",
        "media/photo_2024-07-05_10-00-18.jpg",
        "media/photo_2024-12-24_15-47-53.jpg",
        "media/photo_2024-12-24_16-05-42.jpg",
    ]

    await message.answer("Bu yerda bizning o'quvchilarimizning natijalari bilan tanishasiz 👇🏻")

    media = MediaGroup()

    for i, image_path in enumerate(image_paths):
        try:
            media.attach_photo(InputFile(image_path))
        except FileNotFoundError:
            await message.answer(f"Rasm topilmadi: {image_path}")
        if (i + 1) % 10 == 0 or i == len(image_paths) - 1:
            await message.answer_media_group(media)
            media = MediaGroup()

@dp.message_handler(text='📞 Contact')
async def send_link(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)  # Har bir qator uchun 1 ta tugma

    telegram_button = InlineKeyboardButton(
        text="📱 Telegram Channel",
        url="https://t.me/Hogwarts_school_tashkent"
    )
    telegram_profile_button = InlineKeyboardButton(
        text="💭 Qo'shimcha savollar uchun",
        url="https://t.me/Hogwarts_school_admin"
    )
    instagram_button = InlineKeyboardButton(
        text="📸 Instagram",
        url="https://www.instagram.com/invites/contact/?i=mk6nbs2zlvcw&utm_content=q0xok7v"
    )

    keyboard.add(telegram_button, instagram_button, telegram_profile_button)
    await message.answer("Bu bizning telefon raqamimiz: +998947019916", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: True)
async def process_callback(callback_query: types.CallbackQuery):
    course_name = callback_query.data
    course_info = course_details.get(course_name, "Kurs ma'lumotlari topilmadi.")

    await callback_query.message.answer(course_info)
    await callback_query.answer()

