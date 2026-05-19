# AutoResearch v4 中文说明

AutoResearch 是一个面向科研实验自动化的离线优先框架，目标是把早期科研想法逐步转换成可运行、可验证、可调参、可记录的实验项目。

当前版本已经打通如下流程：

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

项目采用分层设计。上游模块负责理解、规范化和规划科研任务；下游模块复用已有 AutoResearch adapter、task card、study、objective、recorder 等自动训练和自动调参能力。

## 当前已经实现的能力

- 基于规则的 `idea text` / `.txt` / `.md` 到 RTS 转换。
- RTS schema、YAML/JSON 读写和基础校验。
- RTS 到 `requirement.md` 的确定性生成。
- RTS 到 `implementation_plan.yaml` / `implementation_plan.md` 的确定性生成。
- 基于 RTS 和 implementation plan 的 generated project 生成。
- `general_pytorch` 和 `rgb_ir_reid` 两个可运行 PyTorch 模板。
- generated project 的训练前自动验证。
- 与现有 AutoResearch task card 格式兼容的 `task_card.yaml` 生成。
- 从 RTS 到 generated project、validation、task card、final report 的端到端 workflow。
- proxy objective / weighted objective / constraints 的数据结构和离线计算器。
- 原有 adapter-based training 和 Optuna HPO 框架。

## 当前限制

- 尚未实现论文 PDF 解析。
- 尚未实现 LLM 版本的 idea 解析。
- 尚未实现前端页面；前端输入输出规范见 `docs/frontend_io_spec.md`。
- ProjectGenerator 当前只内置两个模板：`general_pytorch` 和 `rgb_ir_reid`。
- 端到端 workflow 默认不启动训练。
- proxy objective policy 当前会写入 requirement、implementation plan 和 task card；现有 HPO objective 仍保持原有评分路径，后续可继续接入。

## 项目结构

```text
auto_research/
  adapters/                 # 已有外部训练项目适配器
  core/                     # study、objective、recorder、task_card、safety
  evaluators/               # JSON/log 指标解析
  generation/               # 项目生成和 task card 生成
  objective/                # proxy objective 计算
  planning/                 # idea->RTS、requirement、implementation plan
  readers/                  # idea 文本和文件读取
  rts/                      # Research Task Specification schema、IO、validation
  search_space/             # 搜索空间校验和采样
  templates/                # generated project 模板
  templates_docs/           # 文档模板
  validation/               # generated project 验证
  workflows/                # 端到端 workflow 编排
docs/
examples/
tests/
```

## 安装

环境要求：

- Python 3.10+
- `optuna`
- `pyyaml`
- `torch`，用于 generated project 的 dummy training 验证

本地安装：

```bash
pip install -e .
```

安装可选依赖：

```bash
pip install -e .[wandb]
```

## 快速开始：idea 转 RTS

将自然语言科研想法转换成 RTS：

```bash
python -m auto_research.cli idea-to-rts \
  --idea-text "设计一个用于RGB-IR跨模态行人重识别的双流网络，加入跨模态注意力融合模块和中心约束损失。" \
  --project-name rgb_ir_attention_test \
  --output ./rgb_ir_attention_rts.yaml
```

校验生成的 RTS：

```bash
python -m auto_research.cli validate-rts \
  --rts ./rgb_ir_attention_rts.yaml
```

第一版 idea reader 是离线规则版，可以识别常见任务提示：

- RGB-IR / 红外 / 可见光 / 跨模态行人重识别 -> `rgb_ir_reid`
- ReID / 行人重识别 -> `person_reid`
- pose / keypoint / heatmap / 姿态估计 -> `pose_estimation`
- shadow removal / 阴影去除 -> `shadow_removal`
- diffusion / restoration / 修复 -> `diffusion_restoration`
- classification / 分类 -> `image_classification`
- 无法识别 -> `general_pytorch`

## 快速开始：从 RTS 运行完整 workflow

生成一个示例 RTS：

```bash
python -m auto_research.cli init-rts \
  --project-name rgb_ir_attention_test \
  --output ./rts_example.yaml
```

运行端到端 workflow：

```bash
python -m auto_research.cli run-from-rts \
  --rts ./rts_example.yaml \
  --output-dir ./generated_projects \
  --overwrite
```

该命令会生成：

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

默认不会启动训练。如果需要通过已有 study API 启动训练：

```bash
python -m auto_research.cli run-from-rts \
  --rts ./rts_example.yaml \
  --output-dir ./generated_projects \
  --overwrite \
  --enable-training
```

只有明确需要自动调参时才建议开启 HPO：

```bash
python -m auto_research.cli run-from-rts \
  --rts ./rts_example.yaml \
  --output-dir ./generated_projects \
  --overwrite \
  --enable-training \
  --enable-hpo
```

## 分步骤命令

生成需求文档：

```bash
python -m auto_research.cli rts-to-requirement \
  --rts ./rts_example.yaml \
  --output ./requirement.md
```

生成实现计划：

```bash
python -m auto_research.cli rts-to-plan \
  --rts ./rts_example.yaml \
  --output-yaml ./implementation_plan.yaml \
  --output-md ./implementation_plan.md
```

