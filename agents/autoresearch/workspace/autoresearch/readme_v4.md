# AutoResearch v4

AutoResearch is an offline-first research automation framework that turns early research ideas into runnable experiments.

The current version connects these stages:

```text
idea text / manual RTS
-> RTS
-> requirement.md
-> implementation_plan.yaml / implementation_plan.md
-> generated_project
-> validation_result.json / validation_report.md
-> task_card.yaml
-> existing training / HPO framework
-> final_report.md
```

The project is intentionally layered. Upstream modules understand and plan a research task; downstream modules reuse the existing AutoResearch adapter-based training and hyperparameter optimization framework.

## What Is Implemented

- Rule-based `idea text` / `.txt` / `.md` to RTS conversion.
- RTS schema, YAML/JSON IO, and validation.
- Deterministic RTS to `requirement.md` generation.
- Deterministic RTS to implementation plan generation.
- Project generation from RTS and implementation plan.
- Runnable PyTorch templates for `general_pytorch` and `rgb_ir_reid`.
- Generated project validation before training handoff.
- Task card generation compatible with the existing AutoResearch task-card format.
- End-to-end workflow from RTS to generated project, validation, task card, and final report.
- Proxy objective / weighted objective policy data model and offline score calculator.
- Existing adapter-based training and Optuna HPO framework.

## Current Limitations

- Paper PDF parsing is not implemented.
- LLM-based idea parsing is not implemented.
- Frontend UI is not implemented; `docs/frontend_io_spec.md` describes the intended pages and IO.
- Project generation currently ships two templates: `general_pytorch` and `rgb_ir_reid`.
- The end-to-end workflow does not start training by default.
- Proxy objective policy is currently propagated into planning and task cards; the existing HPO objective still uses the established score path unless extended later.

## Project Structure

```text
auto_research/
  adapters/                 # existing external training adapters
  core/                     # study, objective, recorder, task card, safety
  evaluators/               # JSON/log metric parsers
  generation/               # project and task-card generation
  objective/                # proxy objective calculation
  planning/                 # idea->RTS, requirement, implementation plan
  readers/                  # idea text/file readers
  rts/                      # Research Task Specification schema, IO, validation
  search_space/             # search-space validation and sampling
  templates/                # generated project templates
  templates_docs/           # document templates
  validation/               # generated project validation
  workflows/                # end-to-end workflow orchestration
docs/
examples/
tests/
```

## Installation

Requirements:

- Python 3.10+
- `optuna`
- `pyyaml`
- `torch` for generated project smoke training

Install locally:

```bash
pip install -e .
```

Optional dependency group:

```bash
pip install -e .[wandb]
```

## Quick Start: Idea to RTS

Convert a natural-language idea into an RTS file:

```bash
python -m auto_research.cli idea-to-rts \
  --idea-text "设计一个用于RGB-IR跨模态行人重识别的双流网络，加入跨模态注意力融合模块和中心约束损失。" \
  --project-name rgb_ir_attention_test \
  --output ./rgb_ir_attention_rts.yaml
```

Validate the generated RTS:

```bash
python -m auto_research.cli validate-rts \
  --rts ./rgb_ir_attention_rts.yaml
```

The first idea reader is heuristic and offline. It recognizes common task hints such as:

- RGB-IR / infrared / visible light / cross-modal ReID -> `rgb_ir_reid`
- ReID / person re-identification -> `person_reid`
- pose / keypoint / heatmap -> `pose_estimation`
- shadow removal -> `shadow_removal`
- diffusion / restoration -> `diffusion_restoration`
- classification -> `image_classification`
- unknown ideas -> `general_pytorch`

## Quick Start: Full Workflow from RTS

Create an example RTS:

```bash
python -m auto_research.cli init-rts \
  --project-name rgb_ir_attention_test \
  --output ./rts_example.yaml
```

Run the end-to-end workflow:

```bash
python -m auto_research.cli run-from-rts \
  --rts ./rts_example.yaml \
  --output-dir ./generated_projects \
  --overwrite
```

This produces:

```text
generated_projects/rgb_ir_attention_test/
  configs/config.yaml
  datasets/
  models/
  losses/
  trainers/
  evaluators/
  scripts/run_train.sh
  train.py
  test.py
  rts.yaml
  requirement.md
  implementation_plan.yaml
  implementation_plan.md
  generation_report.md
  validation_result.json
  validation_report.md
  task_card.yaml
  final_report.md
```

Training is not launched by default. To request training through the existing study API:

```bash
python -m auto_research.cli run-from-rts \
  --rts ./rts_example.yaml \
  --output-dir ./generated_projects \
  --overwrite \
  --enable-training
```

Use HPO only when intended:

```bash
python -m auto_research.cli run-from-rts \
  --rts ./rts_example.yaml \
  --output-dir ./generated_projects \
  --overwrite \
  --enable-training \
  --enable-hpo
```

## Step-by-Step CLI

Generate a requirement document:

```bash
python -m auto_research.cli rts-to-requirement \
  --rts ./rts_example.yaml \
  --output ./requirement.md
```

Generate an implementation plan:

```bash
python -m auto_research.cli rts-to-plan \
  --rts ./rts_example.yaml \
  --output-yaml ./implementation_plan.yaml \
  --output-md ./implementation_plan.md
```

Generate a runnable project:

```bash
python -m auto_research.cli generate-project \
  --rts ./rts_example.yaml \
  --plan ./implementation_plan.yaml \
  --output-dir ./generated_projects \
  --overwrite
```

Validate the generated project:

```bash
python -m auto_research.cli validate-project \
  --project-dir ./generated_projects/rgb_ir_attention_test
```

Generate a task card:

