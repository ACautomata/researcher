#!/usr/bin/env python3
"""Regression tests for report_clawprobench._load_base.

Codex P2 #2 (PR #103): ``BENCH_BASE_RESULTS_JSON`` may carry a full previous
summary base64-encoded as a repo secret. That blob easily exceeds NAME_MAX, so
``Path(raw).exists()`` raises ``OSError(ENAMETOOLONG)`` on the Linux runner
(pathlib does not swallow ENAMETOOLONG the way os.path.exists does) before the
base64 fallback runs, crashing the aggregate step. The fix must catch OSError
and still decode the base64.

Run: ``python3 .github/bench/test_report_clawprobench.py`` (or pytest).
"""
from __future__ import annotations

import base64
import importlib.util
import json
import os
import pathlib
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location(
    "report_clawprobench", HERE / "report_clawprobench.py"
)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)


def _encode(payload: dict) -> str:
    return base64.b64encode(json.dumps(payload).encode("utf-8")).decode("ascii")


def test_long_base64_decodes_without_raising() -> None:
    """A >NAME_MAX base64 secret decodes; OSError from the path probe is caught."""
    payload = {
        "avg_score": 0.42,
        "pass_at_3_rate": 0.5,
        "pass_cubed_rate": 0.3,
        "scenarios": [{"id": f"research_paper_review_{i:03d}"} for i in range(40)],
    }
    raw = _encode(payload)
    assert len(raw) > 255, f"setup: expected >255 char base64, got {len(raw)}"
    os.environ["BENCH_BASE_SUMMARY"] = raw

    # Simulate the Linux runner: Path(raw).exists() raises ENAMETOOLONG for the
    # long blob. (macOS APFS returns False instead, so monkeypatch to force the
    # cross-platform red-before-fix path.)
    orig_exists = pathlib.Path.exists

    def raise_enametoolong(self):  # type: ignore[no-untyped-def]
        if str(self) == raw:
            raise OSError(36, "File name too long")
        return orig_exists(self)

    pathlib.Path.exists = raise_enametoolong  # type: ignore[method-assign]
    try:
        result = mod._load_base()
    finally:
        pathlib.Path.exists = orig_exists  # type: ignore[method-assign]
        os.environ.pop("BENCH_BASE_SUMMARY", None)

    assert result == payload, f"expected decoded payload, got {result!r}"


def test_short_path_still_loaded(tmp_path: pathlib.Path) -> None:
    """A real file path still loads (the OSError guard does not skip it)."""
    payload = {"avg_score": 0.7, "pass_at_3_rate": 0.6, "pass_cubed_rate": 0.4}
    f = tmp_path / "base.json"
    f.write_text(json.dumps(payload))
    os.environ["BENCH_BASE_SUMMARY"] = str(f)
    try:
        result = mod._load_base()
    finally:
        os.environ.pop("BENCH_BASE_SUMMARY", None)
    assert result == payload, f"expected {payload}, got {result!r}"


def test_missing_env_returns_none() -> None:
    os.environ.pop("BENCH_BASE_SUMMARY", None)
    assert mod._load_base() is None


def test_garbage_base64_returns_none() -> None:
    """Non-path, non-decodable input does not raise."""
    os.environ["BENCH_BASE_SUMMARY"] = "!!! not valid base64 and not a path !!!"
    try:
        assert mod._load_base() is None
    finally:
        os.environ.pop("BENCH_BASE_SUMMARY", None)


def main() -> int:
    test_long_base64_decodes_without_raising()
    with tempfile.TemporaryDirectory() as d:
        test_short_path_still_loaded(pathlib.Path(d))
    test_missing_env_returns_none()
    test_garbage_base64_returns_none()
    print("test_report_clawprobench: all tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
