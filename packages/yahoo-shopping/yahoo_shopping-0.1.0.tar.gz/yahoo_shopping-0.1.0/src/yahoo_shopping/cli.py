import asyncio
import functools
from collections.abc import Coroutine
from copy import copy
from typing import Any, Callable, ParamSpec, TypeVar

import cyclopts
from nest_asyncio import apply
from rich import print

from ._main import YahooShopping

apply()

P = ParamSpec("P")
TReturn = TypeVar("TReturn")


def _prints(f: Callable[P, Coroutine[Any, Any, TReturn]]) -> Callable[P, TReturn]:
    @functools.wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> TReturn:
        result = asyncio.run(f(*args, **kwargs))
        print(result)
        return result

    return wrapper


async def _main() -> int:
    app = cyclopts.App(name="yahoo-shopping", help="Yahoo! Shopping API CLI")
    # ys = await YahooShopping().__aenter__()
    async with YahooShopping() as ys:
        for f in [
            ys.itemSearch,
            ys.highRatingTrendRanking,
            ys.itemLookup,
            ys.categorySearch,
            ys.queryRanking,
            ys.getModule,
            ys.reviewSearch,
            ys.searchScrape,
            ys.itemScrape,
            ys.itemPrice,
        ]:
            f_ = copy(f)
            app.command()(_prints(f_))
        app()
    return 0


def main() -> int:
    return asyncio.run(_main())
