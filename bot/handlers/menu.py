from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()

@router.message(F.text == "/menu")
async def show_menu(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💼 Open Account")],
            [KeyboardButton(text="🏦 Check Account Balance")],
            [KeyboardButton(text="📞 Contact Support")],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )
    await message.answer(
        "🏦 *Welcome to Yash Private Bank's Services Menu:*\n\n"
        "Select an option below to proceed 👇",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
