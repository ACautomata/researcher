# AutoResearch Agent Runbook

This directory contains the AutoResearch validation framework as part of the `autoresearch` OpenClaw agent workspace. It is intentionally kept under `agents/autoresearch/workspace/` so the code, examples, tests, and case reports are reviewed as agent-owned research infrastructure instead of a loose repository-level script drop.

## Purpose

AutoResearch turns research ideas or RTS task specifications into executable hyperparameter optimization studies. The current validation case uses the CVPR 2022 NCL long-tailed visual recognition paper as a realistic proxy experiment.

The NCL case does not reproduce the full paper. It tests whether the framework can:

- accept an RTS-style task definition,
- generate requirement and implementation plans,
- run a bounded HPO study,
- record per-trial metrics and configurations,
- select the best trial,
- produce quantitative and qualitative validation evidence.

## Layout

- `auto_research/`: framework source code.
- `tests/`: unit and workflow tests.
- `examples/ncl_case/`: NCL-derived RTS, task card, and proxy training entry point.
- `docs/ncl_case_validation_report_zh.md`: Chinese validation report.
- `docs/ncl_case_validation_report.md`: English validation report.

Runtime outputs such as `outputs/`, `logs/`, `.pytest_tmp/`, `.tmp/`, `.venv/`, and `generated_projects/` are ignored by the repository and should not be committed.

## Validation Commands

From this directory:

```bash
python -m pip install -e . pytest
python -m pytest -v --tb=short
python -m auto_research.core.study \
  --task-card examples/ncl_case/ncl_proxy_task_card.yaml \
  --study-name ncl-case-validation \
  --storage outputs/ncl_case_validation/study.db \
  --output-root outputs/ncl_case_validation \
  --n-trials 12 \
  --direction maximize \
  --seed 42
```

Known local test caveat: the generated PyTorch project validation tests require `torch`. In the current Python 3.14 environment those tests fail with `ModuleNotFoundError: No module named 'torch'`; the remaining tests pass.
