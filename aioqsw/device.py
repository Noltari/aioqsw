"""QNAP QSW Device."""

from __future__ import annotations

from datetime import datetime, timedelta
import re
from typing import Any

from aioqsw.const import (
    API_ANOMALY,
    API_BUILD_NUMBER,
    API_CHIP_ID,
    API_CI_BRANCH,
    API_CI_COMMIT,
    API_CI_PIPELINE,
    API_COMMIT_CPSS,
    API_COMMIT_ISS,
    API_DATE,
    API_DESCRIPTION,
    API_DOWNLOAD_URL,
    API_FAN1_SPEED,
    API_FAN2_SPEED,
    API_FCS_ERRORS,
    API_FULL_DUPLEX,
    API_KEY,
    API_LINK,
    API_MAC_ADDR,
    API_MAX_PORT_CHANNELS,
    API_MAX_PORTS_PER_PORT_CHANNEL,
    API_MAX_SWITCH_TEMP,
    API_MESSAGE,
    API_MODEL,
    API_NEWER,
    API_NUMBER,
    API_PORT_NUM,
    API_PRODUCT,
    API_PUB_DATE,
    API_RESULT,
    API_RX_ERRORS,
    API_RX_OCTETS,
    API_SERIAL,
    API_SPEED,
    API_START_INDEX,
    API_SWITCH_TEMP,
    API_TRUNK_NUM,
    API_TX_OCTETS,
    API_UPTIME,
    API_VAL,
    API_VERSION,
    QSD_ANOMALY,
    QSD_BUILD_NUMBER,
    QSD_CHIP_ID,
    QSD_CI_BRANCH,
    QSD_CI_COMMIT,
    QSD_CI_PIPELINE,
    QSD_COMMIT_CPSS,
    QSD_COMMIT_ISS,
    QSD_DATE,
    QSD_DATETIME,
    QSD_DESCRIPTION,
    QSD_DOWNLOAD_URLS,
    QSD_FAN1_SPEED,
    QSD_FAN2_SPEED,
    QSD_FCS_ERRORS,
    QSD_FIRMWARE,
    QSD_FULL_DUPLEX,
    QSD_ID,
    QSD_LACP_PORT_NUM,
    QSD_LACP_PORTS,
    QSD_LINK,
    QSD_MAC,
    QSD_MAX_CHANNEL_PORTS,
    QSD_MAX_CHANNELS,
    QSD_MESSAGE,
    QSD_MODEL,
    QSD_NEWER,
    QSD_NUMBER,
    QSD_PORT_NUM,
    QSD_PORTS,
    QSD_PRODUCT,
    QSD_PUB_DATE,
    QSD_RX_ERRORS,
    QSD_RX_OCTETS,
    QSD_RX_SPEED,
    QSD_SERIAL,
    QSD_SPEED,
    QSD_START_ID,
    QSD_START_INDEX,
    QSD_TEMP,
    QSD_TEMP_MAX,
    QSD_TRUNK_NUM,
    QSD_TX_OCTETS,
    QSD_TX_SPEED,
    QSD_UPTIME_SECONDS,
    QSD_UPTIME_TIMESTAMP,
    QSD_VERSION,
)
from aioqsw.exceptions import APIError


class FirmwareCheck:
    """Firmware Check."""

    def __init__(self, data: dict[str, Any]):
        """Firmware Check init."""
        self.build_number: str | None = None
        self.date: str | None = None
        self.description: str | None = None
        self.download_urls: list[str] = []
        self.newer: bool | None = None
        self.number: str | None = None
        self.version: str | None = None

        self.update_data(data)

    def update_data(self, data: dict[str, Any]) -> None:
        """Update Firmware Check data."""
        res: dict[str, Any] | None = data.get(API_RESULT)
        if res is None:
            raise APIError

        build_number = res.get(API_BUILD_NUMBER)
        if build_number is not None:
            self.build_number = str(build_number)

        date = res.get(API_DATE)
        if date is not None:
            self.date = str(date)

        description = res.get(API_DESCRIPTION)
        if description is not None:
            self.description = str(description)

        download_urls: list[Any] | None = res.get(API_DOWNLOAD_URL)
        if download_urls is not None:
            for url in download_urls:
                self.download_urls.append(str(url))

        newer = res.get(API_NEWER)
        if newer is not None:
            self.newer = bool(newer)

        number = res.get(API_NUMBER)
        if number is not None:
            self.number = str(number)

        version = res.get(API_VERSION)
        if version is not None:
            self.version = str(version)

    def data(self) -> dict[str, Any]:
        """Return Firmware Info data."""
        data: dict[str, Any] = {}

        build_number = self.get_build_number()
        if build_number is not None:
            data[QSD_BUILD_NUMBER] = build_number

        date = self.get_date()
        if date is not None:
            data[QSD_DATE] = date

        description = self.get_description()
        if description is not None:
            data[QSD_DESCRIPTION] = description

        download_urls = self.get_download_urls()
        if download_urls is not None:
            data[QSD_DOWNLOAD_URLS] = download_urls

        firmware = self.get_firmware()
        if firmware is not None:
            data[QSD_FIRMWARE] = firmware

        newer = self.get_newer()
        if newer is not None:
            data[QSD_NEWER] = newer

        number = self.get_number()
        if number is not None:
            data[QSD_NUMBER] = number

        version = self.get_version()
        if version is not None:
            data[QSD_VERSION] = version

        return data

    def get_build_number(self) -> str | None:
        """Get build number."""
        return self.build_number

    def get_date(self) -> str | None:
        """Get date."""
        return self.date

    def get_description(self) -> str | None:
        """Get description."""
        if self.description is not None and len(self.description) > 0:
            return self.description
        return None

    def get_download_urls(self) -> list[str] | None:
        """Get download URLs."""
        if len(self.download_urls) > 0:
            return self.download_urls
        return None

    def get_firmware(self) -> str | None:
        """Get firmware."""
        if self.version is not None:
            if self.number is not None:
                if self.build_number is not None:
                    return f"{self.version}.{self.number} ({self.build_number})"
                return f"{self.version}.{self.number}"
            return self.version
        return None

    def get_newer(self) -> bool | None:
        """Get newer."""
        return self.newer

    def get_number(self) -> str | None:
        """Get number."""
        return self.number

    def get_version(self) -> str | None:
        """Get version."""
        return self.version


