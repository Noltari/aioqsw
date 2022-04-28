"""QNAP QSW Device."""
from __future__ import annotations

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
    API_MAC_ADDR,
    API_MAX_SWITCH_TEMP,
    API_MESSAGE,
    API_MODEL,
    API_NEWER,
    API_NUMBER,
    API_PORT_NUM,
    API_PRODUCT,
    API_PUB_DATE,
    API_RESULT,
    API_SERIAL,
    API_SWITCH_TEMP,
    API_TRUNK_NUM,
    API_UPTIME,
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
    QSD_DESCRIPTION,
    QSD_DOWNLOAD_URLS,
    QSD_FAN1_SPEED,
    QSD_FAN2_SPEED,
    QSD_FIRMWARE,
    QSD_MAC,
    QSD_MESSAGE,
    QSD_MODEL,
    QSD_NEWER,
    QSD_NUMBER,
    QSD_PORT_NUM,
    QSD_PRODUCT,
    QSD_PUB_DATE,
    QSD_SERIAL,
    QSD_TEMP,
    QSD_TEMP_MAX,
    QSD_TRUNK_NUM,
    QSD_UPTIME,
    QSD_VERSION,
)
from aioqsw.exceptions import APIError


class FirmwareCheck:
    """Firmware Check."""

    def __init__(self, firmware_check: dict[str, Any]):
        """Firmware Check init."""
        self.build_number: str | None = None
        self.date: str | None = None
        self.description: str | None = None
        self.download_urls: list[str] = []
        self.newer: bool | None = None
        self.number: str | None = None
        self.version: str | None = None

        res = firmware_check.get(API_RESULT)
        if not res:
            raise APIError

        if API_BUILD_NUMBER in res:
            self.build_number = str(res[API_BUILD_NUMBER])

        if API_DATE in res:
            self.date = str(res[API_DATE])

        if API_DESCRIPTION in res:
            self.description = str(res[API_DESCRIPTION])

        if API_DOWNLOAD_URL in res:
            for url in res[API_DOWNLOAD_URL]:
                self.download_urls.append(str(url))

        if API_NEWER in res:
            self.newer = bool(res[API_NEWER])

        if API_NUMBER in res:
            self.number = str(res[API_NUMBER])

        if API_VERSION in res:
            self.version = str(res[API_VERSION])

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

    def __init__(self, firmware_condition: dict[str, Any]):
        """System Time init."""
        self.anomaly: bool | None = None
        self.message: str | None = None

        res = firmware_condition.get(API_RESULT)
        if not res:
            raise APIError

        if API_ANOMALY in res:
            self.anomaly = bool(res[API_ANOMALY])

        if API_MESSAGE in res:
            self.message = str(res[API_MESSAGE])

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

    def __init__(self, firmware_info: dict[str, Any]):
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

        res = firmware_info.get(API_RESULT)
        if not res:
            raise APIError

        if API_BUILD_NUMBER in res:
            self.build_number = str(res[API_BUILD_NUMBER])

        if API_CI_BRANCH in res:
            self.ci_branch = str(res[API_CI_BRANCH])

        if API_CI_COMMIT in res:
            self.ci_commit = str(res[API_CI_COMMIT])

        if API_CI_PIPELINE in res:
            self.ci_pipeline = str(res[API_CI_PIPELINE])

        if API_COMMIT_CPSS in res:
            self.commit_cpss = str(res[API_COMMIT_CPSS])

        if API_COMMIT_ISS in res:
            self.commit_iss = str(res[API_COMMIT_ISS])

        if API_DATE in res:
            self.date = str(res[API_DATE])

        if API_NUMBER in res:
            self.number = str(res[API_NUMBER])

        if API_PUB_DATE in res:
            self.pub_date = str(res[API_PUB_DATE])

        if API_VERSION in res:
            self.version = str(res[API_VERSION])

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


class SystemBoard:
    """System Board."""

    def __init__(self, system_board: dict[str, Any]):
        """System Board init."""
        self.chip_id: str | None = None
        self.mac: str | None = None
        self.model: str | None = None
        self.port_num: int | None = None
        self.product: str | None = None
        self.serial: str | None = None
        self.trunk_num: int | None = None

        res = system_board.get(API_RESULT)
        if not res:
            raise APIError

        if API_CHIP_ID in res:
            self.chip_id = str(res[API_CHIP_ID])
        if API_MAC_ADDR in res:
            self.mac = str(res[API_MAC_ADDR])
        if API_MODEL in res:
            self.model = str(res[API_MODEL])
        if API_PORT_NUM in res:
            self.port_num = int(res[API_PORT_NUM])
        if API_PRODUCT in res:
            self.product = str(res[API_PRODUCT])
        if API_SERIAL in res:
            self.serial = str(res[API_SERIAL])
        if API_TRUNK_NUM in res:
            self.trunk_num = int(res[API_TRUNK_NUM])

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

    def __init__(self, system_sensor: dict[str, Any]):
        """System Sensor init."""
        self.fan1_speed: int | None = None
        self.fan2_speed: int | None = None
        self.temp: int | None = None
        self.temp_max: int | None = None

        res = system_sensor.get(API_RESULT)
        if not res:
            raise APIError

        if API_FAN1_SPEED in res:
            self.fan1_speed = int(res[API_FAN1_SPEED])

        if API_FAN2_SPEED in res:
            self.fan2_speed = int(res[API_FAN2_SPEED])

        if API_MAX_SWITCH_TEMP in res:
            self.temp_max = int(res[API_MAX_SWITCH_TEMP])

        if API_SWITCH_TEMP in res:
            self.temp = int(res[API_SWITCH_TEMP])

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

    def __init__(self, system_time: dict[str, Any]):
        """System Time init."""
        self.uptime: int | None = None

        res = system_time.get(API_RESULT)
        if not res:
            raise APIError

        if API_UPTIME in res:
            self.uptime = int(res[API_UPTIME])

    def data(self) -> dict[str, Any]:
        """Return System Board data."""
        data: dict[str, Any] = {}

        uptime = self.get_uptime()
        if uptime is not None:
            data[QSD_UPTIME] = uptime

        return data

    def get_uptime(self) -> int | None:
        """Get Uptime."""
        return self.uptime
