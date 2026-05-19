"""Tests for study-level trial recording outputs."""

from __future__ import annotations

import json
from pathlib import Path

from auto_research.core.recorder import TrialRecorder, build_trial_record


def test_trial_recorder_creates_tsv_and_jsonl(tmp_path: Path) -> None:
    recorder = TrialRecorder(str(tmp_path))
    record = build_trial_record(
        task_name="demo_hpo",
        trial_id="trial_000001",
        status="completed",
        score=88.5,
        trial_config={"lr": 0.0003, "batch_size": 64},
        metrics={"mAP": 75.3, "rank1": 84.2},
        command=["python", "train.py", "--lr", "0.0003"],
        trial_dir=str(tmp_path / "trial_000001"),
        start_time="2026-04-26T00:00:00+00:00",
        end_time="2026-04-26T00:01:00+00:00",
        duration_seconds=60.0,
        error_message="",
    )

    assert recorder.record_trial(record) is True

    tsv_text = recorder.tsv_path.read_text(encoding="utf-8")
    jsonl_lines = recorder.jsonl_path.read_text(encoding="utf-8").splitlines()

    assert "task_name\ttrial_id\tstatus\tscore" in tsv_text
    assert "demo_hpo" in tsv_text
    assert len(jsonl_lines) == 1
    payload = json.loads(jsonl_lines[0])
    assert payload["trial_id"] == "trial_000001"
    assert payload["metrics"]["mAP"] == 75.3


def test_trial_recorder_appends_multiple_records(tmp_path: Path) -> None:
    recorder = TrialRecorder(str(tmp_path))

    for index in range(2):
        recorder.record_trial(
            build_trial_record(
                task_name="demo_hpo",
                trial_id=f"trial_{index + 1:06d}",
                status="completed",
                score=80.0 + index,
                trial_config={"index": index},
                metrics={"mAP": 70.0 + index},
                command=["python", "train.py"],
                trial_dir=str(tmp_path / f"trial_{index + 1:06d}"),
                start_time="2026-04-26T00:00:00+00:00",
                end_time="2026-04-26T00:01:00+00:00",
                duration_seconds=60.0,
                error_message="",
            )
        )

    assert len(recorder.jsonl_path.read_text(encoding="utf-8").splitlines()) == 2
    assert len(recorder.tsv_path.read_text(encoding="utf-8").splitlines()) == 3


def test_trial_recorder_swallows_write_failures(tmp_path: Path, monkeypatch) -> None:
    recorder = TrialRecorder(str(tmp_path))

    def broken_append_tsv(self, record):  # noqa: ANN001
        raise OSError("disk full")

    monkeypatch.setattr(TrialRecorder, "_append_tsv", broken_append_tsv)

    success = recorder.record_trial(
        build_trial_record(
            task_name="demo_hpo",
            trial_id="trial_000001",
            status="failed",
            score=-1.0,
            trial_config={},
            metrics={},
            command=[],
            trial_dir=str(tmp_path / "trial_000001"),
            start_time="2026-04-26T00:00:00+00:00",
            end_time="2026-04-26T00:00:01+00:00",
            duration_seconds=1.0,
            error_message="boom",
        )
    )

    assert success is False
