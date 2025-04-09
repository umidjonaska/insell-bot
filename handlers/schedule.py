from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import datetime
import os
from config import REPORT_TIME
from .start import get_chat_ids
from service.api import fetch_report_data
from service.test import generate_pdf

# Asenkron hisobot yuborish funksiyasi
async def send_report(bot):
    data = fetch_report_data()
    if data:
        today = datetime.date.today().strftime("%Y-%m-%d")
        filename = f"hisobot_{today}.pdf"
        generate_pdf(data, filename)

        for chat_id in get_chat_ids():
            with open(filename, "rb") as doc:
                await bot.send_document(chat_id, doc, caption=f"{today} uchun hisobot")
        os.remove(filename)

# Jobni har kuni ishga tushirish uchun
def schedule_job(bot):
    scheduler = AsyncIOScheduler()
    # Har kunni intervalda ishga tushirish (REPORTED_TIME va vaqtni sozlash)
    scheduler.add_job(lambda: asyncio.create_task(send_report(bot)), 'interval', days=1, start_date=REPORT_TIME)
    scheduler.start()

# schedulerning infinite loop funksiyasi
async def start_scheduler(bot):
    schedule_job(bot)
    print(f"{schedule_job}  bu schedule.py")
    while True:
        await asyncio.sleep(1)
