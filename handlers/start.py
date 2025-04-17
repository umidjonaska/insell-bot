from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def start_command(message: Message):
    chat_id = message.chat.id
    await message.answer(f"Assalomu aleykum! CRUD GROUP tomonidan yasalgan InSell botiga xush kelibsiz! Sizning chat ID'ingiz: {chat_id}")