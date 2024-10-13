import random

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


router = Router()


@router.message(Command("facts"))
async def facts(message: Message):
    # random_fact = random.choice(FACTS)
    await message.answer("test")
