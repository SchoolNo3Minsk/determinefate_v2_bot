import json
import random

from typing import Tuple

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

LANGUAGES = {"ru": "Русский", "by": "Беларускі"}

PHRASES_FILE = open("data/locale/locale.json", "r", encoding="utf-8")
PHRASES_JSON = json.load(PHRASES_FILE)

FACTS_FILE = open("data/locale/facts.json", "r", encoding="utf-8")
FACTS_JSON = json.load(FACTS_FILE)


def get_language_name(language: str) -> str:
    return LANGUAGES[language]


def get_phrase(language: str, phrase: str) -> str:
    return PHRASES_JSON.get(language).get(phrase)


def get_fact(language: str) -> Tuple[str, str]:
    fact = random.choice(FACTS_JSON.get(language))
    return fact["fact"], fact["description"]


def check_canceled(function):
    async def decorator_access(message: Message, state: FSMContext, locale: str):
        if message.text == "❌Отмена" or message.text == "❌Адмена":
            await state.clear()

            return await message.reply(
                text=f"⛔ {get_phrase(locale, "error_cancel")}",
                reply_markup=ReplyKeyboardRemove()
            )

        return await function(message, state, locale)

    return decorator_access

