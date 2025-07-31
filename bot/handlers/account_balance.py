from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot.database import get_account_details

router = Router()

class BalanceState(StatesGroup):
    waiting_for_account_number = State()


@router.message(F.text.lower() == "check balance")
async def ask_account_number(message: Message, state: FSMContext):
    await message.answer("🔢 Please enter your account number to check your balance:")
    await state.set_state(BalanceState.waiting_for_account_number)


@router.message(BalanceState.waiting_for_account_number)
async def show_balance(message: Message, state: FSMContext):
    acc_num = message.text.strip()

    account = await get_account_details(acc_num)

    if account:
        # Fake static balance for now
        await message.answer(
            f"🏦 *Account Holder:* {account['full_name']}\n"
            f"💰 *Available Balance:* ₹25,000.00\n"
            f"📄 *Account Number:* {account['account_number']}",
            parse_mode="Markdown"
        )
    else:
        await message.answer("❌ Account not found. Please check your account number.")

    await state.clear()
