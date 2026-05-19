# AutoResearch

AutoResearch 是一个面向科研实验自动化的框架，目标是把早期的科研想法逐步连接到可运行、可调参、可记录的实验流程。

当前项目已经覆盖两层能力：

- 上游规划层：用 RTS（Research Task Specification）表达 idea、paper 或人工输入的研究任务，并自动生成稳定的 `requirement.md`。
- 下游执行层：通过 task card 和 adapter 接入外部训练项目，执行训练、解析指标、记录结果，并进行自动超参优化。

AutoResearch 不内置具体模型训练代码，也不会重写你的训练项目。它通过统一协议协调外部训练脚本。

## 总体流程

```text
idea / paper / manual input
-> RTS（Research Task Specification）
-> requirement.md
-> implementation_plan
-> generated project
-> task_card.yaml / adapter config
-> existing auto-training module
-> metrics, records, HPO results
```

当前仓库已经实现：

- RTS schema、读写和基础校验。
- RTS 到 `requirement.md` 的确定性生成。
- 基于 adapter 的自动训练和自动调参。
- 指标解析、评分、实验记录和安全检查。

尚未实现：

- 自动论文阅读器或 idea reader。
- implementation plan 自动生成。
- generated project 自动生成。
- 从 RTS 自动生成 task card。

## 项目结构

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

核心职责：

- `auto_research.rts`：Research Task Specification 协议，包括 schema、YAML/JSON 读写和校验。
- `auto_research.planning`：生成确定性的规划文档，例如 `requirement.md`。
- `auto_research.adapters`：把采样参数转换为外部训练项目可执行的形式。
- `auto_research.search_space`：校验和采样 task card 中定义的搜索空间。
- `auto_research.evaluators`：解析 JSON 和日志中的指标。
- `auto_research.core.task_card`：加载、校验 YAML task card，并创建 adapter。
- `auto_research.core.objective`：执行一个完整的 Optuna trial。
- `auto_research.core.study`：命令行启动 Optuna study。
- `auto_research.core.recorder`：写入 `results.tsv` 和 `results.jsonl`。
- `auto_research.core.safety`：执行命令白名单、路径检查、重复配置检查、NaN/Inf 检查和连续失败停止策略。

## 安装

环境要求：

- Python 3.10+
- `optuna`
- `pyyaml`

本地安装：

```bash
pip install -e .
```

安装可选依赖：

```bash
pip install -e .[wandb]
```

## 快速开始：RTS 到需求文档

生成一个 RGB-IR 跨模态行人重识别示例 RTS：

```bash
python -m auto_research.cli init-rts \
  --project-name rgb_ir_attention_test \
  --output ./rts_example.yaml
```

校验 RTS：

```bash
python -m auto_research.cli validate-rts \
  --rts ./rts_example.yaml
```

生成 `requirement.md`：

```bash
python -m auto_research.cli rts-to-requirement \
  --rts ./rts_example.yaml \
  --output ./requirement.md
```

如果 RTS 校验失败，默认不会生成文档，并会打印错误信息。如果仍希望生成：

```bash
python -m auto_research.cli rts-to-requirement \
  --rts ./rts_example.yaml \
  --output ./requirement.md \
  --allow-invalid
```

使用 `--allow-invalid` 时，生成的文档开头会包含 Validation Warning。

## RTS 包含什么

RTS 是科研理解和工程执行之间的中间表示。它足够具体，可以指导后续项目生成；同时又不绑定任何单一训练仓库。

主要字段包括：

- `meta`：项目名、来源类型、来源路径、创建时间和描述。
- `task`：任务类型、研究问题、学习范式。
- `goal`：主指标、优化方向、次级指标。
- `input` 和 `output`：输入模态、数据格式、输入形状、输出类型和维度。
- `baseline`：基线模板或 fallback 基线。
- `model`：backbone、components、heads。
- `losses`：loss 名称、权重和参数。
- `training`：optimizer、scheduler、batch size、epochs、learning rate 等训练配置。
- `datasets`：数据集名称、路径、划分和备注。
- `search_space`：后续可映射到 `auto_research/search_space` 的超参搜索空间。
- `ablation`：消融实验设计。
- `implementation`：后续 generated project 需要包含的文件和模块。
- `validation`：import、dummy forward、backward、one-batch train、config load、checkpoint save/load 等检查项。
- `adapter`：计划使用的 adapter，例如 `pytorch_yaml`、`pytorch_argparse` 或 `subprocess`。

## 需求文档 requirement.md

`requirement.md` 由 RTS 自动生成。它不是论文摘要，也不是最终代码，而是后续 ImplementationPlanner、ProjectGenerator、TaskCardGenerator 的工程依据。

生成文档固定包含 18 个章节：

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

标准结构模板位于：`auto_research/templates_docs/requirement_template.md`。

## 快速开始：自动训练和自动调参

仓库提供了一个假的训练脚本：`examples/dummy_train.py`。它不需要 GPU，也不会训练真实模型，只会模拟训练、写出 `metrics.json`，并在 stdout 中打印可解析指标。

运行 dummy HPO 示例：

