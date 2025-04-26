from aiogram import Dispatcher

from .start import router as start_router
from .mahsulot import router as mahsulot_router
from .kassa import router as kassa_router
from .nasiya import router as nasiya_router
from .umumiy import router as umumiy_router
from .vaqt import router as time_router
from .soat import router as soat_router
# from .soat import

def register_handlers(dp: Dispatcher):
    dp.include_router(mahsulot_router)
    dp.include_router(start_router)
    dp.include_router(kassa_router)
    dp.include_router(nasiya_router)
    dp.include_router(umumiy_router)
    dp.include_router(time_router)
    dp.include_router(soat_router)