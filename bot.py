import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.handlers import register_handlers
from handlers.schedule import start_scheduler  # start_scheduler import qilinadi

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Register handlers
register_handlers(dp)

# Start the bot
async def main():
    await dp.start_polling(bot)
    await start_scheduler(bot)
    print(start_scheduler(bot))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())  # Asenkron ishga tushirish
    except KeyboardInterrupt:
        print('Exit')
