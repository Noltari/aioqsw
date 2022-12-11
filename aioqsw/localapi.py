"""QNAP QSW API."""
from __future__ import annotations

import asyncio
import base64
import json
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, cast

from aiohttp import ClientSession, ContentTypeError
from aiohttp.client_exceptions import ClientConnectorError
from aiohttp.client_reqrep import ClientResponse

from aioqsw.device import (
    FirmwareCheck,
    FirmwareCondition,
    FirmwareInfo,
    LACPInfo,
    PortsStatistics,
    PortsStatus,
    SystemBoard,
    SystemSensor,
    SystemTime,
)

from .const import (
    API_AUTHORIZATION,
    API_COMMAND,
    API_DONE,
    API_DOWNLOAD_SIZE,
    API_FIRMWARE_SIZE,
    API_NONE,
    API_PASSWORD,
    API_PATH,
    API_PATH_V1,
    API_PROGRESS,
    API_QSW_ID,
    API_QSW_LANG,
    API_REBOOT,
    API_RESULT,
    API_USERNAME,
    HTTP_CALL_TIMEOUT,
    QSD_FIRMWARE_CHECK,
    QSD_FIRMWARE_CONDITION,
    QSD_FIRMWARE_INFO,
    QSD_PORTS_STATISTICS,
    QSD_PORTS_STATUS,
    QSD_SYSTEM_BOARD,
    QSD_SYSTEM_SENSOR,
    QSD_SYSTEM_TIME,
)
from .exceptions import (
    APIError,
    InternalServerError,
    InvalidHost,
    InvalidResponse,
    LoginError,
    QswError,
)

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
        self._first_update: bool = True
        self.aiohttp_session = aiohttp_session
        self.api_key: str | None = None
        self.cookies: dict[str, str] = {
            API_QSW_LANG: "ENG",
        }
        self.firmware_check: FirmwareCheck | None = None
        self.firmware_condition: FirmwareCondition | None = None
        self.firmware_info: FirmwareInfo | None = None
        self.firmware_progress: float = 0.0
        self.headers: dict[str, str] = {}
        self.lacp_info: LACPInfo | None = None
        self.options = options
        self.ports_statistics: PortsStatistics | None = None
        self.ports_status: PortsStatus | None = None
        self.system_board: SystemBoard | None = None
        self.system_sensor: SystemSensor | None = None
        self.system_time: SystemTime | None = None

    async def http_request_bytes(
        self, method: str, path: str, data: Any | None = None
    ) -> bytes:
        """Device HTTP request."""
        _LOGGER.debug("aiohttp request: /%s (params=%s)", path, data)

        try:
            resp: ClientResponse = await self.aiohttp_session.request(
                method,
                f"{self.options.url}/{path}",
                cookies=self.cookies,
                data=json.dumps(data),
                headers=self.headers,
                timeout=HTTP_CALL_TIMEOUT,
            )
        except ClientConnectorError as err:
            raise InvalidHost from err

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

        try:
            resp: ClientResponse = await self.aiohttp_session.request(
                method,
                f"{self.options.url}/{path}",
                cookies=self.cookies,
                data=json.dumps(data),
                headers=self.headers,
                timeout=HTTP_CALL_TIMEOUT,
            )
        except ClientConnectorError as err:
            raise InvalidHost from err

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
            if resp.status == 500:
                raise InternalServerError(
                    f"Internal server error @ {method} /{path} HTTP={resp.status} Resp={resp_json}"
                )
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

    async def get_lacp_info(self) -> dict[str, Any]:
        """API GET LACP info."""
        return await self.http_request("GET", f"{API_PATH_V1}/lacp/info")

    async def get_live(self) -> dict[str, Any]:
        """API GET live."""
        return await self.http_request("GET", f"{API_PATH}/live")

    async def get_ports_statistics(self) -> dict[str, Any]:
        """API GET ports status."""
        return await self.http_request("GET", f"{API_PATH_V1}/ports/statistics")

    async def get_ports_status(self) -> dict[str, Any]:
        """API GET ports status."""
        return await self.http_request("GET", f"{API_PATH_V1}/ports/status")

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

    async def post_firmware_update_live(self) -> dict[str, Any]:
        """API POST live firmware update."""
        return await self.http_request(
            "POST", f"{API_PATH_V1}/firmware/update/live", {}
        )

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

    async def live_update(self) -> bool:
        """Update QNAP QSW to live firmware."""
        await self.login()

        self.firmware_progress = 0.0
        response = await self.post_firmware_update_live()

        result = response.get(API_RESULT)
        if API_RESULT not in response or result != API_NONE:
            raise APIError(f"Error when updating: {response}")

        return True

    async def reboot(self) -> bool:
        """Reboot QNAP QSW."""
        await self.login()

        response = await self.post_system_command(API_REBOOT)

        result = response.get(API_RESULT)
        if API_RESULT not in response or result != API_NONE:
            raise APIError(f"Error when rebooting: {response}")

        return True

    async def update_progress(self) -> float:
        """Get QNAP QSW update progress."""
        response = await self.get_firmware_update()

        result = response.get(API_RESULT)
        if result is dict:
            if result.keys() >= {API_DOWNLOAD_SIZE, API_FIRMWARE_SIZE}:
                dl_size = float(result[API_DOWNLOAD_SIZE])
                fw_size = float(result[API_FIRMWARE_SIZE])
                self.firmware_progress = dl_size * 100.0 / fw_size

        return self.firmware_progress

    async def update_status(self) -> bool:
        """Get QNAP QSW update status."""
        response = await self.get_firmware_status()

        result = response.get(API_RESULT)
        if API_RESULT in response and result == API_NONE:
            return False
        if result is dict:
            if API_PROGRESS in result and result[API_PROGRESS] == API_DONE:
                return False

        return True

    async def validate(self) -> SystemBoard:
        """Validate QNAP QSW."""
        self._first_update = True
        self.ports_statistics = None

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

            # Update lacp/info once
            if self.lacp_info is None:
                lacp_info = await self.get_lacp_info()
                self.lacp_info = LACPInfo(lacp_info)

            # Update system/board once
            if self.system_board is None:
                system_board = await self.get_system_board()
                self.system_board = SystemBoard(system_board)

            # Get LACP ports start from lacp/info
            if self.lacp_info is not None:
                lacp_start = self.lacp_info.get_start_id()
            elif self.system_board is not None:
                lacp_start = self.system_board.get_port_num() + 1
            else:
                lacp_start = None

            ports_statistics_data = await self.get_ports_statistics()
            _datetime = datetime.utcnow()
            ports_statistics = PortsStatistics(
                ports_statistics_data, lacp_start, _datetime
            )
            ports_statistics.calc(self.ports_statistics)
            self.ports_statistics = ports_statistics

            ports_status_data = await self.get_ports_status()
            ports_status = PortsStatus(ports_status_data, lacp_start)
            ports_status.calc()
            self.ports_status = ports_status

            system_time = await self.get_system_time()
            self.system_time = SystemTime(system_time)
        except QswError as err:
            system_sensor.cancel()
            raise err
        else:
            try:
                self.system_sensor = SystemSensor(await system_sensor)
            except InternalServerError as err:
                if self._first_update:
                    raise err
                _LOGGER.warning(err)

        self._first_update = False

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

        if self.ports_statistics is not None:
            ports_statistics_data = self.ports_statistics.data()
            if len(ports_statistics_data) > 0:
                data[QSD_PORTS_STATISTICS] = ports_statistics_data

        if self.ports_status is not None:
            ports_status_data = self.ports_status.data()
            if len(ports_status_data) > 0:
                data[QSD_PORTS_STATUS] = ports_status_data

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
