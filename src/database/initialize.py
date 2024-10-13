from tortoise import Tortoise

from config import settings


async def setup_db() -> None:
    await Tortoise.init(
        db_url=settings.db_url.get_secret_value(),
        modules={
            "models": [
                "src.database.models.users"
                # "src.utils.database.models.queries"
            ]
        },
        timezone='Europe/Minsk',
    )

    await Tortoise.generate_schemas()


async def close_db() -> None:
    await Tortoise.close_connections()
