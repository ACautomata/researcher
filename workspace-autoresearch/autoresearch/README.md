# AutoResearch

AutoResearch is a research automation framework that connects early research ideas to runnable experiments.

It now covers two layers of the workflow:

- Upstream planning: represent an idea, paper, or manual task as RTS, then generate a stable `requirement.md`.
- Downstream execution: connect a generated or external training project to existing adapters, run trials, parse metrics, record results, and perform hyperparameter optimization.

AutoResearch does not bundle model training code and does not rewrite your trainer. It coordinates external training projects through task cards and adapters.

## Pipeline

```text
idea / paper / manual input
-> RTS (Research Task Specification)
-> requirement.md
-> implementation_plan
-> generated project
-> task_card.yaml / adapter config
-> existing auto-training module
-> metrics, records, HPO results
```

Implemented in this repository:

- RTS schema, IO, and validation.
- RTS to `requirement.md` generation.
- Adapter-based automatic training and hyperparameter optimization.
- Metric parsing, scoring, experiment recording, and safety checks.

Not implemented yet:

- automatic paper or idea reader
- implementation plan generation
- generated project creation
- automatic task card generation from RTS

## Project Structure

```text
auto_research/
  adapters/
    base.py
    pytorch_argparse_adapter.py
    pytorch_yaml_adapter.py
    subprocess_adapter.py
  core/
    objective.py
    recorder.py
    safety.py
    study.py
    task_card.py
    types.py
  evaluators/
    json_parser.py
    log_parser.py
  planning/
    requirement_generator.py
  rts/
    schema.py
    validation.py
    io.py
  search_space/
  task_cards/
  templates_docs/
    requirement_template.md
  utils/
docs/
examples/
tests/
```

Core responsibilities:

- `auto_research.rts`: the Research Task Specification protocol, including schema, YAML/JSON IO, and validation.
- `auto_research.planning`: deterministic planning documents such as `requirement.md`.
- `auto_research.adapters`: bridges sampled parameters to an external training project.
- `auto_research.search_space`: validates and samples task-card search spaces.
- `auto_research.evaluators`: parses JSON and log metrics.
- `auto_research.core.task_card`: loads, validates, and instantiates adapters from YAML task cards.
- `auto_research.core.objective`: runs one Optuna trial end to end.
- `auto_research.core.study`: starts Optuna studies from the command line.
- `auto_research.core.recorder`: writes `results.tsv` and `results.jsonl`.
- `auto_research.core.safety`: enforces command allowlists, path checks, duplicate-config checks, NaN/Inf checks, and failure-stop policy.

## Installation

Requirements:

- Python 3.10+
- `optuna`
- `pyyaml`

Install locally:

```bash
pip install -e .
```

Optional dependency group:

```bash
pip install -e .[wandb]
```

## Quick Start: RTS to Requirement Document

Create an example RTS for an RGB-IR person re-identification task:

```bash
python -m auto_research.cli init-rts \
  --project-name rgb_ir_attention_test \
  --output ./rts_example.yaml
```

Validate the RTS:

```bash
python -m auto_research.cli validate-rts \
  --rts ./rts_example.yaml
```

Generate `requirement.md`:

```bash
python -m auto_research.cli rts-to-requirement \
  --rts ./rts_example.yaml \
  --output ./requirement.md
```

If the RTS is invalid, the command refuses to generate by default and prints validation errors. To generate anyway:

```bash
python -m auto_research.cli rts-to-requirement \
  --rts ./rts_example.yaml \
  --output ./requirement.md \
  --allow-invalid
```

With `--allow-invalid`, the generated document starts with a validation warning.

## What RTS Contains

RTS is the intermediate representation between research understanding and engineering execution. It is designed to be specific enough for later project generation, but independent from any one training repository.

Important sections include:

