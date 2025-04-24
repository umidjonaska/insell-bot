import os
from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from services.kassa_pdf import kassa_pdf
from services.mahsulot_pdf import mahsulot_pdf
from services.nasiya_pdf import nasiya_pdf
from services.umumiy_pdf import umumiy_pdf

router = Router()

@router.message(CommandStart())
async def start_command(message: Message):
    print("✅ /start komandasi kelib tushdi") 
    telegram_id = message.chat.id  # Telegram ID

    # PDF fayllar va ularning funksiyalari ro‘yxati
    pdf_generators = [
        ("Umumiy PDF", umumiy_pdf),
        ("Kassa PDF", kassa_pdf),
        ("Mahsulot PDF", mahsulot_pdf),
        ("Nasiya PDF", nasiya_pdf)
    ]

    pdf_paths = []

    # PDF fayllarni yaratish
    for label, pdf_func in pdf_generators:
        pdf_path = pdf_func(telegram_id, logo_path='insell.png')
        if pdf_path:
            pdf_paths.append(pdf_path)
            print(f"{label}: {pdf_path}")
        else:
            print(f"{label} yaratilmadi")

    # PDF fayllarni yuborish
    for pdf_path in pdf_paths:
        if os.path.exists(pdf_path):
            document = FSInputFile(path=pdf_path, filename=os.path.basename(pdf_path))
            await message.answer_document(document)
            os.remove(pdf_path)  # Yuborilgandan so‘ng o‘chirish
        else:
            await message.answer("PDF fayl mavjud emas")

    # Xush kelibsiz xabar
    await message.answer(
        f"👋 Assalomu alaykum!\n"
        f"CRUD GROUP tomonidan yasalgan InSell botiga xush kelibsiz!\n"
        f"Sizning chat ID'ingiz: <code>{telegram_id}</code>"
    )
