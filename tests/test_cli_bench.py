from __future__ import annotations

import json

from diba._cli.app import dispatch


def test_bench_state_base_json_contract(capsys):
    code = dispatch(["bench", "state-base", "--n", "3", "--format", "json"])
    captured = capsys.readouterr()

    assert code == 0
    payload = json.loads(captured.out)
    assert payload["benchmark"] == "state-base"
    assert payload["sample_size"] == 3
    assert payload["tolerance_profile"] in {"ci", "golden"}
    assert payload["cache_mode"] in {"warm-cache", "cold-cache"}
    assert payload["ephemeris_io"] in {"included", "excluded"}
    assert isinstance(payload["median_ms"], float)
    assert isinstance(payload["p95_ms"], float)
    assert isinstance(payload["charts_per_sec"], float)
    assert isinstance(payload["cpu_model"], str)
    assert isinstance(payload["machine"], str)


def test_bench_state_base_include_ephe_io_flag(capsys):
    code = dispatch(
        [
            "bench",
            "state-base",
            "--n",
            "2",
            "--include-ephe-io",
            "--format",
            "json",
        ]
    )
    captured = capsys.readouterr()

    assert code == 0
    payload = json.loads(captured.out)
    assert payload["ephemeris_io"] == "included"


def test_bench_state_base_rejects_non_positive_n(capsys):
    code = dispatch(["bench", "state-base", "--n", "0", "--format", "json"])
    captured = capsys.readouterr()

    assert code == 2
    assert "Error:" in captured.err
