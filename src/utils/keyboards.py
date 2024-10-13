from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def get_language_keyboard():
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="🇷🇺 Русский", callback_data="language:ru"))
    keyboard.add(InlineKeyboardButton(text="🇧🇾 Беларускі", callback_data="language:by"))

    return keyboard
