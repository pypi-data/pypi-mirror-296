"""
Exception classes for Ursactl
"""


class UrsaCtlError(Exception):
    """Generic errors."""


class UrsaNotAuthorized(UrsaCtlError):
    """Authentication/authorization errors."""


class UrsaProjectNotDefined(UrsaCtlError):
    """Project required but not defined."""


class UrsaBadProjectName(UrsaCtlError):
    """Project name is not valid."""