生成可运行项目：

```bash
python -m auto_research.cli generate-project \
  --rts ./rts_example.yaml \
  --plan ./implementation_plan.yaml \
  --output-dir ./generated_projects \
  --overwrite
```

验证 generated project：

```bash
python -m auto_research.cli validate-project \
  --project-dir ./generated_projects/rgb_ir_attention_test
```

生成 task card：

```bash
python -m auto_research.cli generate-task-card \
  --project-dir ./generated_projects/rgb_ir_attention_test \
  --plan ./generated_projects/rgb_ir_attention_test/implementation_plan.yaml \
  --output ./generated_projects/rgb_ir_attention_test/task_card.yaml
```

手动运行 generated project 的一步 dummy training：

```bash
cd generated_projects/rgb_ir_attention_test
python train.py --config configs/config.yaml --max-steps 1
```

预期输出：

```text
outputs/metrics.json
outputs/checkpoint.pt
outputs/train.log
```

## RTS

RTS 是 Research Task Specification，是科研想法和可执行实验之间的核心中间表示。

重要字段：

- `meta`：项目名、来源类型、来源路径、描述。
- `task`：任务类型、研究问题、学习范式。
- `goal`：主指标、优化方向、次级指标。
- `objective_policy`：可选的代理目标、多指标加权目标和约束。
- `input` 和 `output`：输入模态、格式、形状和输出契约。
- `baseline`：选定模板。
- `model`：backbone、components、heads。
- `losses`：loss 名称、权重、参数。
- `training`：optimizer、scheduler、batch size、epochs、learning rate。
- `search_space`：超参搜索空间。
- `validation`：generated project 需要通过的检查项。
- `adapter`：计划使用的训练 adapter。

objective policy 示例：

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

`requirement.md` 由 RTS 自动生成，用于工程需求审核。它不是论文摘要，也不是最终代码，而是后续项目生成和验证的工程依据。

主要内容包括：

- 项目概览
- 研究问题和目标
- baseline template 要求
- 模型要求
- loss 要求
- 数据集要求
- 训练要求
- 评估指标
- 超参搜索空间
- 验证标准
- 与已有 AutoResearch 训练模块的接口

## Implementation Plan

`implementation_plan.yaml` 是机器可读计划，`implementation_plan.md` 是人类可读计划。

内容包括：

- 选定 baseline template
- 需要创建的文件
- 需要修改的文件
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

`ProjectGenerator` 根据 RTS 和 implementation plan 生成可运行 PyTorch 项目。

当前支持模板：

- `general_pytorch`
- `rgb_ir_reid`

生成项目支持：

```bash
python train.py --config configs/config.yaml
python train.py --config configs/config.yaml --max-steps 1
python train.py --config configs/config.yaml --dry-run
python test.py --config configs/config.yaml --mode dummy-forward
```

## Project Validation

`ProjectValidator` 是训练前安全门。

验证项包括：

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

验证输出：

```text
validation_result.json
validation_report.md
```

## Task Card Generation

`TaskCardGenerator` 会把已验证的 generated project 和 implementation plan 转换成现有 AutoResearch 训练框架可识别的 task card。

生成的 task card 包括：

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

默认要求 `validation_result.json` 存在且 `passed=true`，否则不会生成 task card。

## 已有训练和 HPO 框架

已有训练系统仍然是 adapter-based：

- `subprocess`
- `pytorch_yaml`
- `pytorch_argparse`

主入口：

```bash
python -m auto_research.core.study \
  --task-card examples/task_cards/dummy_hpo.yaml \
  --n-trials 10
```

端到端 workflow 可以调用这条已有路径，但只有在传入 `--enable-training` 时才会启动。

## Proxy Objective / 多指标策略

`auto_research.objective.ProxyObjectiveCalculator` 提供了最小可用的离线实现：

- 单指标 objective
- 多指标 weighted sum objective
- 指标约束
- 训练时间、显存等资源约束

示例：

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

## 前端设计参考

前端页面输入输出规范见：

```text
docs/frontend_io_spec.md
```

建议页面：

1. Input Page
2. RTS Editor Page
3. Requirement Preview Page
4. Implementation Plan Page
5. Project Generation Page
6. Validation Page
7. Task Card Page
8. Training Dashboard
9. Final Report Page

## 测试

运行全部测试：

```bash
pytest
```

最近一次全量测试状态：

```text
126 passed
```

常用定向测试：

```bash
pytest tests/test_idea_to_rts.py
pytest tests/test_proxy_objective.py
pytest tests/test_rts_to_experiment_workflow.py
pytest tests/test_task_card_generator.py
pytest tests/test_project_validator.py
```

## 建议人工确认点

- RTS 校验后。
- `requirement.md` 生成后。
- implementation plan 生成后。
- 覆盖 generated project 前。
- validation 失败时。
- 生成或提交 task card 前。
- 启动训练或 HPO 前。

## 后续路线

建议后续继续推进：

- LLM 版本 idea to RTS。
- paper PDF 到 RTS。
- 更多 generated project 模板。
- 前端 UI。
- Training Dashboard。
- proxy objective 与现有 HPO objective 的更深集成。
- 更完整的 validation repair workflow。
