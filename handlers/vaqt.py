from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.user_settings import set_user_report_time

router = Router()

# 🔘 Soat tanlash uchun tugmalar
def get_hour_keyboard():
    builder = InlineKeyboardBuilder()
    for i in range(0, 24):
        builder.button(text=f"{i:02d}", callback_data=f"set_hour:{i}")
    builder.adjust(6)
    return builder.as_markup()

# 🔘 Minut tanlash uchun tugmalar
def get_minute_keyboard(hour: int):
    builder = InlineKeyboardBuilder()
    for m in range(0, 60, 5):
        builder.button(text=f"{m:02d}", callback_data=f"set_minute:{hour}:{m}")
    builder.adjust(6)
    return builder.as_markup()

@router.callback_query(F.data.startswith("set_hour:"))
async def handle_hour_selection(callback: CallbackQuery):
    hour = int(callback.data.split(":")[1])
    await callback.message.edit_text(
        f"🕒 Soat {hour:02d} tanlandi. Endi **minut**ni tanlang:",
        reply_markup=get_minute_keyboard(hour)
    )

@router.callback_query(F.data.startswith("set_minute:"))
async def handle_minute_selection(callback: CallbackQuery):
    _, hour, minute = callback.data.split(":")
    hour, minute = int(hour), int(minute)

    set_user_report_time(callback.from_user.id, hour, minute)
    await callback.message.edit_text(f"✅ Endi har kuni soat {hour:02d}:{minute:02d} da hisobot olasiz.")
