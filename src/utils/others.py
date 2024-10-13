import json

from typing import Dict

from src.database import Users


async def get_user_language(user_id: int) -> str:
    user = await Users.filter(uid=user_id).first()
    if not user:
        return "ru"

    return user.language


# async def get_phrases(language: str) -> Dict:
#     with open(f"data/locale/language.json", 'r', encoding='utf-8') as file:
#         translations = json.load(file)
#
#     return translations
