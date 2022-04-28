"""QNAP QSW config backup example."""
import asyncio
import json
import os

import _config
import aiohttp

from aioqsw.exceptions import APIError
from aioqsw.localapi import QnapQswApi


async def main():
    """QNAP QSW config backup example."""

    async with aiohttp.ClientSession() as aiohttp_session:
        qsw = QnapQswApi(aiohttp_session, _config.QNAP_QSW_OPTIONS)
        try:
            system_board = await qsw.validate()
            if system_board is not None:
                print(f"System Board: {system_board.data()}")

            await qsw.update()
            print(json.dumps(qsw.data(), indent=4, sort_keys=True))

            print("Checking QNAP QSW firmware update...")
            cfg_backup = await qsw.config_backup()
            if cfg_backup:
                cfg_backup_path = os.path.dirname(os.path.abspath(__file__))
                cfg_backup_file = open(f"{cfg_backup_path}/qsw.conf", "wb")
                cfg_backup_file.write(cfg_backup)
                cfg_backup_file.close()
        except APIError:
            print("Invalid host.")


if __name__ == "__main__":
    asyncio.run(main())