```bash
python -m auto_research.core.study \
  --task-card examples/task_cards/dummy_hpo.yaml \
  --n-trials 10
```

常见输出：

- `outputs/dummy_hpo/trial_000001/metrics.json`
- `outputs/dummy_hpo/trial_000001/train_stdout.log`
- `outputs/dummy_hpo/trial_000001/train_stderr.log`
- `outputs/dummy_hpo/trial_000001/trial_record.json`
- `outputs/dummy_hpo/results.tsv`
- `outputs/dummy_hpo/results.jsonl`

常用 study 参数：

- `--study-name`：覆盖 Optuna study 名称。
- `--storage`：传入 storage URL 或本地 SQLite 路径，例如 `runs/study.db`。
- `--timeout`：设置整个 study 的超时时间。
- `--direction`：`maximize` 或 `minimize`。
- `--output-root`：覆盖 task card 中的输出根目录。
- `--dry-run`：只打印命令，不真正执行。
- `--seed`：设置 Optuna sampler 随机种子。

## Task Card

Task card 描述 AutoResearch 如何启动外部训练项目、搜索哪些参数，以及如何给每个 trial 评分。

最小示例：

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

主要字段：

- `task_name`：任务名，也会作为输出目录名。
- `adapter`：描述如何启动外部训练项目。
- `search_space`：Optuna 参数采样定义。
- `score`：描述如何把解析到的指标转换为优化目标。
- `constraints.timeout`：单个 trial 的超时时间，单位是秒。
- `constraints.max_trials`：CLI 未覆盖时的默认 trial 数量。
- `safety.max_consecutive_failures`：连续失败过多时提前停止 study。
- `safety.allow_commands`：可执行命令白名单。

## 内置 Adapter

### `subprocess`

当目标项目已经可以通过普通命令行启动时，使用 `subprocess`。

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

模板中可以使用采样参数，例如 `{lr}`，也可以使用内置变量 `{trial_dir}`、`{trial_id}`、`{output_root}`。

### `pytorch_yaml`

当外部项目通过 YAML 配置文件控制训练，并希望 AutoResearch 为每个 trial 生成 resolved config 时，使用 `pytorch_yaml`。

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

该 adapter 会读取基础 YAML，按 dot path 覆盖采样参数，注入 trial 输出目录，写出每个 trial 的配置文件，并启动训练脚本。

### `pytorch_argparse`

当训练脚本已经通过 CLI 参数暴露超参时，使用 `pytorch_argparse`。

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

该 adapter 会构造 `python train_entry`，追加固定参数，把采样参数映射到 CLI flag，并注入 trial 输出目录。

## 搜索空间规范

支持的参数类型：

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

规则：

- `float` 支持 `low`、`high` 和可选的 `log`。
- `int` 支持 `low`、`high` 和可选的 `step`。
- `categorical` 支持数字、字符串和布尔值。
- `bool` 会在 `False` 和 `True` 之间采样。

## 指标和评分

内置指标收集优先读取：

- `metrics.json`
- `result.json`
- `summary.json`
- `train_stdout.log`

推荐 JSON 格式：

```json
{
  "mAP": 76.3,
  "rank1": 84.5,
  "loss": 0.72
}
```

评分配置示例：

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

评分公式：

```text
primary_metric + weighted_secondary_metrics - weighted_penalties
```

指标归一化支持常见别名，例如 `mAP`、`map`、`Rank-1`、`rank1`、`top1`、`loss`、`final_loss`。百分制指标会统一到 0-100 标度。

## 安全模型

AutoResearch 当前会执行以下安全策略：

- 禁止 `shell=True`。
- 默认只允许执行 `python` 和 `python3`。
- 阻止 `rm`、`rm -rf`、`shutdown`、`reboot`、`mkfs`、`dd` 等危险命令。
- `trial_dir` 必须位于 `output_root` 下。
- 拒绝 NaN 和 Inf 指标。
- 同一次 study 中拒绝重复采样配置。
- 连续失败次数过多时提前停止 study。

示例：

```yaml
safety:
  max_consecutive_failures: 5
  allow_commands:
    - python
    - python3
```

## 开发和测试

运行 RTS 测试：

```bash
pytest tests/test_rts.py
```

运行需求文档生成测试：

```bash
pytest tests/test_requirement_generator.py
```

运行全部测试：

```bash
pytest
```

## 当前限制

- RTS 当前主要来自人工输入；自动 idea reader 和 paper reader 还未实现。
- `requirement.md` 生成是确定性的模板化过程，不调用大模型。
- implementation plan 生成和 project generation 是后续阶段。
- 还没有实现从 RTS 自动生成 task card。
- 当前训练框架假设本地 subprocess 风格执行，还不是集群调度系统。
- 内置指标解析器覆盖常见 JSON 文件和简单 stdout 日志模式。
- 如果目标项目不能通过 CLI 启动，也不能输出可解析指标，则需要实现自定义 adapter。

## 更多文档

- Adapter 协议：`docs/adapter_protocol.md`
- Requirement 模板：`auto_research/templates_docs/requirement_template.md`
- Dummy 训练脚本：`examples/dummy_train.py`
- 端到端 task card：`examples/task_cards/dummy_hpo.yaml`
