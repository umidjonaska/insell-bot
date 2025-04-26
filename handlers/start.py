import os
from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from services.kassa_pdf import kassa_pdf
from services.mahsulot_pdf import mahsulot_pdf
from services.nasiya_pdf import nasiya_pdf
from services.umumiy_pdf import umumiy_pdf
# from services.user_settings import get_user_report_time
from services.user_settings import set_user_report_time

router = Router()

CHAT_ID_FILE = "chat_id.txt"

@router.message(CommandStart())
async def start_command(message: Message):
    print("✅ /start komandasi kelib tushdi")
    telegram_id = message.chat.id  # Telegram ID

    # --- chat_id.txt ichida faqat noyob ID saqlash ---
    try:
        existing_ids = set()
        if os.path.exists(CHAT_ID_FILE):
            with open(CHAT_ID_FILE, "r", encoding="utf-8") as f:
                existing_ids = set(line.strip() for line in f if line.strip())

        if str(telegram_id) not in existing_ids:
            with open(CHAT_ID_FILE, "a", encoding="utf-8") as f:
                f.write(f"{telegram_id}\n")
            print(f"✅ Yangi Chat ID {telegram_id} saqlandi.")
        else:
            print(f"ℹ️ Chat ID {telegram_id} allaqachon mavjud.")
    except Exception as e:
        print(f"❌ Chat ID saqlashda xato: {e}")

    # 🟢 BIRINCHI: Xush kelibsiz xabar
    await message.answer(
        f"👋 Assalomu alaykum!\n"
        f"CRUD GROUP tomonidan yasalgan InSell botiga xush kelibsiz!\n"
        f"Sizning chat ID'ingiz: {telegram_id}\n\n"
    )

    # ⏳ Oraliq xabar: tayyorlanmoqda
    loading_message = await message.answer("⏳ Iltimos kuting, siz uchun PDF hisobotlar tayyorlanmoqda...")

    # PDF generator funksiyalari ro‘yxati
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

    # ⏳ Oraliq xabarni o'chirish
    await loading_message.delete()

    # Foydalanuvchidan vaqtni belgilashni so'rash
    await message.answer(
        "🕒 Endi, hisobotni qaysi soat va minutda olishni xohlasangiz, shuni yuboring.\n"
        "Masalan: `10 30` (10 soat, 30 minut) kabi."
    )

@router.message(lambda message: message.text and len(message.text.split()) == 2)
async def set_report_time(message: Message):
    try:
        hour, minute = map(int, message.text.split())
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            raise ValueError

        # Foydalanuvchi tanlagan vaqtda hisobot yuborish uchun saqlaymiz
        set_user_report_time(message.from_user.id, hour, minute)
        await message.answer(f"✅ Hisobotni endi soat {hour}:{minute} da olasiz.")
    except ValueError:
        await message.answer("Iltimos, soat va minutni to‘g‘ri formatda kiriting: `soat minut` (masalan, 10 30).")
