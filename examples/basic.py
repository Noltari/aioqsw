"""Basic QNAP QSW client example."""
import asyncio
import json

import _config
import aiohttp

from aioqsw.exceptions import APIError
from aioqsw.localapi import QnapQswApi


async def main():
    """Basic QNAP QSW client example."""

    async with aiohttp.ClientSession() as aiohttp_session:
        client = QnapQswApi(aiohttp_session, _config.QNAP_QSW_OPTIONS)
        try:
            system_board = await client.validate()
            if system_board is not None:
                print(f"System Board: {system_board.data()}")
            await client.update()
            print(json.dumps(client.data(), indent=4, sort_keys=True))
        except APIError:
            print("Invalid host.")


if __name__ == "__main__":
    asyncio.run(main())