class FirmwareCondition:
    """Firmware Condition."""

    def __init__(self, data: dict[str, Any]):
        """System Time init."""
        self.anomaly: bool | None = None
        self.message: str | None = None

        self.update_data(data)

    def update_data(self, data: dict[str, Any]) -> None:
        """Update Firmware Condition data."""
        res: dict[str, Any] | None = data.get(API_RESULT)
        if res is None:
            raise APIError

        anomaly = res.get(API_ANOMALY)
        if anomaly is not None:
            self.anomaly = bool(anomaly)

        message = res.get(API_MESSAGE)
        if message is not None:
            self.message = str(message)

    def data(self) -> dict[str, Any]:
        """Return System Board data."""
        data: dict[str, Any] = {}

        anomaly = self.get_anomaly()
        if anomaly is not None:
            data[QSD_ANOMALY] = anomaly

        message = self.get_message()
        if message is not None:
            data[QSD_MESSAGE] = message

        return data

    def get_anomaly(self) -> bool | None:
        """Get Anomaly."""
        return self.anomaly

    def get_message(self) -> str | None:
        """Get Message."""
        if self.message is not None and len(self.message) > 0:
            return self.message
        return None


class FirmwareInfo:
    """Firmware Info."""

    def __init__(self, data: dict[str, Any]):
        """Firmware Info init."""
        self.build_number: str | None = None
        self.ci_branch: str | None = None
        self.ci_commit: str | None = None
        self.ci_pipeline: str | None = None
        self.commit_cpss: str | None = None
        self.commit_iss: str | None = None
        self.date: str | None = None
        self.number: str | None = None
        self.pub_date: str | None = None
        self.version: str | None = None

        self.update_data(data)

    def update_data(self, data: dict[str, Any]) -> None:
        """Update Firmware Info data."""
        res: dict[str, Any] | None = data.get(API_RESULT)
        if res is None:
            raise APIError

        build_number = res.get(API_BUILD_NUMBER)
        if build_number is not None:
            self.build_number = str(build_number)

        ci_branch = res.get(API_CI_BRANCH)
        if ci_branch is not None:
            self.ci_branch = str(ci_branch)

        ci_commit = res.get(API_CI_COMMIT)
        if ci_commit is not None:
            self.ci_commit = str(ci_commit)

        ci_pipeline = res.get(API_CI_PIPELINE)
        if ci_pipeline is not None:
            self.ci_pipeline = str(ci_pipeline)

        commit_cpss = res.get(API_COMMIT_CPSS)
        if commit_cpss is not None:
            self.commit_cpss = str(commit_cpss)

        commit_iss = res.get(API_COMMIT_ISS)
        if commit_iss is not None:
            self.commit_iss = str(commit_iss)

        date = res.get(API_DATE)
        if date is not None:
            self.date = str(date)

        number = res.get(API_NUMBER)
        if number is not None:
            self.number = str(number)

        pub_date = res.get(API_PUB_DATE)
        if pub_date is not None:
            self.pub_date = str(pub_date)

        version = res.get(API_VERSION)
        if version is not None:
            self.version = str(version)

    def data(self) -> dict[str, Any]:
        """Return Firmware Info data."""
        data: dict[str, Any] = {}

        build_number = self.get_build_number()
        if build_number is not None:
            data[QSD_BUILD_NUMBER] = build_number

        ci_branch = self.get_ci_branch()
        if ci_branch is not None:
            data[QSD_CI_BRANCH] = ci_branch

        ci_commit = self.get_ci_commit()
        if ci_commit is not None:
            data[QSD_CI_COMMIT] = ci_commit

        ci_pipeline = self.get_ci_pipeline()
        if ci_pipeline is not None:
            data[QSD_CI_PIPELINE] = ci_pipeline

        commit_cpss = self.get_commit_cpss()
        if commit_cpss is not None:
            data[QSD_COMMIT_CPSS] = commit_cpss

        commit_iss = self.get_commit_iss()
        if commit_iss is not None:
            data[QSD_COMMIT_ISS] = commit_iss

        date = self.get_date()
        if date is not None:
            data[QSD_DATE] = date

        firmware = self.get_firmware()
        if firmware is not None:
            data[QSD_FIRMWARE] = firmware

        number = self.get_number()
        if number is not None:
            data[QSD_NUMBER] = number

        pub_date = self.get_pub_date()
        if pub_date is not None:
            data[QSD_PUB_DATE] = pub_date

        version = self.get_version()
        if version is not None:
            data[QSD_VERSION] = version

        return data

    def get_build_number(self) -> str | None:
        """Get build number."""
        return self.build_number

    def get_ci_branch(self) -> str | None:
        """Get CI branch."""
        return self.ci_branch

    def get_ci_commit(self) -> str | None:
        """Get CI commit."""
        return self.ci_commit

    def get_ci_pipeline(self) -> str | None:
        """Get CI pipeline."""
        return self.ci_pipeline

    def get_commit_cpss(self) -> str | None:
        """Get commit cpss."""
        if self.commit_cpss and len(self.commit_cpss) > 0:
            return self.commit_cpss
        return None

    def get_commit_iss(self) -> str | None:
        """Get commit iss."""
        return self.commit_iss

    def get_date(self) -> str | None:
        """Get date."""
        return self.date

    def get_firmware(self) -> str | None:
        """Get firmware."""
        if self.version is not None:
            if self.number is not None:
                if self.build_number is not None:
                    return f"{self.version}.{self.number} ({self.build_number})"
                return f"{self.version}.{self.number}"
            return self.version
        return None

    def get_number(self) -> str | None:
        """Get number."""
        return self.number

    def get_pub_date(self) -> str | None:
        """Get pub date."""
        return self.pub_date

    def get_version(self) -> str | None:
        """Get version."""
        return self.version


