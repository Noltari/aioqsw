"""QNAP QSW reboot example."""

import asyncio
import json

import _config
import aiohttp

from aioqsw.exceptions import APIError
from aioqsw.localapi import QnapQswApi


async def main():
    """QNAP QSW reboot example."""

    async with aiohttp.ClientSession() as aiohttp_session:
        qsw = QnapQswApi(aiohttp_session, _config.QNAP_QSW_OPTIONS)
        try:
            system_board = await qsw.validate()
            if system_board is not None:
                print(f"System Board: {system_board.data()}")

            await qsw.update()
            print(json.dumps(qsw.data(), indent=4, sort_keys=True))

            print("Rebooting QNAP QSW...")
            await qsw.reboot()
        except APIError:
            print("Invalid host.")


if __name__ == "__main__":
    asyncio.run(main())
