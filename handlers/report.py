from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from datetime import date
from services.generate_pdf import generate_pdf

router = Router()
chat_ids = set()

@router.message(Command('hisobot'))
async def send_daily_report(message: Message):
    # Hisobot ma'lumotlarini olish
    data = {
        "Sana": str(date.today()),
        "Umumiy foydalanuvchilar": 125,
        "Yangi foydalanuvchilar": 8,
        "Faol foydalanuvchilar": 67,
        "Yuborilgan xabarlar": 342
    }

    # PDF fayl yaratish
    filename = f"hisobot_{date.today()}.pdf"
    generate_pdf(data, filename)

    # PDFni yuborish
    pdf_file = FSInputFile(filename)
    await message.answer_document(pdf_file, caption="Kundalik hisobot tayyor!")

def get_chat_ids():
    return chat_ids