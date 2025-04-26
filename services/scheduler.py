import os
from datetime import datetime
from aiogram.types import FSInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.kassa_pdf import kassa_pdf
from services.mahsulot_pdf import mahsulot_pdf
from services.nasiya_pdf import nasiya_pdf
from services.umumiy_pdf import umumiy_pdf

CHAT_ID_FILE = "chat_id.txt"

def get_users_from_file():
    users = []
    if os.path.exists(CHAT_ID_FILE):
        with open(CHAT_ID_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    user_info = line.strip().split(",")
                    if len(user_info) == 3:
                        chat_id = int(user_info[0])
                        hour = int(user_info[1])
                        minute = int(user_info[2])
                        users.append({"telegram_id": chat_id, "hour": hour, "minute": minute})
    return users

async def send_reports_for_users(bot):
    try:
        users = get_users_from_file()
        now = datetime.now()
        for user in users:
            if user["hour"] == now.hour and user["minute"] == now.minute:
                chat_id = user["telegram_id"]
                print(f"Hisobot yuborilmoqda: {chat_id}")
                pdf_generators = [
                    ("Umumiy PDF", umumiy_pdf),
                    ("Kassa PDF", kassa_pdf),
                    ("Mahsulot PDF", mahsulot_pdf),
                    ("Nasiya PDF", nasiya_pdf)
                ]

                pdf_paths = []
                for label, func in pdf_generators:
                    path = func(chat_id, logo_path="insell.png")
                    if path:
                        pdf_paths.append(path)
                        print(f"{label}: {path}")
                    else:
                        print(f"{label} yaratilmadi")

                for path in pdf_paths:
                    if os.path.exists(path):
                        document = FSInputFile(path=path, filename=os.path.basename(path))
                        await bot.send_document(chat_id=chat_id, document=document)
                        os.remove(path)
                    else:
                        await bot.send_message(chat_id=chat_id, text="PDF fayl mavjud emas")
    except Exception as e:
        print(f"❌ Hisobot yuborishda xato: {e}")

async def setup_scheduler(bot):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_reports_for_users,
        trigger="cron",
        hour="*",
        minute="*",
        second="0",
        args=[bot]
    )
    scheduler.start()
