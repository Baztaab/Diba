# -*- coding: utf-8 -*-
"""
Backward compatibility module for settings_models.

DEPRECATED: This module will be removed in Diba v6.0.
Please update your imports:
    OLD: from diba.kr_types.settings_models import ...
    NEW: from diba.schemas.settings_models import ...
"""

import warnings

warnings.warn(
    "The 'diba.kr_types.settings_models' module is deprecated and will be removed in v6.0. "
    "Please update your imports to use 'diba.schemas.settings_models' instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export everything from schemas.settings_models for backward compatibility
from diba.schemas.settings_models import *  # noqa: F401, F403
