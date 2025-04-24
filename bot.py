import asyncio
import logging
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers.handlers import register_handlers

# Hisobot yuboruvchi funksiyalar
from handlers.kassa import send_kassa_silent
from handlers.nasiya import send_nasiya_silent
from handlers.mahsulot import send_mahsulot_silent
from handlers.umumiy import send_umumiy_silent
from services.get_telegram import get_telegram_id

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
scheduler = AsyncIOScheduler()

register_handlers(dp)

# Barcha foydalanuvchilarga barcha hisobotlarni yuborish
async def send_reports_for_users():
    try:
        users = await get_telegram_id()
        for user in users:
            chat_id = user['telegram_id']
            await send_kassa_silent(bot, chat_id)
            await send_nasiya_silent(bot, chat_id)
            await send_mahsulot_silent(bot, chat_id)
            await send_umumiy_silent(bot, chat_id)
    except Exception as e:
        print(f"Hisobotlarni yuborishda xato: {e}")


async def main():
    scheduler.add_job(
        send_reports_for_users,
        trigger='cron', hour=14, minute=18, second=20
    )
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
