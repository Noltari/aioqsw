"""QNAP QSW library exceptions."""

from __future__ import annotations


class QswError(Exception):
    """Base class for aioqsw errors."""


class APIError(QswError):
    """Exception raised when API fails."""


class APITimeout(QswError):
    """Exception raised when API timeouts."""


class InternalServerError(APIError):
    """Exception raised when API returns internal server error."""


class InvalidHost(QswError):
    """Exception raised when invalid host is requested."""


class InvalidResponse(QswError):
    """Exception raised when invalid response is received."""


class LoginError(QswError):
    """Exception raised when login fails."""
