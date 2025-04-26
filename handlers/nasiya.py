import os
from aiogram import Router, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from services.nasiya_pdf import nasiya_pdf

router = Router()

# Vaqt asosida chaqiriladigan versiya
async def send_nasiya_silent(bot: Bot, telegram_id: int):
    try:
        pdf_path = nasiya_pdf(telegram_id=telegram_id, logo_path='insell.png')

        if not pdf_path or not os.path.exists(pdf_path):
            print(f"❌ {telegram_id} uchun nasiya hisobot fayli topilmadi.")
            return

        document = FSInputFile(path=pdf_path, filename=os.path.basename(pdf_path))
        await bot.send_document(chat_id=telegram_id, document=document)

        os.remove(pdf_path)
        print(f"✅ {telegram_id} uchun nasiya hisobot yuborildi.")

    except Exception as e:
        print(f"❌ {telegram_id} uchun nasiya hisobotini yuborishda xato: {e}")
