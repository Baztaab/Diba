"""API-level orchestration containers for composed capability outputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict

from diba.engine.state import VedicState


@dataclass
class ChartAnalysis:
    """Aggregate capability outputs built from one base state."""

    base_state: VedicState
    results: Dict[str, Any] = field(default_factory=dict)

    def add_result(self, key: str, value: Any) -> None:
        """Store one capability result under a stable key."""
        self.results[key] = value
