from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "📞 Contact Support")
async def contact_support(message: Message):
    await message.answer(
        "📞 *Yash Private Bank Support*\n\n"
        "For any queries, please contact us:\n"
        "📱 Phone: +91-9876543210\n"
        "📧 Email: support@yashbank.in\n"
        "🏢 Address: Yash Towers, Mumbai\n\n"
        "_Available: Mon-Sat, 9AM - 6PM_",
        parse_mode="Markdown"
    )
