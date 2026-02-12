"""Varga dispatcher wrapper."""

from __future__ import annotations

from typing import Any, Iterable, Mapping, Optional

from diba.vedic.vargas import compute_varga as _compute_varga
from diba.vedic.vargas import compute_vargas as _compute_vargas


def compute_varga(
    core_objects: Mapping[str, Any],
    chart_id: str,
    method: Optional[int] = None,
):
    return _compute_varga(core_objects, chart_id, method=method)


def compute_vargas(
    core_objects: Mapping[str, Any],
    charts: Iterable[str],
    methods: Optional[Mapping[str, int]] = None,
):
    return _compute_vargas(core_objects, charts, methods=methods)
