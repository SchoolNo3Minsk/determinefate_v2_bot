from typing import List

from .commands import find
from .commands import start
from .commands import facts


def get_routers() -> List:
    return [
        find.router,
        start.router,
        facts.router
    ]
