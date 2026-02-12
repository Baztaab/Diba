"""Public-boundary conversion helpers for 0-based and 1-based ids."""

from __future__ import annotations


def rasi0_to_rasi1(rasi_index: int) -> int:
    if not (0 <= int(rasi_index) <= 11):
        raise ValueError(f"rasi_index out of range: {rasi_index}")
    return int(rasi_index) + 1


def rasi1_to_rasi0(rasi_id: int) -> int:
    if not (1 <= int(rasi_id) <= 12):
        raise ValueError(f"rasi_id out of range: {rasi_id}")
    return int(rasi_id) - 1