class LACPInfo:
    """LACP Info."""

    def __init__(self, data: dict[str, Any]):
        """LACP Info init."""
        self.max_channels: int | None = None
        self.max_channel_ports: int | None = None
        self.start_index: int | None = None

        self.update_data(data)

    def update_data(self, data: dict[str, Any]) -> None:
        """Update LACP Info data."""
        res: dict[str, Any] | None = data.get(API_RESULT)
        if res is None:
            raise APIError

        max_channels = res.get(API_MAX_PORT_CHANNELS)
        if max_channels is not None:
            self.max_channels = int(max_channels)

        max_channel_ports = res.get(API_MAX_PORTS_PER_PORT_CHANNEL)
        if max_channel_ports is not None:
            self.max_channel_ports = int(max_channel_ports)

        start_index = res.get(API_START_INDEX)
        if start_index is not None:
            self.start_index = int(start_index)

    def data(self) -> dict[str, Any]:
        """Return LACP Info data."""
        data: dict[str, Any] = {}

        max_channels = self.get_max_channels()
        if max_channels is not None:
            data[QSD_MAX_CHANNELS] = max_channels

        max_channel_ports = self.get_max_channel_ports()
        if max_channel_ports is not None:
            data[QSD_MAX_CHANNEL_PORTS] = max_channel_ports

        start_id = self.get_start_id()
        if start_id is not None:
            data[QSD_START_ID] = start_id

        start_index = self.get_start_index()
        if start_index is not None:
            data[QSD_START_INDEX] = start_index

        return data

    def get_max_channels(self) -> int | None:
        """Get max channels."""
        return self.max_channels

    def get_max_channel_ports(self) -> int | None:
        """Get max ports per channel."""
        return self.max_channel_ports

    def get_start_id(self) -> int | None:
        """Get start ID."""
        start_index = self.get_start_index()
        if start_index is not None:
            return start_index + 1
        return None

    def get_start_index(self) -> int | None:
        """Get start index."""
        return self.start_index


