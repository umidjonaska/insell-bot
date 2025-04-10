from aiogram import Dispatcher
from .start import router as start_router
from .report import router as report_router

def register_handlers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(report_router)
