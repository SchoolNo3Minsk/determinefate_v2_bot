from typing import List

from .commands import start
from .commands import facts


def get_routers() -> List:
    return [
        start.router,
        facts.router
    ]
