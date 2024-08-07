"""QNAP QSW basic example."""

import asyncio
import json
import timeit

import _config
import aiohttp

from aioqsw.exceptions import APIError
from aioqsw.localapi import QnapQswApi


async def main():
    """QNAP QSW basic example."""

    async with aiohttp.ClientSession() as aiohttp_session:
        qsw = QnapQswApi(aiohttp_session, _config.QNAP_QSW_OPTIONS)
        try:
            system_board = await qsw.validate()
            if system_board is not None:
                print(f"System Board: {system_board.data()}")
            print("***")

            update_start = timeit.default_timer()
            await qsw.update()
            update_end = timeit.default_timer()
            print(json.dumps(qsw.data(), indent=4, sort_keys=True))
            print(f"Update time: {update_end - update_start}")
            print("***")

            print("Waiting 5 seconds to gather speed data")
            await asyncio.sleep(5)
            print("***")

            update_start = timeit.default_timer()
            await qsw.update()
            update_end = timeit.default_timer()
            print(json.dumps(qsw.data(), indent=4, sort_keys=True))
            print(f"Update time: {update_end - update_start}")
        except APIError:
            print("Invalid host.")


if __name__ == "__main__":
    asyncio.run(main())
