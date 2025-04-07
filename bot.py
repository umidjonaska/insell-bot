import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

# Botni sozlab olish
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    await dp.start_polling()

if __name__ == '__main__':
    logging.baseConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())