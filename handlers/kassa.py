import requests
import os
from aiogram import Router, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from services.kassa_pdf import kassa_pdf
from services.get_telegram import get_telegram_id  # get_telegram_id import qilingan

router = Router()

@router.message(Command("k_hisobot"))
async def send_kassa(message: Message, bot: Bot):
    # PDF yaratish
    pdf_path = kassa_pdf(telegram_id=message.from_user.id, logo_path='insell.png')

    if not os.path.exists(pdf_path):
        await message.answer("❌ Hisobot yaratishda xatolik yuz berdi.")
        return

    # PDFni yuborish
    document = FSInputFile(path=pdf_path, filename=os.path.basename(pdf_path))
    await bot.send_document(chat_id=message.chat.id, document=document)

    if os.path.exists(pdf_path):
        os.remove(pdf_path)

# Barcha foydalanuvchilarga mahsulot hisobotini yuborish (silent)
async def send_kassa_silent(bot: Bot, telegram_id: int):
    try:
        pdf_path = kassa_pdf(telegram_id=telegram_id, logo_path='insell.png')

        if not pdf_path or not os.path.exists(pdf_path):
            print(f"{telegram_id} uchun hisobot fayli topilmadi.")
            return

        document = FSInputFile(path=pdf_path, filename=os.path.basename(pdf_path))
        await bot.send_document(chat_id=telegram_id, document=document)

        if os.path.exists(pdf_path):
            os.remove(pdf_path)

    except Exception as e:
        print(f"{telegram_id} uchun kassa hisobotini yuborishda xatolik: {e}")
