import os
from aiogram import Router, Bot
from aiogram.types import FSInputFile
from services.kassa_pdf import kassa_pdf

router = Router()

# Bitta foydalanuvchiga kassa hisobotini yuborish
async def send_kassa_silent(bot: Bot, telegram_id: int):
    try:
        pdf_path = kassa_pdf(telegram_id=telegram_id, logo_path='insell.png')

        if not pdf_path or not os.path.exists(pdf_path):
            print(f"❌ {telegram_id} uchun hisobot fayli topilmadi.")
            return

        document = FSInputFile(path=pdf_path, filename=os.path.basename(pdf_path))
        await bot.send_document(chat_id=telegram_id, document=document)

        os.remove(pdf_path)
        print(f"✅ {telegram_id} uchun kassa hisoboti yuborildi.")

    except Exception as e:
        print(f"❌ {telegram_id} uchun kassa hisobotini yuborishda xato: {e}")
