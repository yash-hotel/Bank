# handlers/register.py

import random
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import create_user, user_exists

register_router = Router()

class RegisterState(StatesGroup):
    waiting_for_name = State()
    waiting_for_mobile = State()
    waiting_for_aadhaar = State()
    waiting_for_pan = State()
    waiting_for_kit_options = State()

@register_router.message(Command("start"))
async def start_handler(message: Message):
    welcome_text = (
        "🏦 Welcome to <b>Yash Private Bank</b>!\n\n"
        "Your trusted digital partner for safe and smart banking.\n"
        "💳 Manage your money with ease and transparency.\n"
        "🧾 Check balances, view statements, and more — anytime, anywhere.\n"
        "🔐 Your data is protected with military-grade encryption.\n\n"
        "Type /register to open your account now!"
    )
    await message.answer(welcome_text)

@register_router.message(Command("register"))
async def register_command(message: Message, state: FSMContext):
    if user_exists(message.from_user.id):
        await message.answer("✅ You already have an account with Yash Private Bank.")
    else:
        await message.answer("👤 Please enter your full name:")
        await state.set_state(RegisterState.waiting_for_name)

@register_router.message(RegisterState.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📱 Enter your mobile number:")
    await state.set_state(RegisterState.waiting_for_mobile)

@register_router.message(RegisterState.waiting_for_mobile)
async def process_mobile(message: Message, state: FSMContext):
    await state.update_data(mobile=message.text)
    await message.answer("🆔 Enter your Aadhaar number:")
    await state.set_state(RegisterState.waiting_for_aadhaar)

@register_router.message(RegisterState.waiting_for_aadhaar)
async def process_aadhaar(message: Message, state: FSMContext):
    await state.update_data(aadhaar=message.text)
    await message.answer("🧾 Enter your PAN number:")
    await state.set_state(RegisterState.waiting_for_pan)

@register_router.message(RegisterState.waiting_for_pan)
async def process_pan(message: Message, state: FSMContext):
    await state.update_data(pan=message.text)

    # Show welcome kit options
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Debit Card"), KeyboardButton(text="Credit Card")],
            [KeyboardButton(text="Passbook"), KeyboardButton(text="Cheque Book")],
            [KeyboardButton(text="Internet Banking")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Select welcome kit item"
    )

    await message.answer(
        "📦 What would you like to include in your welcome kit?\n"
        "You can select one or more items (send one at a time).",
        reply_markup=keyboard
    )
    await state.set_state(RegisterState.waiting_for_kit_options)

@register_router.message(RegisterState.waiting_for_kit_options)
async def process_kit_options(message: Message, state: FSMContext):
    data = await state.get_data()
    selected_kit = message.text

    # Generate a unique account number (e.g. AC1234567890)
    account_number = "AC" + str(random.randint(1000000000, 9999999999))

    # Save to database
    create_user(
        user_id=message.from_user.id,
        name=data["name"],
        account_number=account_number,
        mobile=data["mobile"],
        aadhaar=data["aadhaar"],
        pan=data["pan"],
        welcome_kit=selected_kit
    )

    # Final confirmation message
    await message.answer(
        f"🎉 <b>Account Successfully Opened!</b>\n\n"
        f"👤 Name: {data['name']}\n"
        f"🏦 Account No: {account_number}\n"
        f"📱 Mobile: {data['mobile']}\n"
        f"🆔 Aadhaar: {data['aadhaar']}\n"
        f"🧾 PAN: {data['pan']}\n"
        f"📦 Welcome Kit: {selected_kit}\n\n"
        f"✅ You can now use /balance and other services. Welcome to Yash Private Bank!"
    )
    await state.clear()
