from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()
chat_ids = set()  # Bu yerda barcha foydalanuvchilarning chat_id'lari saqlanadi

@router.message(CommandStart())
async def start_command(message: Message):
    # Foydalanuvchini chat_id'larini set ga qo'shamiz
    chat_ids.add(message.chat.id)
    await message.answer("Assalomu aleykum! CRUD GROUP tomonidan yasalgan InSell botiga xush kelibsiz!")
