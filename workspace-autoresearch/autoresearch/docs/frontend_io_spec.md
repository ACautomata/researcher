# AutoResearch Frontend Input/Output Specification

本文档用于指导 AutoResearch 前端页面设计，重点说明每个流程步骤的页面名称、用户输入、系统输出、输出文件、示例数据、人工确认点和当前实现状态。

## 1. Overall Pipeline

```text
idea / paper / manual input
-> RTS
-> requirement.md
-> implementation_plan
-> generated_project
-> validation
-> task_card
-> auto training / HPO
-> final_report
```

当前后端已经支持从 `manual rts.yaml` 到 `final_report.md` 的端到端链路。默认 workflow 不启动训练；只有用户显式开启训练时，才会尝试调用已有 AutoResearch training / HPO 模块。

## 2. Step 0: Idea / Paper / Manual RTS Input

建议页面名称：`Input Page`

用户输入：

- `idea text`：用户直接输入研究想法。
- `paper pdf`：用户上传论文 PDF。
- `manual rts.yaml`：用户上传或编辑标准 RTS 文件。

当前状态：

- `manual RTS supported`
- `idea/paper parser not implemented yet`

idea 示例：

```text
我想做一个 RGB-IR 跨模态行人重识别方法。
输入包括 RGB 图像和红外图像，输出是行人 embedding。
希望使用 mAP 作为主指标，并最大化 mAP。
模型中希望加入 cross-modal attention。
loss 使用 cross entropy、triplet loss 和 center constraint。
```

系统输出：

- 如果用户上传 RTS：进入 RTS 加载和校验。
- 如果用户输入 idea/paper：当前版本只能提示“暂未实现自动解析”，后续可扩展为自动生成 RTS 草稿。

是否需要人工确认：需要。用户需要确认输入类型和任务目标。

## 3. Step 1: RTS Generation / Loading

建议页面名称：`RTS Editor Page`

用户输入：

- `manual rts.yaml`
- 或由 `init-rts` 示例生成的 RTS。

系统输出：

- `rts.yaml`
- 页面可展示为表单和 YAML 双视图。

页面展示字段：

- `meta.project_name`
- `meta.source_type`
- `task.type`
- `task.research_problem`
- `goal.primary_metric`
- `goal.optimization_direction`
- `input.modalities`
- `output.type`
- `baseline.template`
- `model.components`
- `losses`
- `training`
- `search_space`
- `adapter`

示例 YAML：

```yaml
meta:
  project_name: rgb_ir_attention_test
  source_type: manual
  source_path: null
  description: RGB-IR cross-modal person re-identification attention baseline.

task:
  type: rgb_ir_reid
  research_problem: Learn discriminative cross-modal embeddings for RGB and IR person images.
  learning_paradigm: supervised

goal:
  primary_metric: mAP
  optimization_direction: maximize
  secondary_metrics:
    - rank1
    - rank5

input:
  modalities:
    - RGB
    - IR
  data_format: paired_image_folders
  input_shape:
    - 3
    - 256
    - 128

output:
  type: embedding
  dimension: 512

baseline:
  template: rgb_ir_reid

losses:
  - name: cross_entropy
    weight: 1.0
    params: {}
  - name: triplet
    weight: 1.0
    params:
      margin: 0.3
  - name: center_constraint
    weight: 0.01
    params: {}

search_space:
  lr:
    type: float
    low: 1.0e-5
    high: 1.0e-3
    log: true
  batch_size:
    type: categorical
    choices: [32, 64]
```

当前状态：Done。后端已实现 `auto_research.rts.schema`、`io`、`validation`，并提供 CLI：

```bash
python -m auto_research.cli init-rts --project-name rgb_ir_attention_test --output ./rts_example.yaml
```

是否需要人工确认：建议需要。RTS 是后续所有步骤的源头。

## 4. Step 2: RTS Validation

建议页面名称：`RTS Editor Page` 或 `RTS Validation Panel`

用户输入：

- `rts.yaml`

系统输出：

- validation dict
- 页面展示 `passed/errors/warnings`

示例 JSON：

```json
{
  "passed": true,
  "errors": [],
  "warnings": []
}
```

失败示例：

```json
{
  "passed": false,
  "errors": [
    "meta.project_name must be a non-empty string.",
    "goal.optimization_direction must be either maximize or minimize."
  ],
  "warnings": []
}
```

页面展示建议：

- 顶部状态：Passed / Failed
- 错误列表：红色
- 警告列表：黄色
- 按字段定位：例如 `goal.optimization_direction`

当前状态：Done。

是否需要人工确认：需要。RTS 校验通过后，建议用户点击“确认并生成需求文档”。

