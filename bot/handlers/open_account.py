from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.database import save_account

router = Router()

# Step-by-step state management
class AccountOpenForm(StatesGroup):
    name = State()
    phone = State()
    address = State()
    kit = State()

@router.message(F.text.lower() == "open account")
async def start_account_opening(message: Message, state: FSMContext):
    await message.answer("Please enter your full name:")
    await state.set_state(AccountOpenForm.name)

@router.message(AccountOpenForm.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Enter your phone number:")
    await state.set_state(AccountOpenForm.phone)

@router.message(AccountOpenForm.phone)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Enter your address:")
    await state.set_state(AccountOpenForm.address)

@router.message(AccountOpenForm.address)
async def get_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)

    # Welcome kit options
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Debit Card"), KeyboardButton(text="Credit Card")],
            [KeyboardButton(text="Passbook"), KeyboardButton(text="Cheque Book")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Select what you want in your welcome kit:", reply_markup=keyboard)
    await state.set_state(AccountOpenForm.kit)

@router.message(AccountOpenForm.kit)
async def get_kit_and_save(message: Message, state: FSMContext):
    await state.update_data(kit=message.text)
    data = await state.get_data()

    # Save to DB
    account_number = save_account(
        name=data['name'],
        phone=data['phone'],
        address=data['address'],
        welcome_kit=data['kit']
    )

    await message.answer(
        f"🎉 Congratulations! Your account has been successfully opened.\n\n"
        f"🏦 *Yash Private Bank*\n"
        f"👤 Name: {data['name']}\n"
        f"📱 Phone: {data['phone']}\n"
        f"🏠 Address: {data['address']}\n"
        f"🎁 Welcome Kit: {data['kit']}\n"
        f"🔢 Account Number: `{account_number}`",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()
