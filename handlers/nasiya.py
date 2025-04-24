import requests
import os
from aiogram import Router, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from services.nasiya_pdf import nasiya_pdf
from services.get_telegram import get_telegram_id

router = Router()

# 1. Foydalanuvchi komandasi bilan yuboriladigan versiya
@router.message(Command("n_hisobot"))
async def send_nasiya(message: Message, bot: Bot):
    await send_nasiya_silent(bot, message.chat.id)

# Barcha foydalanuvchilarga mahsulot hisobotini yuborish (silent)
async def send_nasiya_silent(bot: Bot, telegram_id: int):
    try:
        pdf_path = nasiya_pdf(telegram_id=telegram_id, logo_path='insell.png')

        if not os.path.exists(pdf_path):
            print(f"❌ {telegram_id} uchun fayl topilmadi.")
            return

        document = FSInputFile(path=pdf_path, filename=os.path.basename(pdf_path))
        await bot.send_document(chat_id=telegram_id, document=document)

        if os.path.exists(pdf_path):
            os.remove(pdf_path)

    except Exception as e:
        print(f"❌ {telegram_id} uchun nasiya hisobotini yuborishda xato: {e}")

