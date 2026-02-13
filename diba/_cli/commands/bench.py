"""Benchmark CLI commands."""

from __future__ import annotations

import math
import os
import platform
import statistics
import time
from typing import Any, Dict

from diba._cli.errors import CLIError
from diba.core.contracts import tolerance_profile
from diba.domain.models.common import BirthData, PlaceInput
from diba.engine import AstrologySettings, AstronomyContext, DibaEngine


def _benchmark_subject() -> BirthData:
    return BirthData(
        year=1990,
        month=1,
        day=1,
        hour=12,
        minute=0,
        seconds=0.0,
        tz_str="UTC",
        place=PlaceInput(lat=0.0, lon=0.0, altitude=0.0),
    )


def _p95(values: list[float]) -> float:
    ordered = sorted(values)
    idx = max(0, math.ceil(0.95 * len(ordered)) - 1)
    return ordered[idx]


def run_bench_state_base_command(args) -> Dict[str, Any]:
    """Run base-state benchmark and return machine-readable metrics."""
    sample_size = int(args.n)
    if sample_size <= 0:
        raise CLIError("--n must be > 0.")

    profile_name = (args.tol_profile or os.getenv("DIBA_TOL_PROFILE", "ci")).strip().lower()
    profile = tolerance_profile(profile_name)

    engine = DibaEngine(
        session_ctx=AstronomyContext(ephe_path=args.ephe_path),
        astro_settings=AstrologySettings(),
    )
    subject = _benchmark_subject()

    if not bool(args.include_ephe_io):
        engine.state(subject)
    if bool(args.warm_cache):
        engine.state(subject)

    durations_ms: list[float] = []
    started = time.perf_counter()
    with engine.session():
        for _ in range(sample_size):
            t0 = time.perf_counter()
            engine.state(subject)
            durations_ms.append((time.perf_counter() - t0) * 1000.0)
    total_seconds = time.perf_counter() - started

    cpu_model = platform.processor() or platform.machine()
    charts_per_sec = float(sample_size) / total_seconds if total_seconds > 0 else 0.0

    return {
        "benchmark": "state-base",
        "sample_size": sample_size,
        "tolerance_profile": profile_name,
        "tolerance": {
            "angle_deg": profile.angle_deg,
            "time_seconds": profile.time_seconds,
        },
        "cache_mode": "warm-cache" if bool(args.warm_cache) else "cold-cache",
        "ephemeris_io": "included" if bool(args.include_ephe_io) else "excluded",
        "cpu_model": cpu_model,
        "machine": platform.platform(),
        "median_ms": round(float(statistics.median(durations_ms)), 6),
        "p95_ms": round(float(_p95(durations_ms)), 6),
        "total_seconds": round(float(total_seconds), 6),
        "charts_per_sec": round(float(charts_per_sec), 6),
    }