class PortStatistics:
    """Single Port Statistics."""

    def __init__(self, data: dict[str, Any]):
        """Single Port Statistics init."""
        key = data.get(API_KEY)
        if key is None:
            raise APIError

        self.cur_rx_octets: int | None = None
        self.cur_tx_octets: int | None = None
        self.fcs_errors: int | None = None
        self.id: int = int(key)
        self.lacp_id: int | None = None
        self.prev_rx_octets: int | None = None
        self.prev_tx_octets: int | None = None
        self.rx_errors: int | None = None
        self.rx_speed: int = 0
        self.tx_speed: int = 0

        self.update_data(data)

    def update_data(self, data: dict[str, Any]) -> None:
        """Update Port Statistics data."""

        self.prev_rx_octets = self.cur_rx_octets
        self.prev_tx_octets = self.cur_tx_octets

        val: dict[str, Any] | None = data.get(API_VAL)
        if val is not None:
            fcs_errors = val.get(API_FCS_ERRORS)
            if fcs_errors is not None:
                self.fcs_errors = int(fcs_errors)

            rx_errors = val.get(API_RX_ERRORS)
            if rx_errors is not None:
                self.rx_errors = int(rx_errors)

            cur_rx_octets = val.get(API_RX_OCTETS)
            if cur_rx_octets is not None:
                self.cur_rx_octets = int(cur_rx_octets)

            cur_tx_octets = val.get(API_TX_OCTETS)
            if cur_tx_octets is not None:
                self.cur_tx_octets = int(cur_tx_octets)

    @staticmethod
    def calc_speed(
        cur_octets: int | None, prev_octets: int | None, seconds: float
    ) -> int:
        """Calculate network speed."""
        if (seconds > 0) and (cur_octets is not None) and (prev_octets is not None):
            return int((cur_octets - prev_octets) / seconds)
        return 0

    def calc(self, seconds: float) -> None:
        """Calculate Port Statistics data."""
        self.rx_speed = self.calc_speed(
            self.get_cur_rx_octets(), self.get_prev_rx_octets(), seconds
        )
        self.tx_speed = self.calc_speed(
            self.get_cur_tx_octets(), self.get_prev_tx_octets(), seconds
        )

    def data(self) -> dict[str, Any]:
        """Return Single Port Statistics data."""
        data: dict[str, Any] = {}

        fcs_errors = self.get_fcs_errors()
        if fcs_errors is not None:
            data[QSD_FCS_ERRORS] = fcs_errors

        data[QSD_ID] = self.get_lacp_id() or self.get_id()

        rx_errors = self.get_rx_errors()
        if rx_errors is not None:
            data[QSD_RX_ERRORS] = rx_errors

        rx_octets = self.get_cur_rx_octets()
        if rx_octets is not None:
            data[QSD_RX_OCTETS] = rx_octets

        rx_speed = self.get_rx_speed()
        if rx_speed is not None:
            data[QSD_RX_SPEED] = rx_speed

        tx_octets = self.get_cur_tx_octets()
        if tx_octets is not None:
            data[QSD_TX_OCTETS] = tx_octets

        tx_speed = self.get_tx_speed()
        if tx_speed is not None:
            data[QSD_TX_SPEED] = tx_speed

        return data

    def get_cur_rx_octets(self) -> int | None:
        """Get port current RX octets."""
        return self.cur_rx_octets

    def get_cur_tx_octets(self) -> int | None:
        """Get port current TX octets."""
        return self.cur_tx_octets

    def get_fcs_errors(self) -> int | None:
        """Get port FCS errors."""
        return self.fcs_errors

    def get_id(self) -> int:
        """Get port ID."""
        return self.id

    def get_lacp_id(self) -> int | None:
        """Get LACP port ID."""
        return self.lacp_id

    def get_prev_rx_octets(self) -> int | None:
        """Get port previous RX octets."""
        return self.prev_rx_octets

    def get_prev_tx_octets(self) -> int | None:
        """Get port previous TX octets."""
        return self.prev_tx_octets

    def get_rx_errors(self) -> int | None:
        """Get port RX errors."""
        return self.rx_errors

    def get_rx_speed(self) -> int | None:
        """Get port RX speed."""
        return self.rx_speed

    def get_tx_speed(self) -> int | None:
        """Get port TX speed."""
        return self.tx_speed

    def set_id(self, _id: int) -> None:
        """Set port ID."""
        self.id = _id

    def set_lacp_id(self, lacp_id: int) -> None:
        """Set LACP port ID."""
        self.lacp_id = lacp_id