## 5. Step 3: Requirement Document Generation

建议页面名称：`Requirement Preview Page`

用户输入：

- `rts.yaml`

系统输出：

- `requirement.md`

输出文件：

```text
generated_projects/{project_name}/requirement.md
```

文档固定包含 18 个章节：

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

Markdown 片段示例：

```md
# Requirement Document

## 1. Document Role in the Auto-Research Pipeline

This requirement.md is generated from RTS. It is a bridge between research understanding and code generation.
```

页面需求：

- Markdown 预览
- 原文查看
- 下载按钮
- “确认进入 Implementation Plan”按钮

当前状态：Done。模块为 `auto_research.planning.requirement_generator.RequirementGenerator`。

是否需要人工确认：建议需要。需求文档是项目生成前的重要人工审核点。

## 6. Step 4: Implementation Plan Generation

建议页面名称：`Implementation Plan Page`

用户输入：

- `rts.yaml`

系统输出：

- `implementation_plan.yaml`
- `implementation_plan.md`

输出文件：

```text
generated_projects/{project_name}/implementation_plan.yaml
generated_projects/{project_name}/implementation_plan.md
```

示例 YAML 片段：

```yaml
project:
  name: rgb_ir_attention_test
  task_type: rgb_ir_reid
  source_type: manual
  primary_metric: mAP
  optimization_direction: maximize

template:
  selected: rgb_ir_reid
  fallback: general_pytorch
  reason: RTS baseline.template is explicitly provided.
  warnings: []

files_to_create:
  - path: models/modality_attention.py
    purpose: Implement modality_attention.
    module_type: model_component
  - path: losses/center_constraint.py
    purpose: feature compactness constraint
    module_type: loss

validation_checks:
  - import_check
  - dummy_forward
  - loss_backward
  - one_batch_train
  - config_load
  - checkpoint_save_load
```

页面展示重点：

- `template.selected`
- `files_to_create`
- `files_to_modify`
- `model_components`
- `losses`
- `adapter_requirements`
- `validation_checks`
- `manual_review_items`
- `warnings`

当前状态：Done。模块为 `auto_research.planning.implementation_planner.ImplementationPlanner`。

是否需要人工确认：建议需要。用户应确认模板、待创建文件、loss 和 adapter 方案。

## 7. Step 5: Project Generation

建议页面名称：`Project Generation Page`

用户输入：

- `rts.yaml`
- `implementation_plan.yaml`
- `output_dir`
- `overwrite` 开关

系统输出：

- generated project
- `generation_report.md`
- 同步保存 `rts.yaml`、`requirement.md`、`implementation_plan.yaml`、`implementation_plan.md`

文件树示例：

```text
generated_projects/
└── rgb_ir_attention_test/
    ├── configs/
    │   └── config.yaml
    ├── datasets/
    │   ├── __init__.py
    │   └── dummy_dataset.py
    ├── models/
    │   ├── __init__.py
    │   ├── baseline.py
    │   ├── build.py
    │   └── modality_attention.py
    ├── losses/
    │   ├── __init__.py
    │   ├── build.py
    │   └── center_constraint.py
    ├── trainers/
    │   ├── __init__.py
    │   └── trainer.py
    ├── evaluators/
    │   ├── __init__.py
    │   └── evaluator.py
    ├── scripts/
    │   └── run_train.sh
    ├── train.py
    ├── test.py
    ├── README.md
    ├── requirements.txt
    ├── rts.yaml
    ├── requirement.md
    ├── implementation_plan.yaml
    ├── implementation_plan.md
    └── generation_report.md
```

当前状态：Done。第一版模板已支持：

- `general_pytorch`
- `rgb_ir_reid`

生成项目默认 CPU 可运行，支持 dummy data，一步训练后输出：

```text
outputs/metrics.json
outputs/checkpoint.pt
outputs/train.log
```

是否需要人工确认：建议需要。尤其要确认生成文件结构和是否允许覆盖已有项目。

## 8. Step 6: Project Validation

建议页面名称：`Validation Page`

用户输入：

- generated project directory
- 可选 `config_path`
- 可选 `timeout`

系统输出：

- `validation_result.json`
- `validation_report.md`

输出文件：

```text
generated_projects/{project_name}/validation_result.json
generated_projects/{project_name}/validation_report.md
```

示例 JSON：

