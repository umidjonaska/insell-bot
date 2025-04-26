import os
from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart

from handlers.vaqt import get_hour_keyboard  # eski vaqt emas!
from handlers.vaqt import get_hour_keyboard
from services.kassa_pdf import kassa_pdf
from services.mahsulot_pdf import mahsulot_pdf
from services.nasiya_pdf import nasiya_pdf
from services.umumiy_pdf import umumiy_pdf

router = Router()
CHAT_ID_FILE = "chat_id.txt"

@router.message(CommandStart())
async def start_command(message: Message):
    telegram_id = message.chat.id

    try:
        existing_ids = set()
        if os.path.exists(CHAT_ID_FILE):
            with open(CHAT_ID_FILE, "r", encoding="utf-8") as f:
                existing_ids = set(line.strip() for line in f if line.strip())

        if str(telegram_id) not in existing_ids:
            with open(CHAT_ID_FILE, "a", encoding="utf-8") as f:
                f.write(f"{telegram_id}\n")
    except Exception as e:
        print(f"❌ Chat ID saqlashda xato: {e}")

    await message.answer(
        f"👋 Assalomu alaykum!\n"
        f"CRUD GROUP tomonidan yasalgan InSell botiga xush kelibsiz!\n"
        f"Sizning chat ID'ingiz: {telegram_id}\n"
    )

    loading_message = await message.answer("⏳ Hisobotlar tayyorlanmoqda...")

    pdf_generators = [
        ("Umumiy PDF", umumiy_pdf),
        ("Kassa PDF", kassa_pdf),
        ("Mahsulot PDF", mahsulot_pdf),
        ("Nasiya PDF", nasiya_pdf)
    ]

    pdf_paths = []
    for label, func in pdf_generators:
        path = func(telegram_id, logo_path='insell.png')
        if path:
            pdf_paths.append(path)

    for path in pdf_paths:
        if os.path.exists(path):
            doc = FSInputFile(path=path, filename=os.path.basename(path))
            await message.answer_document(doc)
            os.remove(path)
        else:
            await message.answer("PDF fayl topilmadi")

    await loading_message.delete()
    await message.answer("🕒 Hisobotni qaysi **soat**da olishni xohlaysiz?", reply_markup=get_hour_keyboard())
