from typing import List

from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from src.utils.others import get_phrase


def get_language_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="🇷🇺 Русский", callback_data="language:ru"))
    keyboard.add(InlineKeyboardButton(text="🇧🇾 Беларускі", callback_data="language:by"))

    return keyboard


def accept_keyboard(language: str) -> List[List[KeyboardButton]]:
    return [
        [
            KeyboardButton(text=f"➡️Да")
        ],
        [
            KeyboardButton(text=f"❌ {get_phrase(language, "cancel")}")
        ]
    ]


def cancel_keyboard(language: str) -> List[List[KeyboardButton]]:
    return [
        [
            KeyboardButton(
                text=f"❌ {get_phrase(language, "cancel")}"
            )
        ]
    ]


def skip_or_cancel_keyboard(language: str) -> List[List[KeyboardButton]]:
    return [
        [
            KeyboardButton(text=f"➡️{get_phrase(language, "skip")}")
        ],
        [
            KeyboardButton(text=f"❌ {get_phrase(language, "cancel")}")
        ]
    ]
