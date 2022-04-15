"""QNAP QSW API Config."""

from aioqsw.localapi import ConnectionOptions

QNAP_QSW_OPTIONS = ConnectionOptions("QSW_URL", "QSW_USER", "QSW_PASS")
