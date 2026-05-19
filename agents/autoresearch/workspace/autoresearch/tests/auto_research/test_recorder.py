"""Focused tests for trial recording outputs."""

from __future__ import annotations

import json
from pathlib import Path

from auto_research.core.recorder import TrialRecorder, build_trial_record


def test_trial_recorder_writes_tsv_and_jsonl(tmp_path: Path) -> None:
    recorder = TrialRecorder(str(tmp_path))
    record = build_trial_record(
        task_name="dummy_hpo",
        trial_id="trial_000001",
        status="completed",
        score=93.2,
        trial_config={"lr": 0.0003, "batch_size": 64},
        metrics={"mAP": 76.3, "rank1": 84.5, "loss": 0.72},
        command=["python", "examples/dummy_train.py"],
        trial_dir=str(tmp_path / "trial_000001"),
        start_time="2026-04-26T00:00:00+00:00",
        end_time="2026-04-26T00:00:01+00:00",
        duration_seconds=1.0,
        error_message="",
    )

    assert recorder.record_trial(record) is True
    assert recorder.tsv_path.exists()
    assert recorder.jsonl_path.exists()

    tsv_text = recorder.tsv_path.read_text(encoding="utf-8")
    payload = json.loads(recorder.jsonl_path.read_text(encoding="utf-8").splitlines()[0])

    assert "task_name\ttrial_id\tstatus\tscore" in tsv_text
    assert "dummy_hpo" in tsv_text
    assert payload["metrics"]["mAP"] == 76.3


def test_trial_recorder_returns_false_when_append_fails(tmp_path: Path, monkeypatch) -> None:
    recorder = TrialRecorder(str(tmp_path))

    def broken_append_jsonl(self, record):  # noqa: ANN001
        raise OSError("disk full")

    monkeypatch.setattr(TrialRecorder, "_append_jsonl", broken_append_jsonl)

    success = recorder.record_trial(
        build_trial_record(
            task_name="dummy_hpo",
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
