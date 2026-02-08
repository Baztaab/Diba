# -*- coding: utf-8 -*-
"""
This is part of Diba (C) 2025 Giacomo Battaglia
"""


class DibaException(Exception):
    """
    Custom Diba Exception
    """

    def __init__(self, message):
        """
        Initialize a new DibaException.

        Args:
            message: The error message to be displayed.
        """
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
