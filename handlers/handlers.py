from aiogram import Dispatcher
from .start import router as start_router
from .schedule import start_scheduler  # start_scheduler ni alohida import qilamiz

def register_handlers(dp: Dispatcher):
    dp.include_router(start_router)  # start_router routerini qo‘shish
    # start_scheduler ni register qilishning hojati yo‘q, uni alohida ishga tushirish kerak
