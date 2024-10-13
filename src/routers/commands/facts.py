from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from src.utils.others import get_fact

router = Router()


@router.message(Command("facts"))
async def facts(message: Message, locale: str):
    fact = get_fact(locale)
    await message.answer(f"<b>{fact[0]}</b>\n\n{fact[1]}")
