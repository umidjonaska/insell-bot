from aiogram import Router, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from services.kassa_pdf import generate_pdf
import os

router = Router()

# 1. Komandaga javob beruvchi funksiya
@router.message(Command("k_hisobot"))
async def send_kassa(message: Message, bot: Bot):
    pdf_path = generate_pdf(logo_path='insell.png')
    document = FSInputFile(path=pdf_path, filename=os.path.basename(pdf_path))

    await bot.send_document(chat_id=message.chat.id, document=document)

    if os.path.exists(pdf_path):
        os.remove(pdf_path)

# 2. Silent versiya — cron uchun
async def send_kassa_silent(bot: Bot):
    chat_id = 6951699115
    pdf_path = generate_pdf(logo_path='insell.png')
    document = FSInputFile(path=pdf_path, filename=os.path.basename(pdf_path))

    await bot.send_document(chat_id=chat_id, document=document)

    if os.path.exists(pdf_path):
        os.remove(pdf_path)
