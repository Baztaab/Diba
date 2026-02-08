# -*- coding: utf-8 -*-
"""
Backward compatibility module for diba_exception.

DEPRECATED: This module will be removed in Diba v6.0.
Please update your imports:
    OLD: from diba.kr_types.diba_exception import ...
    NEW: from diba.schemas.diba_exception import ...
"""

import warnings

warnings.warn(
    "The 'diba.kr_types.diba_exception' module is deprecated and will be removed in v6.0. "
    "Please update your imports to use 'diba.schemas.diba_exception' instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export everything from schemas.diba_exception for backward compatibility
from diba.schemas.diba_exception import *  # noqa: F401, F403
