from __future__ import annotations

from pathlib import Path

RESEARCH_RULES: dict[str, dict[str, list[str]]] = {
    "phase_a_core_json": {
        "paths": [
            "diba/engine/state.py",
            "diba/chart/service.py",
            "diba/serializers/static_chart_v0_1.py",
            "diba/serializers/api_v1.py",
        ],
        "artifacts": [
            "project_memory/research/phase-a-astronomy-base-pyjhora-extract.md",
            "project_memory/research/phase-a-d1-chart-pyjhora-extract.md",
            "project_memory/research/phase-a-serializer-contract-pyjhora-extract.md",
        ],
    },
    "phase_b_panchanga": {
        "paths": [
            "diba/panchanga/service.py",
            "diba/panchanga/calculators/tithi.py",
            "diba/panchanga/calculators/nakshatra.py",
            "diba/panchanga/calculators/vara.py",
            "diba/panchanga/calculators/yoga.py",
            "diba/panchanga/calculators/karana.py",
        ],
        "artifacts": [
            "project_memory/research/phase-b-panchanga-baseline-pyjhora-extract.md",
            "project_memory/research/phase-b-tithi-boundaries-pyjhora-extract.md",
        ],
    },
    "phase_c_vimshottari": {
        "paths": [
            "diba/dasha/service.py",
            "diba/dasha/graha/vimsottari.py",
        ],
        "artifacts": [
            "project_memory/research/phase-c-vimshottari-baseline-pyjhora-extract.md",
            "project_memory/research/phase-c-dasha-time-contract-pyjhora-extract.md",
        ],
    },
}

REQUIRED_SECTIONS = [
    "## PyJHora Source Paths",
    "## Functions Reviewed",
    "## Algorithm and Formula Steps",
    "## Inputs/Outputs and Contracts",
    "## Boundary and Edge Cases",
    "## ADR Alignment Notes",
]


def test_research_artifacts_exist_for_capabilities() -> None:
    root = Path(__file__).resolve().parents[1]

    for rule_name, rule in RESEARCH_RULES.items():
        touched = any((root / rel).exists() for rel in rule["paths"])
        if not touched:
            continue

        for rel in rule["artifacts"]:
            p = root / rel
            assert p.exists(), f"Missing research artifact required by {rule_name}: {rel}"

            text = p.read_text(encoding="utf-8")
            for marker in REQUIRED_SECTIONS:
                assert marker in text, f"Research artifact {rel} missing section: {marker}"