class PortsStatistics:
    """Ports Statistics."""

    def __init__(
        self,
        data: dict[str, Any],
        lacp_start: int | None,
        cur_datetime: datetime,
    ):
        """Ports Statistics init."""
        self._first_update: bool = True
        self.cur_datetime: datetime = cur_datetime
        self.fcs_errors: int | None = None
        self.lacp_ports: dict[int, PortStatistics] = {}
        self.lacp_start: int | None = None
        self.link: int | None = None
        self.phy_ports: dict[int, PortStatistics] = {}
        self.ports: dict[int, PortStatistics] = {}
        self.prev_datetime: datetime = cur_datetime
        self.rx_errors: int | None = None
        self.rx_octets: int | None = None
        self.rx_speed: int = 0
        self.tx_octets: int | None = None
        self.tx_speed: int = 0

        self.update_data(data, lacp_start, cur_datetime)

    def update_lacp_ports(self, lacp_start: int | None) -> None:
        """Update LACP Ports."""
        lacp_id_min = None
        if lacp_start is not None:
            for port in self.ports.values():
                port_id = port.get_id()
                if port_id >= lacp_start:
                    if lacp_id_min is None or port_id < lacp_id_min:
                        lacp_id_min = port_id

        if lacp_id_min is not None:
            lacp_id_min -= 1

        lacp_ports: dict[int, PortStatistics] = {}
        phy_ports: dict[int, PortStatistics] = {}
        for port in self.ports.values():
            port_id = port.get_id()
            if (
                lacp_id_min is not None
                and lacp_start is not None
                and port_id >= lacp_start
            ):
                lacp_id = port_id - lacp_id_min
                port.set_lacp_id(lacp_id)
                lacp_ports[lacp_id] = port
            else:
                phy_ports[port_id] = port
        self.lacp_ports = lacp_ports
        self.phy_ports = phy_ports

        self.lacp_start = lacp_start

    def update_data(
        self, data: dict[str, Any], lacp_start: int | None, cur_datetime: datetime
    ) -> None:
        """Update Port Statistics data."""
        res: list[dict[str, Any]] | None = data.get(API_RESULT)
        if res is None:
            raise APIError

        self.prev_datetime = self.cur_datetime
        self.cur_datetime = cur_datetime

        for port_data in res:
            port_key = port_data.get(API_KEY)
            if port_key is not None:
                port_id = int(port_key)

                port_stats = self.get_port(port_id)
                if port_stats is None:
                    self.ports[port_id] = PortStatistics(port_data)
                else:
                    port_stats.update_data(port_data)

        if self._first_update or lacp_start != self.lacp_start:
            self.update_lacp_ports(lacp_start)

        self.calc()

        self._first_update = False

    @staticmethod
    def calc_speed(
        cur_octets: int | None, prev_octets: int | None, seconds: float
    ) -> int:
        """Calculate network speed."""
        if seconds > 0 and cur_octets is not None and prev_octets is not None:
            return int((cur_octets - prev_octets) / seconds)
        return 0

    def calc(self) -> None:
        """Calculate Ports Statistics data."""
        fcs_errors = 0
        rx_errors = 0
        rx_octets = 0
        tx_octets = 0

        if not self._first_update:
            seconds = (self.cur_datetime - self.prev_datetime).total_seconds()
        else:
            seconds = 0

        calc_speeds = not self._first_update and seconds > 0

        for port in self.ports.values():
            port_fcs_errors = port.get_fcs_errors()
            if port_fcs_errors is not None:
                fcs_errors += port_fcs_errors

            port_rx_errors = port.get_rx_errors()
            if port_rx_errors is not None:
                rx_errors += port_rx_errors

            port_rx_octets = port.get_cur_rx_octets()
            if port_rx_octets is not None:
                rx_octets += port_rx_octets

            port_tx_octets = port.get_cur_tx_octets()
            if port_tx_octets is not None:
                tx_octets += port_tx_octets

            if calc_speeds:
                port.calc(seconds)

        if calc_speeds:
            self.rx_speed = self.calc_speed(rx_octets, self.rx_octets, seconds)
            self.tx_speed = self.calc_speed(tx_octets, self.tx_octets, seconds)

        self.fcs_errors = fcs_errors
        self.rx_errors = rx_errors
        self.rx_octets = rx_octets
        self.tx_octets = tx_octets

    def data(self) -> dict[str, Any]:
        """Return Ports Statistics data."""
        data: dict[str, Any] = {}

        cur_datetime = self.get_cur_datetime()
        if cur_datetime is not None:
            data[QSD_DATETIME] = cur_datetime.strftime("%Y/%m/%d %H:%M:%S")

        fcs_errors = self.get_fcs_errors()
        if fcs_errors is not None:
            data[QSD_FCS_ERRORS] = fcs_errors

        lacp_port_num = self.get_lacp_port_num()
        if lacp_port_num is not None:
            data[QSD_LACP_PORT_NUM] = lacp_port_num

        lacp_ports = self.get_lacp_ports()
        if lacp_ports is not None:
            data[QSD_LACP_PORTS] = {}
            for port_id, port in lacp_ports.items():
                data[QSD_LACP_PORTS][port_id] = port.data()

        port_num = self.get_phy_port_num()
        if port_num is not None:
            data[QSD_PORT_NUM] = port_num

        ports = self.get_phy_ports()
        if ports is not None:
            data[QSD_PORTS] = {}
            for port_id, port in ports.items():
                data[QSD_PORTS][port_id] = port.data()

        rx_errors = self.get_rx_errors()
        if rx_errors is not None:
            data[QSD_RX_ERRORS] = rx_errors

        rx_octets = self.get_rx_octets()
        if rx_octets is not None:
            data[QSD_RX_OCTETS] = rx_octets

        rx_speed = self.get_rx_speed()
        if rx_speed is not None:
            data[QSD_RX_SPEED] = rx_speed

        tx_octets = self.get_tx_octets()
        if tx_octets is not None:
            data[QSD_TX_OCTETS] = tx_octets

        tx_speed = self.get_tx_speed()
        if tx_speed is not None:
            data[QSD_TX_SPEED] = tx_speed

        return data

    def get_cur_datetime(self) -> datetime | None:
        """Get statistics current datetime."""
        return self.cur_datetime

    def get_fcs_errors(self) -> int | None:
        """Get total FCS errors."""
        return self.fcs_errors

    def get_lacp_ports(self) -> dict[int, PortStatistics] | None:
        """Get LACP ports."""
        if len(self.lacp_ports) > 0:
            return self.lacp_ports
        return None

    def get_lacp_port_num(self) -> int:
        """Get number of LACP ports."""
        return len(self.lacp_ports)

    def get_phy_ports(self) -> dict[int, PortStatistics] | None:
        """Get Physical ports."""
        if len(self.phy_ports) > 0:
            return self.phy_ports
        return None

    def get_phy_port_num(self) -> int:
        """Get number of Physical ports."""
        return len(self.phy_ports)

    def get_ports(self) -> dict[int, PortStatistics] | None:
        """Get ports."""
        if len(self.ports) > 0:
            return self.ports
        return None

    def get_port(self, port_id: int) -> PortStatistics | None:
        """Get Port by ID."""
        return self.ports.get(port_id)

    def get_prev_datetime(self) -> datetime | None:
        """Get statistics previous datetime."""
        return self.prev_datetime

    def get_rx_errors(self) -> int | None:
        """Get total RX errors."""
        return self.rx_errors

    def get_rx_octets(self) -> int | None:
        """Get total RX octets."""
        return self.rx_octets

    def get_rx_speed(self) -> int | None:
        """Get total RX speed."""
        return self.rx_speed

    def get_tx_octets(self) -> int | None:
        """Get total TX octets."""
        return self.tx_octets

    def get_tx_speed(self) -> int | None:
        """Get total TX speed."""
        return self.tx_speed


