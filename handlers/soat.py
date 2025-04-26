from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandObject, Command
from services.user_settings import set_user_report_time

router = Router()

@router.message(Command("soat"))
async def set_hour(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("🕘 Hisobot soatini belgilash: /soat 10 (0-23)")
        return

    try:
        hour = int(command.args.strip())
        if hour < 0 or hour > 23:
            raise ValueError()
    except ValueError:
        await message.answer("❌ Soat noto‘g‘ri. Iltimos 0-23 orasida kiriting.")
        return

    set_user_report_time(message.from_user.id, hour, 0)
    await message.answer(f"✅ Endi siz har kuni soat {hour}:00 da hisobot olasiz.")
