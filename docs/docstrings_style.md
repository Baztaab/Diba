# Docstrings Style Guide

This project follows PEP 257 for structure, Google-style docstrings for readability,
and type hints in signatures. Sphinx Napoleon should parse these without changes.

Golden Rules
- Types live in signatures. Do not repeat types in docstrings unless units or mode
  clarity are required (e.g., degrees vs radians, UTC vs local, sidereal vs tropical).
- Every public API docstring includes these sections in this order:
  Args, Returns, Raises, Notes, Examples.
- Summary line + blank line are mandatory (PEP 257).

Module Docstring Template
```python
"""
<One-line summary.>

<2-5 lines: what this module provides, for whom, and what it deliberately does not do.>

Public API:
- <ClassOrFunc1>
- <ClassOrFunc2>

Notes:
- Thread-safety: <lock policy / global state policy>
- Determinism: <if applicable>
- Contract: <stability or versioning policy>
"""
```

Function or Method Template (Google-style)
```python
def example(x: int, y: int) -> int:
    """Compute something deterministic.

    Short behavior description. Mention important invariants and boundaries.

    Args:
        x: Meaning of x.
        y: Meaning of y.

    Returns:
        The computed value.

    Raises:
        ValueError: If inputs are invalid.

    Notes:
        - Thread-safety: <lock policy / global state policy>
        - Determinism: <if applicable>
        - Contract: <stability or versioning policy>

    Examples:
        >>> example(1, 2)
        3
    """
```

Project Notes Policy
- Thread-safety and lock boundaries must be stated in Notes for any API that
  touches SwissEph or global runtime state.
- Determinism claims must be explicit when outputs are expected to be stable for
  identical inputs (and same ephemeris version).
- Contract stability must be stated for JSON payloads or schema outputs.

PR Checklist (Docstrings)
- Summary line + blank line present.
- Args/Returns/Raises/Notes/Examples present and accurate.
- No type duplication unless units or mode clarity is needed.
- Notes include thread-safety and contract stability where relevant.
