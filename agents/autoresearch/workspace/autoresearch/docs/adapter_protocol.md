# Adapter Protocol

This document describes the contract between AutoResearch and external training projects.

Important boundary:

AutoResearch supports "arbitrary training projects" only when that project can be launched from the command line and can output parseable metrics, or when you implement a custom `TrainingAdapter`.

## `TrainingAdapter` Interface

The base protocol lives in `auto_research/adapters/base.py`.

Required methods:

### `prepare_trial(self, trial_config: dict, trial_dir: str) -> dict`

Purpose:

- validate or transform sampled hyperparameters
- create files needed by a trial
- prepare a run-specific config or environment

Typical work:

- write a temporary YAML config
- expand relative paths
- inject `trial_dir` into the prepared payload

### `build_command(self, prepared_config: dict, trial_dir: str) -> list[str]`

Purpose:

- convert the prepared configuration into a safe subprocess command

Requirements:

- return `list[str]`
- do not use `shell=True`
- raise clear errors for invalid or incomplete inputs

### `run_trial(self, command: list[str], trial_dir: str, timeout: int, env: dict | None = None) -> dict`

Purpose:

- launch training and capture execution details

Expected behavior:

- execute the command safely
- support timeouts
- capture stdout and stderr
- return structured status information instead of crashing the study

### `collect_metrics(self, trial_dir: str) -> dict`

Purpose:

- read trial outputs and return metrics

Typical sources:

- JSON result files
- YAML result files
- plain-text metrics files
- project-specific artifacts

### `sample_config(self, trial) -> dict`

Purpose:

- sample hyperparameters from an Optuna trial

Notes:

- built-in adapters usually delegate this to the shared search-space layer
- custom adapters can keep this thin unless they need extra logic

### `validate_config(self, trial_config: dict) -> tuple[bool, str]`

Purpose:

- validate one sampled config before training starts

Expected output:

- `(True, "Trial configuration is valid.")`
- or `(False, "clear reason here")`

## How To Write a Custom Adapter

The easiest path is to subclass `TrainingAdapter` directly when your project needs a special launch or metric-collection flow.

Recommended process:

1. Decide what a valid `trial_config` looks like.
2. Decide how the target project should receive those parameters.
3. Decide where metrics will be written.
4. Implement safe command construction.
5. Return metrics as a plain dictionary.

Skeleton:

```python
from __future__ import annotations

from typing import Any

from auto_research.adapters.base import TrainingAdapter


class MyAdapter(TrainingAdapter):
    def prepare_trial(self, trial_config: dict[str, Any], trial_dir: str) -> dict[str, Any]:
        return {"trial_dir": trial_dir, "parameters": dict(trial_config)}

    def build_command(self, prepared_config: dict[str, Any], trial_dir: str) -> list[str]:
        return ["python", "train.py", "--output-dir", trial_dir]

    def run_trial(
        self,
        command: list[str],
        trial_dir: str,
        timeout: int,
        env: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        # You can call subprocess directly or reuse shared logic in a subclass.
        ...

    def collect_metrics(self, trial_dir: str) -> dict[str, Any]:
        return {}

    def sample_config(self, trial) -> dict[str, Any]:
        return {"lr": trial.suggest_float("lr", 1e-5, 1e-3, log=True)}

    def validate_config(self, trial_config: dict[str, Any]) -> tuple[bool, str]:
        return True, "Trial configuration is valid."
```

Practical advice:

- keep all trial outputs inside `trial_dir`
- do not hardcode project-global temp files
- return clear error messages when config preparation fails
- treat missing metrics as a recoverable trial failure, not as a process-wide crash

## Reusing `SubprocessAdapter`

If your project is already command-line friendly, you usually do not need a brand-new adapter.

Prefer:

- `SubprocessAdapter` for general command templates
- `PyTorchYamlAdapter` for YAML-config projects
- `PyTorchArgparseAdapter` for CLI-flag projects

Write a custom adapter only when the target project needs a different preparation or collection flow.

## Metrics Output Specification

AutoResearch expects metrics to become a flat or nested dictionary that can be normalized into scalar values.

Recommended output files:

- `metrics.json`
- `result.json`
- `summary.json`

Recommended JSON example:

```json
{
  "mAP": 76.3,
  "rank1": 84.5,
  "loss": 0.72
}
```

Nested metrics are allowed:

```json
{
  "test_metrics": {
    "mAP": 0.763,
    "top1": 0.845
  },
  "final_loss": 0.72
}
```

Built-in normalization supports:

- `mAP`, `map`, `test_metrics/mAP`
- `Rank-1`, `rank1`, `top1`, `test_metrics/top1`
- `loss`, `final_loss`

Scale handling:

- `0.763` and `76.3` are both accepted for percentage-style metrics such as `mAP`
- `84.5%` is also accepted
- non-numeric values are ignored by built-in normalizers

Log parsing currently recognizes patterns like:

- `mAP: 75.3`
- `Rank-1: 84.2`
- `rank1=84.2`
- `loss: 0.812`

If your project writes metrics differently, implement `collect_metrics()` in your adapter or adjust your training output.

## Search Space Specification

Task cards define search space in YAML and the shared search-space module converts it into Optuna suggestions.

Supported types:

```yaml
search_space:
  lr:
    type: float
    low: 1e-5
    high: 1e-3
    log: true
  epochs:
    type: int
    low: 5
    high: 20
    step: 1
  batch_size:
    type: categorical
    choices: [32, 64]
  use_warmup:
    type: bool
```

Rules:

- `float` supports `low`, `high`, and optional `log`
- `int` supports `low`, `high`, and optional `step`
- `categorical` supports numeric, string, and boolean values
- `bool` is sampled as `False` or `True`

Validation should fail early with clear errors when:

- a required field is missing
- bounds are invalid
- a categorical choice uses an unsupported type

## Safety Constraints

All adapters should respect the framework safety model.

Built-in checks include:

- `shell=True` is forbidden
- the executable must be in the allowlist
- default allowlist is `python` and `python3`
- dangerous commands such as `rm`, `rm -rf`, `shutdown`, `reboot`, `mkfs`, and `dd` are blocked
- `trial_dir` must stay inside `output_root`
- NaN and Inf metrics are rejected
- duplicate config hashes are rejected inside one study run
- the study can stop after too many consecutive failures

Task-card example:

```yaml
safety:
  max_consecutive_failures: 5
  allow_commands:
    - python
    - python3
```

Guidance for custom adapters:

- never use `shell=True`
- always validate `trial_dir`
- keep commands explicit and structured as `list[str]`
- treat unsafe launches as invalid trials rather than uncaught exceptions
- make sure failures in one trial do not crash the full study