```json
{
  "passed": true,
  "project_dir": "generated_projects/rgb_ir_attention_test",
  "config_path": "generated_projects/rgb_ir_attention_test/configs/config.yaml",
  "checks": [
    {
      "name": "required_files_exist",
      "passed": true,
      "details": "All required files exist."
    },
    {
      "name": "one_batch_train",
      "passed": true,
      "command": ["python", "train.py", "--config", "configs/config.yaml", "--max-steps", "1"],
      "stdout": "{'loss': 1.38, 'mAP': 0.12, 'Rank-1': 0.18, 'mINP': 0.08}",
      "stderr": "",
      "details": "Command completed successfully."
    }
  ],
  "errors": [],
  "warnings": [],
  "validation_result_path": "generated_projects/rgb_ir_attention_test/validation_result.json",
  "validation_report_path": "generated_projects/rgb_ir_attention_test/validation_report.md"
}
```

页面展示建议：

- Check list
- 每个 check 的 passed / failed 状态
- command
- stdout 摘要
- stderr 摘要
- errors
- warnings

当前检查项：

- `required_files_exist`
- `config_exists`
- `py_compile`
- `import_check`
- `config_load`
- `dummy_forward`
- `one_batch_train`
- `checkpoint_exists`
- `metrics_json_exists`
- `metrics_json_valid`

当前状态：Done。模块为 `auto_research.validation.project_validator.ProjectValidator`。

是否需要人工确认：validation 失败时必须人工确认；通过时建议允许进入 task card 生成。

## 9. Step 7: Task Card Generation

建议页面名称：`Task Card Page`

用户输入：

- generated project directory
- `implementation_plan.yaml`
- `allow_unvalidated` 开关

系统输出：

- `task_card.yaml`

输出文件：

```text
generated_projects/{project_name}/task_card.yaml
```

示例 YAML：

```yaml
task_name: rgb_ir_attention_test

adapter:
  type: pytorch_yaml
  train_entry: /abs/path/to/generated_projects/rgb_ir_attention_test/train.py
  base_config_path: /abs/path/to/generated_projects/rgb_ir_attention_test/configs/config.yaml
  config_arg_name: --config
  output_dir_key: output.dir
  fixed_args: []
  param_key_map:
    lr: training.lr
    batch_size: training.batch_size
    epochs: training.epochs
    weight_decay: training.weight_decay
  output_root: /abs/path/to/generated_projects/rgb_ir_attention_test/autoresearch_outputs
  metrics_filenames:
    - metrics.json

search_space:
  lr:
    type: float
    low: 1.0e-5
    high: 1.0e-3
    log: true
  batch_size:
    type: categorical
    choices: [32, 64]

score:
  primary_metric: mAP
  invalid_score: -1000000000

objective:
  metric: mAP
  direction: maximize

evaluator:
  type: json
  metrics_path: /abs/path/to/generated_projects/rgb_ir_attention_test/outputs/metrics.json

run:
  project_dir: /abs/path/to/generated_projects/rgb_ir_attention_test
  output_dir: /abs/path/to/generated_projects/rgb_ir_attention_test/outputs
```

页面展示重点：

- `adapter`
- `score` / `objective`
- `search_space`
- `evaluator`
- `run.project_dir`
- `run.output_dir`

当前状态：Done。生成前默认要求 `validation_result.json` 存在且 `passed=true`。

是否需要人工确认：需要。提交训练前应确认 task card。

## 10. Step 8: Auto Training / HPO

建议页面名称：`Training Dashboard`

用户输入：

- `task_card.yaml`
- 是否启动训练
- 是否启动 HPO
- `n_trials`
- `timeout`
- `direction`
- `storage`
- `seed`

系统输出：

- logs
- metrics
- best params
- study results
- per-trial outputs

已有训练模块输出示例：

```text
autoresearch_outputs/
└── rgb_ir_attention_test/
    ├── trial_000001/
    │   ├── metrics.json
    │   ├── train_stdout.log
    │   ├── train_stderr.log
    │   ├── trial_config.yaml
    │   └── trial_record.json
    ├── results.tsv
    └── results.jsonl
```

页面展示建议：

- 当前训练状态：pending / running / completed / failed
- Trial 列表
- 当前指标
- 最优指标
- best params
- stdout/stderr 日志预览
- results.tsv / results.jsonl 下载

当前状态：Partially Done。

说明：

- 已有 `auto_research.core.study`、`objective`、`recorder`、`adapters` 能执行 task card。
- 端到端 workflow 默认不启动训练。
- `run-from-rts --enable-training` 已保守接入现有 study API。
- 前端训练仪表盘尚未实现。

是否需要人工确认：需要。训练和 HPO 可能耗时，应由用户显式点击启动。

## 11. Step 9: Final Report

建议页面名称：`Final Report Page`

用户输入：

- 所有中间结果
- workflow 运行状态

