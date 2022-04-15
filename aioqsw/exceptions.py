"""QNAP QSW library exceptions."""
from __future__ import annotations


class QswError(Exception):
    """Base class for aioqsw errors."""


class APIError(QswError):
    """Exception raised when API fails."""


class InvalidHost(QswError):
    """Exception raised when invalid host is requested."""


class LoginError(QswError):
    """Exception raised when invalid host is requested."""
