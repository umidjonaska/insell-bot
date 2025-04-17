from aiogram import Router, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from services.umumiy_pdf import generate_pdf
import os

router = Router()

@router.message(Command("u_hisobot"))
async def send_umumiy_silent(bot: Bot):
    chat_id = 6951699115
    pdf_path = generate_pdf(logo_path='insell.png')
    document = FSInputFile(path=pdf_path, filename=os.path.basename(pdf_path))

    await bot.send_document(chat_id=chat_id, document=document)

    if os.path.exists(pdf_path):
        os.remove(pdf_path)
