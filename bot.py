import asyncio
import logging
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.handlers import register_handlers
from handlers.report import send_daily_reports

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# Register handlers
register_handlers(dp)

async def send_report():
    await send_daily_reports(bot)

# Start the bot
async def main():
    scheduler.add_job(send_report, trigger='cron', hour=15, minute=38)
    scheduler.start()

    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())  # Asenkron ishga tushirish
    except KeyboardInterrupt:
        print('Exit')
