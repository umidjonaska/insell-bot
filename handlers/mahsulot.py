import os
from aiogram import Router, Bot
from aiogram.types import FSInputFile
from aiogram.types import Message
from aiogram.filters import Command
from services.mahsulot_pdf import mahsulot_pdf

router = Router()

# Vaqt bo‘yicha avtomatik chaqiriladigan funksiya
async def send_mahsulot_silent(bot: Bot, telegram_id: int):
    try:
        pdf_path = mahsulot_pdf(telegram_id=telegram_id, logo_path='insell.png')

        if not pdf_path or not os.path.exists(pdf_path):
            print(f"❌ {telegram_id} uchun mahsulot hisobot fayli topilmadi.")
            return

        document = FSInputFile(path=pdf_path, filename=os.path.basename(pdf_path))
        await bot.send_document(chat_id=telegram_id, document=document)

        os.remove(pdf_path)
        print(f"✅ {telegram_id} uchun mahsulot hisobot yuborildi.")

    except Exception as e:
        print(f"❌ {telegram_id} uchun mahsulot hisobotini yuborishda xato: {e}")
