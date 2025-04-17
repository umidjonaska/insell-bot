from aiogram import Router, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from services.mahsulot_pdf import generate_pdf
import os

router = Router()

# 1️⃣ Foydalanuvchi komanda orqali yuborsa
@router.message(Command("m_hisobot"))
async def send_mahsulot_command(message: Message, bot: Bot):
    await send_mahsulot_silent(bot, message.chat.id)

# 2️⃣ Scheduler orqali yuboriladigan variant
async def send_mahsulot_silent(bot: Bot, chat_id: int = 6951699115):
    pdf_path = generate_pdf(logo_path='insell.png')
    document = FSInputFile(path=pdf_path, filename=os.path.basename(pdf_path))

    await bot.send_document(chat_id=chat_id, document=document)

    if os.path.exists(pdf_path):
        os.remove(pdf_path)
