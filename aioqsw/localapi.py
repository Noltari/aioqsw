"""QNAP QSW API."""
from __future__ import annotations

import asyncio
import base64
import json
import logging
from dataclasses import dataclass
from typing import Any, cast

from aiohttp import ClientSession, ContentTypeError
from aiohttp.client_reqrep import ClientResponse

from aioqsw.device import (
    FirmwareCheck,
    FirmwareCondition,
    FirmwareInfo,
    SystemBoard,
    SystemSensor,
    SystemTime,
)

from .const import (
    API_AUTHORIZATION,
    API_COMMAND,
    API_PASSWORD,
    API_PATH,
    API_PATH_V1,
    API_QSW_ID,
    API_QSW_LANG,
    API_REBOOT,
    API_RESULT,
    API_USERNAME,
    HTTP_CALL_TIMEOUT,
    QSD_FIRMWARE_CHECK,
    QSD_FIRMWARE_CONDITION,
    QSD_FIRMWARE_INFO,
    QSD_SYSTEM_BOARD,
    QSD_SYSTEM_SENSOR,
    QSD_SYSTEM_TIME,
)
from .exceptions import APIError, InvalidHost, InvalidResponse, LoginError, QswError

_LOGGER = logging.getLogger(__name__)


@dataclass
class ConnectionOptions:
    """QNAP QSW options for connection."""

    url: str
    user: str
    password: str