- `meta`: project name, source type, source path, creation time, description.
- `task`: task type, research problem, learning paradigm.
- `goal`: primary metric, optimization direction, secondary metrics.
- `input` and `output`: modalities, data format, shape, output type, dimension.
- `baseline`: selected template or fallback baseline.
- `model`: backbone, components, heads.
- `losses`: loss names, weights, and params.
- `training`: optimizer, scheduler, batch size, epochs, learning rate.
- `datasets`: dataset names, paths, splits, notes.
- `search_space`: HPO parameters that can later map into `auto_research/search_space`.
- `ablation`: ablation study ideas.
- `implementation`: required files and expected modules for a future generated project.
- `validation`: checks such as import, dummy forward, backward, one-batch train, config load, checkpoint save/load.
- `adapter`: intended bridge to existing adapters such as `pytorch_yaml`, `pytorch_argparse`, or `subprocess`.

## Requirement Document

`requirement.md` is generated from RTS. It is not a paper summary and not final code. It is the engineering contract for later agents or tools that will produce an implementation plan, generated project, task card, and adapter configuration.

The generated document has a stable 18-section structure:

1. Document Role in the Auto-Research Pipeline
2. Project Overview
3. Research Problem and Goal
4. Task Definition
5. Input and Output Specification
6. Baseline Template Requirement
7. Model Requirements
8. Loss Function Requirements
9. Dataset Requirements
10. Training Requirements
11. Evaluation Metrics
12. Hyperparameter Search Space
13. Ablation Study Design
14. Generated Project Requirements
15. Validation Criteria
16. Interface with Existing Auto-Training Module
17. Risks and Manual Confirmation Items
18. Summary for Next Stage

The template reference lives at `auto_research/templates_docs/requirement_template.md`.

## Quick Start: Run Automatic Training / HPO

This repository ships with a fake training script at `examples/dummy_train.py`. It does not need a GPU and does not train a real model. It simulates a run, writes `metrics.json`, and prints parseable metrics to stdout.

Run the dummy HPO example:

```bash
python -m auto_research.core.study \
  --task-card examples/task_cards/dummy_hpo.yaml \
  --n-trials 10
```

Expected outputs:

- `outputs/dummy_hpo/trial_000001/metrics.json`
- `outputs/dummy_hpo/trial_000001/train_stdout.log`
- `outputs/dummy_hpo/trial_000001/train_stderr.log`
- `outputs/dummy_hpo/trial_000001/trial_record.json`
- `outputs/dummy_hpo/results.tsv`
- `outputs/dummy_hpo/results.jsonl`

Useful study options:

- `--study-name`: override the Optuna study name.
- `--storage`: pass a storage URL or a local SQLite path such as `runs/study.db`.
- `--timeout`: set a study-level Optuna timeout.
- `--direction`: `maximize` or `minimize`.
- `--output-root`: override the task-card output root.
- `--dry-run`: print commands without executing them.
- `--seed`: set the Optuna sampler seed.

## Task Cards

A task card describes how AutoResearch should launch an external training project, what parameters to search, and how to score each trial.

Minimal example:

```yaml
task_name: demo_hpo

adapter:
  type: subprocess
  command_template:
    - python
    - examples/dummy_train.py
    - --lr
    - "{lr}"
    - --batch-size
    - "{batch_size}"
    - --output-dir
    - "{trial_dir}"

search_space:
  lr:
    type: float
    low: 1e-5
    high: 1e-3
    log: true
  batch_size:
    type: categorical
    choices: [32, 64]

score:
  primary_metric: mAP
  invalid_score: -1000000000

constraints:
  timeout: 300
  max_trials: 20
```

Main fields:

- `task_name`: logical task name and output folder name.
- `adapter`: how to launch the external project.
- `search_space`: Optuna sampling definition.
- `score`: how to convert parsed metrics into a scalar objective.
- `constraints.timeout`: per-trial timeout in seconds.
- `constraints.max_trials`: default trial count when CLI does not override it.
- `safety.max_consecutive_failures`: stop the study after too many consecutive failures.
- `safety.allow_commands`: executable allowlist.

## Built-In Adapters

### `subprocess`

Use `subprocess` when the target project can already be launched from a command line.

