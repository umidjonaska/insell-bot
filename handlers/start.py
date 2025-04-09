from aiogram import Router, types
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command
from datetime import date
from service.test import generate_pdf

router = Router()
chat_ids = set()  # Bu yerda barcha foydalanuvchilarning chat_id'lari saqlanadi

@router.message(CommandStart())
async def start_command(message: Message):
    # Foydalanuvchini chat_id'larini set ga qo'shamiz
    chat_ids.add(message.chat.id)
    await message.answer("Assalomu aleykum! CRUD GROUP tomonidan yasalgan InSell botiga xush kelibsiz!")

@router.message(Command('hisobot'))
async def send_daily_report(message: types.Message):
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