class PortStatus:
    """Single Port Status."""

    def __init__(self, data: dict[str, Any]):
        """Single Port Status init."""
        key = data.get(API_KEY)
        if key is None:
            raise APIError

        self.full_duplex: bool | None = None
        self.id: int = int(key)
        self.lacp_id: int | None = None
        self.link: bool | None = None
        self.speed: int | None = None

        self.update_data(data)

    def update_data(self, data: dict[str, Any]) -> None:
        """Update Port Status data."""
        val: dict[str, Any] | None = data.get(API_VAL)
        if val is not None:
            full_duplex = val.get(API_FULL_DUPLEX)
            if full_duplex is not None:
                self.full_duplex = bool(full_duplex)

            link = val.get(API_LINK)
            if link is not None:
                self.link = bool(link)

            speed = val.get(API_SPEED)
            if speed is not None:
                self.speed = int(speed)

    def data(self) -> dict[str, Any]:
        """Return Single Port Status data."""
        data: dict[str, Any] = {}

        full_duplex = self.get_full_duplex()
        if full_duplex is not None:
            data[QSD_FULL_DUPLEX] = full_duplex

        data[QSD_ID] = self.get_lacp_id() or self.get_id()

        link = self.get_link()
        if link is not None:
            data[QSD_LINK] = link

        speed = self.get_speed()
        if speed is not None:
            data[QSD_SPEED] = speed

        return data

    def get_full_duplex(self) -> bool | None:
        """Get port full duplex."""
        return self.full_duplex

    def get_id(self) -> int:
        """Get port ID."""
        return self.id

    def get_lacp_id(self) -> int | None:
        """Get LACP port ID."""
        return self.lacp_id

    def get_link(self) -> bool | None:
        """Get port link connection."""
        return self.link

    def get_speed(self) -> int | None:
        """Get port speed."""
        return self.speed

    def set_lacp_id(self, _id: int) -> None:
        """Set LACP port ID."""
        self.id = _id

    def set_id(self, _id: int) -> None:
        """Set port ID."""
        self.id = _id