```yaml
adapter:
  type: subprocess
  command_template:
    - python
    - train.py
    - --lr
    - "{lr}"
    - --output-dir
    - "{trial_dir}"
```

Supported placeholders include sampled parameters such as `{lr}` plus built-ins such as `{trial_dir}`, `{trial_id}`, and `{output_root}`.

### `pytorch_yaml`

Use `pytorch_yaml` when the external project reads a YAML config file and AutoResearch should generate one resolved config per trial.

```yaml
adapter:
  type: pytorch_yaml
  train_entry: train.py
  base_config_path: configs/base.yaml
  config_arg_name: --config
  output_dir_key: OUTPUT_DIR
  param_key_map:
    lr: SOLVER.BASE_LR
    weight_decay: SOLVER.WEIGHT_DECAY
```

The adapter loads the base YAML, applies sampled overrides through dot paths, injects the trial output directory, writes a per-trial config, and launches the trainer.

### `pytorch_argparse`

Use `pytorch_argparse` when the external training script exposes hyperparameters as CLI flags.

```yaml
adapter:
  type: pytorch_argparse
  train_entry: train.py
  output_dir_arg: --output-dir
  fixed_args:
    - --device
    - cuda
  param_arg_map:
    lr: --learning-rate
    batch_size: --batch-size
```

The adapter builds `python train_entry`, appends fixed arguments, maps sampled parameters to CLI flags, and injects the trial output directory.

## Search Space Specification

Supported parameter types:

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

- `float` supports `low`, `high`, and optional `log`.
- `int` supports `low`, `high`, and optional `step`.
- `categorical` supports numeric, string, and boolean values.
- `bool` is sampled as `False` or `True`.

## Metrics and Scoring

Built-in metric collection works best when the external project writes one of:

- `metrics.json`
- `result.json`
- `summary.json`
- `train_stdout.log`

Recommended JSON shape:

```json
{
  "mAP": 76.3,
  "rank1": 84.5,
  "loss": 0.72
}
```

Score configuration:

```yaml
score:
  primary_metric: mAP
  secondary_metrics:
    rank1: 0.2
    mINP: 0.1
  penalties:
    loss: 0.5
  invalid_score: -1000000000
```

Score formula:

```text
primary_metric + weighted_secondary_metrics - weighted_penalties
```

Metric normalization supports aliases such as `mAP`, `map`, `Rank-1`, `rank1`, `top1`, `loss`, and `final_loss`. Percentage-like metrics are normalized onto a 0-100 scale.

## Safety Model

AutoResearch currently enforces:

- `shell=True` is forbidden.
- Default executable allowlist is `python` and `python3`.
- Dangerous commands such as `rm`, `rm -rf`, `shutdown`, `reboot`, `mkfs`, and `dd` are blocked.
- `trial_dir` must stay under `output_root`.
- NaN and Inf metrics are rejected.
- Duplicate sampled configs are rejected inside one study run.
- Studies can stop early after too many consecutive failures.

Example:

```yaml
safety:
  max_consecutive_failures: 5
  allow_commands:
    - python
    - python3
```

## Development and Tests

Run the RTS tests:

```bash
pytest tests/test_rts.py
```

Run requirement generation tests:

```bash
pytest tests/test_requirement_generator.py
```

Run all tests:

```bash
pytest
```

## Current Limitations

- RTS currently starts from manual input; automatic idea or paper readers are planned but not implemented.
- `requirement.md` generation is deterministic and template-like; it does not call an LLM.
- Implementation planning and project generation are future stages.
- Task card generation from RTS is not implemented yet.
- The training framework assumes local subprocess-style execution. It is not yet a cluster scheduler.
- Built-in metric parsers cover common JSON files and simple stdout log patterns.
- If your project cannot be started via CLI and cannot emit parseable metrics, you must implement a custom adapter.

## More Documentation

- Adapter protocol: `docs/adapter_protocol.md`
- Requirement template: `auto_research/templates_docs/requirement_template.md`
- Dummy training script: `examples/dummy_train.py`
- End-to-end task card: `examples/task_cards/dummy_hpo.yaml`