```bash
python -m auto_research.cli generate-task-card \
  --project-dir ./generated_projects/rgb_ir_attention_test \
  --plan ./generated_projects/rgb_ir_attention_test/implementation_plan.yaml \
  --output ./generated_projects/rgb_ir_attention_test/task_card.yaml
```

Run the generated project manually for one dummy step:

```bash
cd generated_projects/rgb_ir_attention_test
python train.py --config configs/config.yaml --max-steps 1
```

Expected outputs:

```text
outputs/metrics.json
outputs/checkpoint.pt
outputs/train.log
```

## RTS

RTS means Research Task Specification. It is the central intermediate representation between a research idea and an executable experiment.

Important sections:

- `meta`: project name, source type, source path, description.
- `task`: task type, research problem, learning paradigm.
- `goal`: primary metric, optimization direction, secondary metrics.
- `objective_policy`: optional proxy objective / weighted objective / constraints.
- `input` and `output`: modalities, format, shape, output contract.
- `baseline`: selected template.
- `model`: backbone, components, heads.
- `losses`: loss names, weights, params.
- `training`: optimizer, scheduler, batch size, epochs, learning rate.
- `search_space`: hyperparameter search configuration.
- `validation`: required generated-project checks.
- `adapter`: intended training adapter.

Example objective policy:

```yaml
objective_policy:
  type: weighted_sum
  primary_metric: mAP
  direction: maximize
  metrics:
    mAP: 0.6
    Rank-1: 0.3
    mINP: 0.1
  constraints:
    max_training_time_hours: 12
    max_gpu_memory_gb: 24
    min_metrics:
      Rank-1: 0.7
```

## Requirement Document

`requirement.md` is generated from RTS and is meant for engineering review. It is not a paper summary and not final code. It guides later project generation and validation.

It contains stable sections such as:

- Project overview
- Research problem and goal
- Baseline template requirement
- Model requirements
- Loss requirements
- Dataset requirements
- Training requirements
- Evaluation metrics
- Hyperparameter search space
- Validation criteria
- Interface with existing AutoResearch training modules

## Implementation Plan

`implementation_plan.yaml` is machine-readable. `implementation_plan.md` is human-readable.

It includes:

- selected baseline template
- files to create
- files to modify
- model components
- losses
- config requirements
- search space
- validation checks
- adapter requirements
- task-card requirements
- manual review items
- warnings

## Project Generation

`ProjectGenerator` creates a runnable PyTorch project from RTS and the implementation plan.

Currently supported templates:

- `general_pytorch`
- `rgb_ir_reid`

Generated projects support:

- `python train.py --config configs/config.yaml`
- `python train.py --config configs/config.yaml --max-steps 1`
- `python train.py --config configs/config.yaml --dry-run`
- `python test.py --config configs/config.yaml --mode dummy-forward`

## Project Validation

`ProjectValidator` runs a pre-training safety gate.

Checks include:

- required files exist
- config exists
- Python compile
- import check
- config load / dry run
- dummy forward
- one-batch train
- checkpoint exists
- metrics JSON exists
- metrics JSON valid

Validation outputs:

```text
validation_result.json
validation_report.md
```

## Task Card Generation

`TaskCardGenerator` converts a validated generated project and implementation plan into a task card compatible with the existing `auto_research.core.task_card` parser.

The generated task card includes:

- `task_name`
- `adapter`
- `search_space`
- `score`
- `objective`
- `objective_policy`
- `evaluator`
- `run`
- `constraints`
- `safety`

By default, task-card generation requires a passing `validation_result.json`.

## Existing Training / HPO Framework

The existing training system remains adapter-based:

- `subprocess`
- `pytorch_yaml`
- `pytorch_argparse`

Main entry:

```bash
python -m auto_research.core.study \
  --task-card examples/task_cards/dummy_hpo.yaml \
  --n-trials 10
```

The end-to-end workflow can call this existing path, but only when `--enable-training` is provided.

## Proxy Objective / Multi-Metric Policy

`auto_research.objective.ProxyObjectiveCalculator` provides a minimal offline implementation for:

- single metric objective
- weighted sum objective
- metric constraints
- resource constraints such as training time or GPU memory

Example:

```python
from auto_research.objective import ProxyObjectiveCalculator

result = ProxyObjectiveCalculator().compute(
    {"mAP": 0.8, "Rank-1": 0.7, "mINP": 0.5},
    {
        "type": "weighted_sum",
        "direction": "maximize",
        "metrics": {"mAP": 0.6, "Rank-1": 0.3, "mINP": 0.1},
    },
)
```

## Frontend Design Reference

Frontend input/output requirements are documented in:

```text
docs/frontend_io_spec.md
```

Suggested pages:

1. Input Page
2. RTS Editor Page
3. Requirement Preview Page
4. Implementation Plan Page
5. Project Generation Page
6. Validation Page
7. Task Card Page
8. Training Dashboard
9. Final Report Page

## Tests

Run all tests:

```bash
pytest
```

Recent full test status:

```text
126 passed
```

Targeted tests:

```bash
pytest tests/test_idea_to_rts.py
pytest tests/test_proxy_objective.py
pytest tests/test_rts_to_experiment_workflow.py
pytest tests/test_task_card_generator.py
pytest tests/test_project_validator.py
```

## Recommended Human Review Points

- After RTS validation.
- After `requirement.md` generation.
- After implementation plan generation.
- Before overwriting a generated project.
- When validation fails.
- Before generating or submitting a task card.
- Before launching training or HPO.

## Development Roadmap

Planned next steps:

- LLM-backed idea to RTS conversion.
- Paper PDF to RTS extraction.
- More generated project templates.
- Frontend UI implementation.
- Training dashboard.
- Native proxy-objective integration into the existing HPO objective path.
- Richer validation and repair workflows.
