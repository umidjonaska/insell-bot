import asyncio
import os
from datetime import date
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from config import DEFAULT_CHAT_IDS
#from .start import chat_ids
from services.api import fetch_report_data
from services.generate_pdf import generate_pdf


# Asenkron hisobot yuborish funksiyasi
async def send_report(bot):
    await start_pdf_scheduler(bot)
    print(await start_pdf_scheduler(bot))
    data = {
        "Sana": str(date.today()),
        "Umumiy foydalanuvchilar": 125,
        "Yangi foydalanuvchilar": 8,
        "Faol foydalanuvchilar": 67,
        "Yuborilgan xabarlar": 342
    }
    if data:
        #today = datetime.date.today().strftime("%Y-%m-%d")
        filename = "hisobot.pdf"
        generate_pdf(data, filename)

        for chat_id in DEFAULT_CHAT_IDS:
            with open(filename, "rb") as doc:
                await bot.send_document(chat_id, doc, caption=f"{date.today()} uchun hisobot")
        os.remove(filename)


# PDF yuborish ishini rejalashtirish
async def start_pdf_scheduler(bot):
    scheduler = AsyncIOScheduler()

    # Cron trigger — har kuni 13:41 da
    trigger = CronTrigger(hour=16, minute=6, timezone='Asia/Tashkent')

    # Asenkron ishni scheduler bilan belgilaymiz
    scheduler.add_job(send_report, trigger, args=[bot])
    print(send_report)
    scheduler.start()


# Infinite loop bilan scheduler'ni ishga tushurish
async def start_scheduler(bot):
    start_pdf_scheduler(bot)
    while True:
        await asyncio.sleep(1)
