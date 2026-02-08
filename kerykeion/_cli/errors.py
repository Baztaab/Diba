class CLIError(Exception):
    """Base CLI error with user-facing message."""


class ValidationError(CLIError):
    """Argument validation error."""


class EphemerisNotConfiguredError(CLIError):
    """Ephemeris path not configured when required."""


class SwissEphCalculationError(CLIError):
    """Wrap SwissEph runtime errors."""
