import os
from aiogram import Router, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from services.umumiy_pdf import umumiy_pdf

router = Router()

# Vaqt asosida barcha foydalanuvchilarga yuboriladigan funksiyasi
async def send_umumiy_silent(bot: Bot, telegram_id: int):
    try:
        pdf_path = umumiy_pdf(telegram_id=telegram_id, logo_path='insell.png')

        if not pdf_path or not os.path.exists(pdf_path):
            print(f"❌ {telegram_id} uchun umumiy hisobot fayli topilmadi.")
            return

        document = FSInputFile(path=pdf_path, filename=os.path.basename(pdf_path))
        await bot.send_document(chat_id=telegram_id, document=document)

        os.remove(pdf_path)
        print(f"✅ {telegram_id} uchun umumiy hisobot yuborildi.")

    except Exception as e:
        print(f"❌ {telegram_id} uchun umumiy hisobotni yuborishda xato: {e}")
