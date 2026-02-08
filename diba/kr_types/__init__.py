# -*- coding: utf-8 -*-
"""
Backward compatibility module for Diba v4.x imports.

DEPRECATED: This module will be removed in Diba v6.0.
Please update your imports:
    OLD: from diba.kr_types import ...
    NEW: from diba.schemas import ...
"""

import warnings

# Issue deprecation warning when this module is imported
warnings.warn(
    "The 'diba.kr_types' module is deprecated and will be removed in v6.0. "
    "Please update your imports to use 'diba.schemas' instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export everything from schemas for backward compatibility
from diba.schemas import *  # noqa: F401, F403
from diba.schemas.diba_exception import *  # noqa: F401, F403
from diba.schemas.kr_literals import *  # noqa: F401, F403
from diba.schemas.kr_models import *  # noqa: F401, F403
from diba.schemas.settings_models import *  # noqa: F401, F403
from diba.schemas.chart_template_model import *  # noqa: F401, F403

__all__ = [
    # Re-export from schemas
    "DibaException",
    # kr_literals
    "ZodiacType",
    "Sign",
    "SignNumbers",
    "AspectMovementType",
    "Houses",
    "HouseNumbers",
    "AstrologicalPoint",
    "Element",
    "Quality",
    "ChartType",
    "PointType",
    "LunarPhaseEmoji",
    "LunarPhaseName",
    "SiderealMode",
    "HousesSystemIdentifier",
    "PerspectiveType",
    "SignsEmoji",
    "DibaChartTheme",
    "DibaChartLanguage",
    "RelationshipScoreDescription",
    "CompositeChartType",
    "AspectName",
    # kr_models
    "AstrologicalSubjectModel",
    "CompositeSubjectModel",
    "DibaPointModel",
    "AspectModel",
    "ActiveAspect",
    "SingleChartAspectsModel",
    "DualChartAspectsModel",
    "ElementDistributionModel",
    "QualityDistributionModel",
    "SingleChartDataModel",
    "DualChartDataModel",
    # settings_models
    "DibaSettingsModel",
    # chart_template_model
    "ChartTemplateModel",
]
