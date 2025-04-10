from datetime import date
from aiogram.types import FSInputFile
from services.generate_pdf import generate_pdf

async def send_daily_reports(bot):
    """Kunlik hisobotlarni pdf faylga aylantirish"""
    data = {
        "Sana": str(date.today()),
        "Umumiy foydalanuvchilar": 125,
        "Yangi foydalanuvchilar": 8,
        "Faol foydalanuvchilar": 67,
        "Yuborilgan xabarlar": 342
    }
    generated_pdf_file = generate_pdf(data=data, filename=f"hisobot_{date.today()}.pdf")
    pdf = FSInputFile(f"./hisobot_{date.today()}.pdf")
    await bot.send_document(chat_id="1586745967", document=pdf, caption="📄 Your daily PDF report")