class PortsStatus:
    """Ports Status."""

    def __init__(self, data: dict[str, Any], lacp_start: int | None):
        """Ports Status init."""
        self._first_update: bool = True
        self.lacp_start: int | None = None
        self.link: int | None = None
        self.phy_ports: dict[int, PortStatus] = {}
        self.ports: dict[int, PortStatus] = {}
        self.lacp_ports: dict[int, PortStatus] = {}

        self.update_data(data, lacp_start)

    def update_lacp_ports(self, lacp_start: int | None) -> None:
        """Update LACP Ports."""
        lacp_id_min = None
        if lacp_start is not None:
            for port in self.ports.values():
                port_id = port.get_id()
                if port_id >= lacp_start:
                    if lacp_id_min is None or port_id < lacp_id_min:
                        lacp_id_min = port_id

        if lacp_id_min is not None:
            lacp_id_min -= 1

        lacp_ports: dict[int, PortStatus] = {}
        phy_ports: dict[int, PortStatus] = {}
        for port in self.ports.values():
            port_id = port.get_id()
            if (
                lacp_id_min is not None
                and lacp_start is not None
                and port_id >= lacp_start
            ):
                lacp_id = port_id - lacp_id_min
                port.set_lacp_id(lacp_id)
                lacp_ports[lacp_id] = port
            else:
                phy_ports[port_id] = port
        self.lacp_ports = lacp_ports
        self.phy_ports = phy_ports

        self.lacp_start = lacp_start

    def update_data(self, data: dict[str, Any], lacp_start: int | None) -> None:
        """Update Ports Status data."""
        res: list[dict[str, Any]] | None = data.get(API_RESULT)
        if res is None:
            raise APIError

        for port_data in res:
            port_key = port_data.get(API_KEY)
            if port_key is not None:
                port_id = int(port_key)

                port_status = self.get_port(port_id)
                if port_status is None:
                    self.ports[port_id] = PortStatus(port_data)
                else:
                    port_status.update_data(port_data)

        if self._first_update or lacp_start != self.lacp_start:
            self.update_lacp_ports(lacp_start)

        self.calc()

        self._first_update = False

    def calc(self) -> None:
        """Calculate Ports Status data."""
        ports = self.get_ports()
        if ports is not None:
            link = 0
            for port in ports.values():
                if port.get_link():
                    link += 1
            self.link = link

    def data(self) -> dict[str, Any]:
        """Return Ports Status data."""
        data: dict[str, Any] = {}

        lacp_port_num = self.get_lacp_port_num()
        if lacp_port_num is not None:
            data[QSD_LACP_PORT_NUM] = lacp_port_num

        lacp_ports = self.get_lacp_ports()
        if lacp_ports is not None:
            data[QSD_LACP_PORTS] = {}
            for port_id, port in lacp_ports.items():
                data[QSD_LACP_PORTS][port_id] = port.data()

        link = self.get_link()
        if link is not None:
            data[QSD_LINK] = link

        port_num = self.get_phy_port_num()
        if port_num is not None:
            data[QSD_PORT_NUM] = port_num

        ports = self.get_phy_ports()
        if ports is not None:
            data[QSD_PORTS] = {}
            for port_id, port in ports.items():
                data[QSD_PORTS][port_id] = port.data()

        return data

    def get_lacp_ports(self) -> dict[int, PortStatus] | None:
        """Get LACP ports."""
        if len(self.lacp_ports) > 0:
            return self.lacp_ports
        return None

    def get_lacp_port_num(self) -> int:
        """Get number of LACP ports."""
        return len(self.lacp_ports)

    def get_link(self) -> int | None:
        """Get number of ports with active link."""
        return self.link

    def get_ports(self) -> dict[int, PortStatus] | None:
        """Get ports."""
        if len(self.ports) > 0:
            return self.ports
        return None

    def get_port(self, port_id: int) -> PortStatus | None:
        """Get Port by ID."""
        return self.ports.get(port_id)

    def get_phy_ports(self) -> dict[int, PortStatus] | None:
        """Get Physical ports."""
        if len(self.phy_ports) > 0:
            return self.phy_ports
        return None

    def get_phy_port_num(self) -> int:
        """Get number of Physical ports."""
        return len(self.phy_ports)


class SystemBoard:
    """System Board."""

    def __init__(self, data: dict[str, Any]):
        """System Board init."""
        self.chip_id: str | None = None
        self.mac: str | None = None
        self.model: str | None = None
        self.port_num: int | None = None
        self.product: str | None = None
        self.serial: str | None = None
        self.trunk_num: int | None = None

        self.update_data(data)

    def update_data(self, data: dict[str, Any]) -> None:
        """Update System Board data."""
        res: dict[str, Any] | None = data.get(API_RESULT)
        if res is None:
            raise APIError

        chip_id = res.get(API_CHIP_ID)
        if chip_id is not None:
            self.chip_id = str(chip_id)

        mac = res.get(API_MAC_ADDR)
        if mac is not None:
            self.mac = str(mac)

        model = res.get(API_MODEL)
        if model is not None:
            self.model = str(model)

        port_num = res.get(API_PORT_NUM)
        if port_num is not None:
            self.port_num = int(port_num)

        product = res.get(API_PRODUCT)
        if product is not None:
            self.product = str(product)

        serial = res.get(API_SERIAL)
        if serial is not None:
            self.serial = str(serial)

        trunk_num = res.get(API_TRUNK_NUM)
        if trunk_num is not None:
            self.trunk_num = int(trunk_num)

    def data(self) -> dict[str, Any]:
        """Return System Board data."""
        data: dict[str, Any] = {}

        chip_id = self.get_chip_id()
        if chip_id is not None:
            data[QSD_CHIP_ID] = chip_id

        mac = self.get_mac()
        if mac is not None:
            data[QSD_MAC] = mac

        model = self.get_model()
        if model is not None:
            data[QSD_MODEL] = model

        port_num = self.get_port_num()
        if port_num is not None:
            data[QSD_PORT_NUM] = port_num

        product = self.get_product()
        if product is not None:
            data[QSD_PRODUCT] = product

        serial = self.get_serial()
        if serial is not None:
            data[QSD_SERIAL] = serial

        trunk_num = self.get_trunk_num()
        if trunk_num is not None:
            data[QSD_TRUNK_NUM] = trunk_num

        return data

    def get_chip_id(self) -> str | None:
        """Get Chip ID."""
        return self.chip_id

    def get_mac(self) -> str | None:
        """Get MAC address."""
        return self.mac

    def get_model(self) -> str | None:
        """Get model."""
        return self.model

    def get_port_num(self) -> int | None:
        """Get port number."""
        return self.port_num

    def get_product(self) -> str | None:
        """Get product."""
        return self.product

    def get_serial(self) -> str | None:
        """Get serial."""
        if self.serial is not None:
            return re.sub(r"[\W_]+", "", self.serial)
        return None

    def get_trunk_num(self) -> int | None:
        """Get trunk number."""
        return self.trunk_num


