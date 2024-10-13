from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.database import Users


class UserLocaleMiddleware(BaseMiddleware):
    def __init__(self):
        self.locale = "ru"

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        base = await Users.filter(uid=data["event_from_user"].id).first()
        if base:
            self.locale = base.language

        data["locale"] = self.locale
        return await handler(event, data)