系统输出：

- `final_report.md`

输出文件：

```text
generated_projects/{project_name}/final_report.md
```

示例 Markdown：

```md
# Final Report

## 1. Workflow Summary

- success: True
- project_name: rgb_ir_attention_test
- project_dir: generated_projects/rgb_ir_attention_test

## 9. Errors

- None

## 10. Warnings

- None
```

页面展示建议：

- summary
- generated files
- validation result
- task card path
- training submission status
- errors
- warnings
- next steps

当前状态：Done。模块为 `auto_research.workflows.rts_to_experiment_workflow.RtsToExperimentWorkflow`。

是否需要人工确认：建议需要。final report 是整条链路的最终审核页面。

## 12. Implementation Status Table

| Step | Module | Input | Output | Status |
|---|---|---|---|---|
| Step 0: Idea / Paper / Manual Input | planned idea/paper reader, manual upload | idea text / paper pdf / rts.yaml | RTS draft or loaded RTS | Partially Done |
| Step 1: RTS Generation / Loading | `auto_research.rts.io`, `auto_research.rts.schema` | `rts.yaml` or `init-rts` params | `rts.yaml` | Done |
| Step 2: RTS Validation | `auto_research.rts.validation.RTSValidator` | `rts.yaml` | validation dict | Done |
| Step 3: Requirement Document Generation | `RequirementGenerator` | RTS | `requirement.md` | Done |
| Step 4: Implementation Plan Generation | `ImplementationPlanner`, `BaselineSelector` | RTS | `implementation_plan.yaml`, `implementation_plan.md` | Done |
| Step 5: Project Generation | `ProjectGenerator`, `ConfigGenerator`, templates | RTS + plan | generated project | Done |
| Step 6: Project Validation | `ProjectValidator`, `CommandRunner` | generated project | `validation_result.json`, `validation_report.md` | Done |
| Step 7: Task Card Generation | `TaskCardGenerator` | generated project + plan | `task_card.yaml` | Done |
| Step 8: Auto Training / HPO | existing `core.study`, `objective`, `adapters`, `recorder` | `task_card.yaml` | trial logs, metrics, results | Partially Done |
| Step 9: Final Report | `RtsToExperimentWorkflow` | all intermediate results | `final_report.md` | Done |
| Frontend UI | Not implemented | user interactions | web pages | Not Started |
| Idea / Paper Parser | Not implemented | idea text / PDF | RTS draft | Planned |

## 13. Suggested Frontend Pages

1. `Input Page`
   - 选择输入类型：idea、paper、manual RTS。
   - 上传文件或输入文本。

2. `RTS Editor Page`
   - 表单编辑 RTS。
   - YAML 预览。
   - RTS 校验结果。

3. `Requirement Preview Page`
   - Markdown 预览 `requirement.md`。
   - 人工确认按钮。

4. `Implementation Plan Page`
   - 展示模板选择、files_to_create、files_to_modify、losses、adapter、validation checks。
   - 支持查看 YAML 和 Markdown。

5. `Project Generation Page`
   - 展示生成路径。
   - 展示文件树。
   - 展示 `generation_report.md`。

6. `Validation Page`
   - 展示 validation check list。
   - 查看 stdout/stderr 摘要。
   - 展示错误和警告。

7. `Task Card Page`
   - 展示 adapter、search_space、objective、evaluator。
   - 提供“提交训练”按钮。

8. `Training Dashboard`
   - 展示 trial 状态。
   - 展示当前指标、最优指标、best params。
   - 展示日志。

9. `Final Report Page`
   - 展示 workflow summary。
   - 展示 errors、warnings、next steps。

## 14. Human Confirmation Points

建议人工确认点：

1. RTS 校验后
   - 确认 task type、primary metric、optimization direction、modalities、search space 是否正确。

2. `requirement.md` 生成后
   - 确认需求文档是否准确表达研究目标和工程目标。

3. `implementation_plan` 生成后
   - 确认 baseline template、待创建文件、loss、adapter、validation checks。

4. Project generation 前
   - 确认是否允许 overwrite。
   - 确认输出目录。

5. validation 失败时
   - 必须人工确认错误原因。
   - 不建议跳过 validation 直接生成 task card。

6. task_card 提交训练前
   - 确认 adapter 配置。
   - 确认 search space 范围。
   - 确认 objective metric 和 direction。
   - 确认训练是否需要启动 HPO。

7. training / HPO 启动前
   - 确认资源、超时时间、trial 数量、输出目录。

8. final_report 生成后
   - 确认是否进入下一轮修改 RTS、重新生成项目或启动训练。