class SystemSensor:
    """System Sensor."""

    def __init__(self, data: dict[str, Any]):
        """System Sensor init."""
        self.fan1_speed: int | None = None
        self.fan2_speed: int | None = None
        self.temp: int | None = None
        self.temp_max: int | None = None

        self.update_data(data)

    def update_data(self, data: dict[str, Any]) -> None:
        """Update System Sensor data."""
        res: dict[str, Any] | None = data.get(API_RESULT)
        if res is None:
            raise APIError

        fan1_speed = res.get(API_FAN1_SPEED)
        if fan1_speed is not None:
            self.fan1_speed = int(fan1_speed)

        fan2_speed = res.get(API_FAN2_SPEED)
        if fan2_speed is not None:
            self.fan2_speed = int(fan2_speed)

        temp_max = res.get(API_MAX_SWITCH_TEMP)
        if temp_max is not None:
            self.temp_max = int(temp_max)

        temp = res.get(API_SWITCH_TEMP)
        if temp is not None:
            self.temp = int(temp)

    def data(self) -> dict[str, Any]:
        """Return System Board data."""
        data: dict[str, Any] = {}

        fan1_speed = self.get_fan1_speed()
        if fan1_speed is not None:
            data[QSD_FAN1_SPEED] = fan1_speed

        fan2_speed = self.get_fan2_speed()
        if fan2_speed is not None:
            data[QSD_FAN2_SPEED] = fan2_speed

        temp = self.get_temp()
        if temp is not None:
            data[QSD_TEMP] = temp

        temp_max = self.get_temp_max()
        if temp_max is not None:
            data[QSD_TEMP_MAX] = temp_max

        return data

    def get_fan1_speed(self) -> int | None:
        """Get fan 1 speed."""
        if self.fan1_speed is not None and self.fan1_speed >= 0:
            return self.fan1_speed
        return None

    def get_fan2_speed(self) -> int | None:
        """Get fan 2 speed."""
        if self.fan2_speed is not None and self.fan2_speed >= 0:
            return self.fan2_speed
        return None

    def get_temp(self) -> int | None:
        """Get temperature."""
        return self.temp

    def get_temp_max(self) -> int | None:
        """Get maximum temperature."""
        return self.temp_max


class SystemTime:
    """System Time."""

    def __init__(self, data: dict[str, Any], cur_datetime: datetime):
        """System Time init."""
        self.uptime_seconds: int | None = None
        self.uptime_timestamp: datetime | None = None

        self.update_data(data, cur_datetime)

    def update_data(self, data: dict[str, Any], cur_datetime: datetime) -> None:
        """Update System Time data."""
        res: dict[str, Any] | None = data.get(API_RESULT)
        if res is None:
            raise APIError

        uptime_seconds = res.get(API_UPTIME)
        if uptime_seconds is not None:
            uptime_seconds = int(uptime_seconds)
            if uptime_seconds < 0:
                self.uptime_seconds = None
            else:
                self.uptime_seconds = uptime_seconds

                if self.uptime_timestamp is None:
                    uptime_delta = timedelta(seconds=uptime_seconds)
                    self.uptime_timestamp = cur_datetime - uptime_delta

    def data(self) -> dict[str, Any]:
        """Return System Board data."""
        data: dict[str, Any] = {}

        uptime_seconds = self.get_uptime_seconds()
        if uptime_seconds is not None:
            data[QSD_UPTIME_SECONDS] = uptime_seconds

        uptime_timestamp = self.get_uptime_timestamp()
        if uptime_timestamp is not None:
            data[QSD_UPTIME_TIMESTAMP] = uptime_timestamp

        return data

    def get_uptime_seconds(self) -> int | None:
        """Get Uptime seconds."""
        return self.uptime_seconds

    def get_uptime_timestamp(self) -> str | None:
        """Get Uptime timestamp."""
        if self.uptime_timestamp is not None:
            return self.uptime_timestamp.isoformat()
        return None
