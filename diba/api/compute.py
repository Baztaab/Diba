"""API-level orchestration containers for composed capability outputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict

from diba.engine.state import VedicState


@dataclass
class ChartAnalysis:
    base_state: VedicState
    results: Dict[str, Any] = field(default_factory=dict)

    def add_result(self, key: str, value: Any) -> None:
        self.results[key] = value
