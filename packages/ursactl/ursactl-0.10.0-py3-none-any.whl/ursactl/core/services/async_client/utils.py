import asyncio
from concurrent.futures import FIRST_COMPLETED


class DONE:
    pass


async def get_unless_done(coro, done_future):
    getter_future = asyncio.ensure_future(coro)
    done, pending = await asyncio.wait(
        [getter_future, done_future], return_when=FIRST_COMPLETED
    )
    if done_future in done:
        if not getter_future.done():
            (getter,) = pending
            getter.cancel()
        return DONE
    return await getter_future
