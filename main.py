import asyncio
import logging

from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from src.routers import get_routers
from src.database import setup_db
from src.utils.middlewares import UserLocaleMiddleware

from config import settings

dp = Dispatcher()


async def main() -> None:
    bot = Bot(
        token=settings.token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    dp.include_routers(*get_routers())

    dp.message.middleware(UserLocaleMiddleware())

    await setup_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

    with suppress(SystemExit, KeyboardInterrupt):
        asyncio.run(main())
