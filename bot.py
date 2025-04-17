import asyncio
import logging
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.handlers import register_handlers
from handlers.mahsulot import send_mahsulot_silent
from handlers.kassa import send_kassa_silent
from handlers.nasiya import send_nasiya_silent
from handlers.umumiy import send_umumiy_silent

# Bot va Dispatcher obyektlarini yaratamiz
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# Handlalarni ro'yxatdan o'tkazamiz
register_handlers(dp)

# Hisobot yuboruvchi asosiy funksiya
async def send_report():
    await send_mahsulot_silent(bot)
    await send_kassa_silent(bot)
    await send_nasiya_silent(bot)
    await send_umumiy_silent(bot)

# Botni ishga tushirish funksiyasi
async def main():
    # Har kuni belgilangan vaqtda hisobotlarni yuborish uchun cron job qo'shamiz
    scheduler.add_job(send_report, trigger='cron', hour=17, minute=52)  # O'zingga kerakli vaqtni qo'y
    scheduler.start()

    await dp.start_polling(bot)

# Kirish nuqtasi
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
