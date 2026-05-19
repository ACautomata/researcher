"""Basic smoke tests for package scaffolding."""

from __future__ import annotations

from pathlib import Path
import sys

from auto_research import __version__
from auto_research.adapters.base import TrainingAdapter
from auto_research.core.base import RunContext, RunResult
from auto_research.core.types import ExperimentResult, TrialRecord, TrialStatus
from auto_research.search_space.base import SearchSpaceDefinition, validate_search_space
from auto_research.task_cards.base import TaskCard


def test_version_exists() -> None:
    assert isinstance(__version__, str)


def test_core_placeholders_can_be_instantiated() -> None:
    context = RunContext(trial_id="trial-001", task_name="demo")
    result = RunResult(score=0.0)
    search_space = SearchSpaceDefinition()
    task_card = TaskCard(name="demo", adapter="command", entrypoint="python train.py")

    assert context.task_name == "demo"
    assert result.score == 0.0
    assert search_space.parameters == {}
    assert task_card.adapter == "command"
    assert validate_search_space(search_space.parameters) == (True, "Search space is valid.")


class DummyAdapter(TrainingAdapter):
    def prepare_trial(self, trial_config: dict, trial_dir: str) -> dict:
        return {"trial_dir": trial_dir, **trial_config}

    def build_command(self, prepared_config: dict, trial_dir: str) -> list[str]:
        return [
            sys.executable,
            "-c",
            "from pathlib import Path; Path('metric.txt').write_text('1.0', encoding='utf-8')",
        ]

    def collect_metrics(self, trial_dir: str) -> dict:
        metric_path = Path(trial_dir) / "metric.txt"
        return {"score": float(metric_path.read_text(encoding='utf-8'))}

    def sample_config(self, trial) -> dict:
        return {"lr": 0.001}

    def validate_config(self, trial_config: dict) -> tuple[bool, str]:
        return True, "valid"


def test_core_types_can_be_instantiated() -> None:
    result = ExperimentResult(status=TrialStatus.COMPLETED, score=0.9)
    record = TrialRecord(trial_id="trial-001", result=result)

    assert result.status is TrialStatus.COMPLETED
    assert record.result is result


def test_training_adapter_can_run_generic_command(tmp_path: Path) -> None:
    adapter = DummyAdapter()
    command = adapter.build_command({}, str(tmp_path))

    run_info = adapter.run_trial(command=command, trial_dir=str(tmp_path), timeout=10)
    metrics = adapter.collect_metrics(str(tmp_path))

    assert run_info["status"] == TrialStatus.COMPLETED.value
    assert run_info["return_code"] == 0
    assert metrics["score"] == 1.0
