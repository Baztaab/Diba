"""Generate canonical ayanamsa enum from registry selectable IDs."""

from __future__ import annotations

from pathlib import Path

from diba.vedic.registry import list_ayanamsa_ids


def _enum_member_name(value: str) -> str:
    return value.upper().replace("-", "_")


def render_enum_source() -> str:
    """Render the generated enum module source."""
    values = list_ayanamsa_ids(selectable_only=True, include_aliases=False)
    lines = [
        '"""Auto-generated canonical ayanamsa enum. Do not edit manually."""',
        "",
        "from __future__ import annotations",
        "",
        "from enum import Enum",
        "",
        "",
        "class AyanamsaIdEnum(str, Enum):",
        '    """Canonical selectable ayanamsa IDs."""',
    ]
    for value in values:
        lines.append(f'    {_enum_member_name(value)} = "{value}"')
    lines.append("")
    return "\n".join(lines)


def write_enum_file(target: Path) -> None:
    """Write generated enum source to target path."""
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_enum_source(), encoding="utf-8")


def main() -> None:
    """Entrypoint for direct execution."""
    root = Path(__file__).resolve().parents[1]
    write_enum_file(root / "diba" / "domain" / "enums" / "generated_ayanamsa_enum.py")


if __name__ == "__main__":
    main()
