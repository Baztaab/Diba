# -*- coding: utf-8 -*-
"""
Backward compatibility module for kr_literals.

DEPRECATED: This module will be removed in Diba v6.0.
Please update your imports:
    OLD: from diba.kr_types.kr_literals import ...
    NEW: from diba.schemas.kr_literals import ...
"""

import warnings

warnings.warn(
    "The 'diba.kr_types.kr_literals' module is deprecated and will be removed in v6.0. "
    "Please update your imports to use 'diba.schemas.kr_literals' instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export everything from schemas.kr_literals for backward compatibility
from diba.schemas.kr_literals import *  # noqa: F401, F403