class QnapQswApi:
    """QNAP QSW API class."""

    def __init__(
        self,
        aiohttp_session: ClientSession,
        options: ConnectionOptions,
    ):
        """Device init."""
        self.aiohttp_session = aiohttp_session
        self.api_key: str | None = None
        self.cookies: dict[str, str] = {
            API_QSW_LANG: "ENG",
        }
        self.firmware_check: FirmwareCheck | None = None
        self.firmware_condition: FirmwareCondition | None = None
        self.firmware_info: FirmwareInfo | None = None
        self.headers: dict[str, str] = {}
        self.options = options
        self.system_board: SystemBoard | None = None
        self.system_sensor: SystemSensor | None = None
        self.system_time: SystemTime | None = None

    async def http_request_bytes(
        self, method: str, path: str, data: Any | None = None
    ) -> bytes:
        """Device HTTP request."""
        _LOGGER.debug("aiohttp request: /%s (params=%s)", path, data)

        resp: ClientResponse = await self.aiohttp_session.request(
            method,
            f"{self.options.url}/{path}",
            cookies=self.cookies,
            data=json.dumps(data),
            headers=self.headers,
            timeout=HTTP_CALL_TIMEOUT,
        )

        resp_bytes = await resp.read()

        if resp.status == 401:
            raise LoginError(f"Login error @ {method} /{path}")
        if resp.status != 200:
            raise APIError(f"API error @ {method} /{path} HTTP={resp.status}")

        return resp_bytes

    async def http_request(
        self, method: str, path: str, data: Any | None = None
    ) -> dict[str, Any]:
        """Device HTTP request."""
        _LOGGER.debug("aiohttp request: /%s (params=%s)", path, data)

        resp: ClientResponse = await self.aiohttp_session.request(
            method,
            f"{self.options.url}/{path}",
            cookies=self.cookies,
            data=json.dumps(data),
            headers=self.headers,
            timeout=HTTP_CALL_TIMEOUT,
        )

        resp_json = None
        try:
            resp_json = await resp.json()
        except ContentTypeError as err:
            raise InvalidResponse from err
        else:
            _LOGGER.debug("aiohttp response: %s", resp_json)

        if resp.status == 401:
            raise LoginError("Login error @ {method} /{path}")
        if resp.status != 200:
            raise APIError(
                f"API error @ {method} /{path} HTTP={resp.status} Resp={resp_json}"
            )

        return cast(dict[str, Any], resp_json)

    async def get_about(self) -> dict[str, Any]:
        """API GET about."""
        return await self.http_request("GET", f"{API_PATH}/about")

    async def get_firmware_condition(self) -> dict[str, Any]:
        """API GET firmware condition."""
        return await self.http_request("GET", f"{API_PATH_V1}/firmware/condition")

    async def get_firmware_info(self) -> dict[str, Any]:
        """API GET firmware info."""
        return await self.http_request("GET", f"{API_PATH_V1}/firmware/info")

    async def get_firmware_status(self) -> dict[str, Any]:
        """API GET firmware status."""
        return await self.http_request("GET", f"{API_PATH_V1}/firmware/status")

    async def get_firmware_update(self) -> dict[str, Any]:
        """API GET firmware update."""
        return await self.http_request("GET", f"{API_PATH_V1}/firmware/update")

    async def get_firmware_update_check(self) -> dict[str, Any]:
        """API GET firmware update check."""
        return await self.http_request("GET", f"{API_PATH_V1}/firmware/update/check")

    async def get_live(self) -> dict[str, Any]:
        """API GET live."""
        return await self.http_request("GET", f"{API_PATH}/live")

    async def get_users_verification(self) -> dict[str, Any]:
        """API GET users verification."""
        return await self.http_request("GET", f"{API_PATH_V1}/users/verification")

    async def get_system_board(self) -> dict[str, Any]:
        """API GET system board."""
        return await self.http_request("GET", f"{API_PATH_V1}/system/board")

    async def get_system_config(self) -> bytes:
        """API GET system config."""
        return await self.http_request_bytes("GET", f"{API_PATH_V1}/system/config")

    async def get_system_sensor(self) -> dict[str, Any]:
        """API GET system sensor."""
        return await self.http_request("GET", f"{API_PATH_V1}/system/sensor")

    async def get_system_time(self) -> dict[str, Any]:
        """API GET system time."""
        return await self.http_request("GET", f"{API_PATH_V1}/system/time")

    async def post_system_command(self, command: str) -> dict[str, Any]:
        """API POST system command."""
        params = {
            API_COMMAND: command,
        }
        return await self.http_request("POST", f"{API_PATH_V1}/system/command", params)

    async def post_users_exit(self) -> dict[str, Any]:
        """API POST users exit."""
        return await self.http_request("POST", f"{API_PATH_V1}/users/exit", {})

    async def post_users_login(self, params: dict[str, Any]) -> dict[str, Any]:
        """API POST users login."""
        return await self.http_request("POST", f"{API_PATH_V1}/users/login", params)

    async def check_firmware(self) -> FirmwareCheck:
        """Check QNAP QSW firmware version."""
        await self.login()

        fw_check = await self.get_firmware_update_check()
        self.firmware_check = FirmwareCheck(fw_check)

        return self.firmware_check

    async def config_backup(self) -> bytes:
        """Create a QNAP QSW config backup."""
        await self.login()

        return await self.get_system_config()

    async def reboot(self) -> bool:
        """Reboot QNAP QSW."""
        await self.login()

        response = await self.post_system_command(API_REBOOT)

        result = response.get(API_RESULT)
        if not result:
            raise APIError(f"Error when rebooting: {response}")

        return True

    async def validate(self) -> SystemBoard:
        """Validate QNAP QSW."""
        try:
            await self.get_live()
        except APIError as err:
            raise InvalidHost from err

        try:
            await self._login()
        except APIError as err:
            raise LoginError from err

        res = await self.get_system_board()
        return SystemBoard(res)

    async def update(self) -> None:
        """Update QNAP QSW."""
        await self.login()

        # Call system/sensor first since it takes a lot of time (~5s)
        system_sensor = asyncio.create_task(self.get_system_sensor())

        try:
            firmware_condition = await self.get_firmware_condition()
            self.firmware_condition = FirmwareCondition(firmware_condition)

            # Update firmware/info once
            if self.firmware_info is None:
                firmware_info = await self.get_firmware_info()
                self.firmware_info = FirmwareInfo(firmware_info)

            # Update system/board once
            if self.system_board is None:
                system_board = await self.get_system_board()
                self.system_board = SystemBoard(system_board)

            system_time = await self.get_system_time()
            self.system_time = SystemTime(system_time)
        except QswError as err:
            system_sensor.cancel()
            raise err
        else:
            self.system_sensor = SystemSensor(await system_sensor)

    def _login_clear(self) -> None:
        """Clear login data."""
        self.api_key = None
        if API_QSW_ID in self.cookies:
            del self.cookies[API_QSW_ID]
        if API_AUTHORIZATION in self.headers:
            del self.headers[API_AUTHORIZATION]
        self.firmware_info = None
        self.system_board = None

    def _login_required(self) -> bool:
        """Check if login is required."""
        return (
            not self.api_key
            or API_QSW_ID not in self.cookies
            or API_AUTHORIZATION not in self.headers
        )

    async def _login(self) -> None:
        """Perform a new user login."""
        self._login_clear()

        pass_utf8 = self.options.password.encode("utf-8")
        b64_pass = base64.b64encode(pass_utf8).decode("utf-8")
        params = {
            API_USERNAME: self.options.user,
            API_PASSWORD: b64_pass,
        }
        try:
            login = await self.post_users_login(params)
        except APIError as err:
            raise LoginError from err

        if API_RESULT not in login:
            raise LoginError("Invalid login response")

        self.api_key = str(login[API_RESULT])
        self.cookies[API_QSW_ID] = self.api_key
        self.headers[API_AUTHORIZATION] = f"Bearer {self.api_key}"

    async def login(self) -> None:
        """User login."""
        if self._login_required():
            await self._login()
        else:
            try:
                await self.get_users_verification()
            except LoginError:
                await self._login()

    async def logout(self) -> None:
        """User logout."""
        if not self._login_required():
            try:
                await self.post_users_exit()
            except APIError:
                pass

            self._login_clear()

    def data(self) -> dict[str, Any]:
        """Return QNAP QSW device data."""
        data: dict[str, Any] = {}

        if self.firmware_check is not None:
            firmware_check_data = self.firmware_check.data()
            if len(firmware_check_data) > 0:
                data[QSD_FIRMWARE_CHECK] = firmware_check_data

        if self.firmware_condition is not None:
            firmware_condition_data = self.firmware_condition.data()
            if len(firmware_condition_data) > 0:
                data[QSD_FIRMWARE_CONDITION] = firmware_condition_data

        if self.firmware_info is not None:
            firmware_info_data = self.firmware_info.data()
            if len(firmware_info_data) > 0:
                data[QSD_FIRMWARE_INFO] = firmware_info_data

        if self.system_board is not None:
            system_board_data = self.system_board.data()
            if len(system_board_data) > 0:
                data[QSD_SYSTEM_BOARD] = system_board_data

        if self.system_sensor is not None:
            system_sensor_data = self.system_sensor.data()
            if len(system_sensor_data) > 0:
                data[QSD_SYSTEM_SENSOR] = system_sensor_data

        if self.system_time is not None:
            system_time_data = self.system_time.data()
            if len(system_time_data) > 0:
                data[QSD_SYSTEM_TIME] = system_time_data

        return data
