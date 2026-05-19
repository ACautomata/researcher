# NCL 论文案例验证报告

## 1. 验证目标

本报告使用一篇真实论文案例来验证 AutoResearch 当前开放模块的有效性。

论文案例为：

- 论文：Nested Collaborative Learning for Long-Tailed Visual Recognition, CVPR 2022
- 本地 PDF：`C:/Users/Administrator/Desktop/wenxian/[2022 CVPR]Nested Collaborative Learning for Long-Tailed Visual Recognition.pdf`
- CVPR OpenAccess 页面：https://openaccess.thecvf.com/content/CVPR2022/html/Li_Nested_Collaborative_Learning_for_Long-Tailed_Visual_Recognition_CVPR_2022_paper.html
- 官方 PDF：https://openaccess.thecvf.com/content/CVPR2022/papers/Li_Nested_Collaborative_Learning_for_Long-Tailed_Visual_Recognition_CVPR_2022_paper.pdf


```text
论文实验想法 / 论文案例
-> RTS
-> requirement.md
-> implementation_plan
-> task_card
-> HPO trial 执行
-> 指标记录
-> 最优实验选择
-> 定量和定性评价
```

由于完整 NCL 训练需要 PyTorch、CUDA 环境、长尾数据集准备以及较长训练时间，本次采用 **NCL proxy 实验**。该实验保留论文实验方法的结构和关键超参数，但用轻量确定性脚本模拟训练结果，用于验证 AutoResearch 的流程有效性。

## 2. 采用的论文实验案例

本次选择 NCL 论文中的代表性长尾视觉识别实验设定：

```text
CIFAR100-LT, imbalance factor = 100
```

该案例包含以下实验元素：

| 项目 | 内容 |
| --- | --- |
| 任务类型 | 长尾视觉识别 / 图像分类 |
| 数据集设定 | CIFAR100-LT |
| 不平衡因子 | 100 |
| 方法结构 | NCL 风格多专家协同学习 |
| 关键机制 | Nested Individual Learning、Nested Balanced Online Distillation、Hard Category Mining、自监督/对比增强 |
| 主要指标 | accuracy、many_acc、medium_acc、few_acc、loss |
| 搜索目标 | 优化整体准确率，同时关注 few-shot 和 medium-shot 表现 |

## 3. 新增案例文件

本次验证在最新工作区中新增了 NCL 案例文件：

- `examples/ncl_case/ncl_cifar100_lt_rts.yaml`
- `examples/ncl_case/ncl_proxy_task_card.yaml`
- `examples/ncl_case/ncl_proxy_train.py`

主要输出文件：

- `outputs/ncl_case_validation/planning/rts_validation.json`
- `outputs/ncl_case_validation/planning/requirement.md`
- `outputs/ncl_case_validation/planning/implementation_plan.yaml`
- `outputs/ncl_case_validation/planning/implementation_plan.md`
- `outputs/ncl_case_validation/planning/idea_to_rts_probe.json`
- `outputs/ncl_case_validation/ncl_cifar100_lt_case/results.tsv`
- `outputs/ncl_case_validation/ncl_cifar100_lt_case/results.jsonl`
- `outputs/ncl_case_validation/ncl_cifar100_lt_case/quantitative_summary.json`

## 4. 验证模块和结果概览

| 模块 | 输入 | 输出 | 验证结果 |
| --- | --- | --- | --- |
| RTS schema 和校验 | NCL 论文案例 RTS | `rts_validation.json` | 通过 |
| Requirement 生成 | 合法 RTS | `requirement.md` | 成功生成 |
| Implementation Planner | 合法 RTS | `implementation_plan.yaml/md` | 成功生成 |
| Idea-to-RTS heuristic | NCL 自然语言 idea | 初版 RTS | 部分有效 |
| Task card 执行 | NCL proxy task card | trial 目录和记录 | 通过 |
| Subprocess adapter | 渲染后的训练命令 | `metrics.json` 和日志 | 通过 |
| Study / Objective / Recorder | 12 次 HPO trial | 汇总表和最优 trial | 通过 |
| Proxy objective policy | 指标和加权目标策略 | score 与约束状态 | 通过 |

## 5. 定量验证过程

### 5.1 RTS 校验结果

手工构造的 NCL 论文案例 RTS 通过校验：

```json
{
  "passed": true,
  "errors": [],
  "warnings": []
}
```

说明当前 RTS schema 能够表达该论文案例所需的核心信息，包括：

- 任务类型；
- 数据集和长尾设定；
- 模型结构；
- 损失函数；
- 训练配置；
- 评估指标；
- 搜索空间；
- 消融实验；
- adapter 接口。

### 5.2 Idea-to-RTS 探针结果

为了评估当前 `IdeaToRTSConverter` 是否能自动理解 NCL 论文想法，本次额外输入了一段自然语言 idea：

```text
Use Nested Collaborative Learning for long-tailed visual recognition on CIFAR100-LT with imbalance factor 100...
```

然后检查它是否捕获了 6 个 NCL 关键概念：

| 检查项 | 是否捕获 |
| --- | --- |
| image classification 任务 | 否 |
| accuracy 主指标 | 否 |
| contrastive loss | 是 |
| multi-expert 结构 | 否 |
| hard category mining | 否 |
| CIFAR100-LT 数据集 | 否 |

定量结果：

```text
captured_count = 1
total_checked = 6
捕获率 = 16.7%
```

评价：当前 idea-to-RTS heuristic 对通用词汇有一定识别能力，例如 `contrastive`，但对 NCL 这种具体论文方法的专有结构、数据集和实验范式识别较弱。实际使用时，论文级案例仍需要人工 RTS 或更强的 paper-aware / LLM-based RTS 生成模块。

### 5.3 HPO 执行命令

本次使用 AutoResearch 的 study 模块执行 12 次 proxy HPO：

```powershell
.\.venv\Scripts\python.exe -m auto_research.core.study `
  --task-card examples\ncl_case\ncl_proxy_task_card.yaml `
  --study-name ncl-case-validation `
  --storage outputs\ncl_case_validation\study.db `
  --output-root outputs\ncl_case_validation `
  --n-trials 12 `
  --direction maximize `
  --seed 42
```

### 5.4 HPO 定量结果

12 次 trial 全部完成：

| 指标 | 数值 |
| --- | ---: |
| trial_count | 12 |
| completed | 12 |
| success_rate | 1.0 |
| constraint_pass_rate | 1.0 |
| score_min | 57.673892 |
| score_max | 63.4889585 |
| score_mean | 60.0385372 |
| score_stdev | 1.9808217 |
| best_minus_worst | 5.8150665 |

说明：

- 所有 trial 都成功执行，没有运行失败、超时或无效记录。
- 所有 trial 都满足 proxy objective 中设置的最低指标约束。
- 最优与最差 score 相差约 `5.82`，说明不同超参数组合会产生可区分的优化效果。
- AutoResearch 能够稳定完成采样、执行、解析、评分和记录。

### 5.5 最优实验

最佳 trial：

```text
trial_000008
```

最佳 score：

```text
63.4889585
```

最佳超参数：

```json
{
  "num_experts": 4,
  "base_lr": 0.09412647117513108,
  "weight_decay": 0.000771281194715635,
  "batch_size": 64,
  "diversity_factor": 0.7705958297783961,
  "hcm_ratio": 1.1607850486168974,
  "contrastive_ratio": 0.4
}
```

最佳指标：

```json
{
  "accuracy": 53.8013,
  "many_acc": 59.5813,
  "medium_acc": 56.1199,
  "few_acc": 51.2088,
  "loss": 1.599313,
  "imbalance_factor": 100.0
}
```

从 proxy 目标函数看，该结果具有合理性：

- `base_lr` 接近 NCL/CIFAR 训练常用的 `0.1` 区域；
- `batch_size` 为 `64`，与 NCL 配置中的常用 batch size 一致；
- `contrastive_ratio = 0.4`，代表适度启用对比增强；
- `diversity_factor` 和 `hcm_ratio` 均处于有效区间；
- `num_experts = 4`，表示多专家协同学习结构被激活。

## 6. 定性评价

### 6.1 有效的部分

第一，RTS 能表达真实论文实验。

NCL 案例 RTS 能表达 CIFAR100-LT、imbalance factor、长尾分类、NCL 多专家结构、Hard Category Mining、对比增强、搜索空间和目标指标。这说明 RTS schema 具备承载真实论文实验设计的能力。

第二，需求文档和实现计划生成有效。

从 RTS 自动生成了 `requirement.md`、`implementation_plan.yaml` 和 `implementation_plan.md`。这些文件可以作为后续代码生成、人工实现、实验配置和审查的中间产物。

第三，实验执行链路完整。

AutoResearch 成功完成：

```text
task_card
-> 参数采样
-> 命令渲染
-> subprocess 训练入口执行
-> metrics.json 解析
-> score 计算
-> results.tsv / results.jsonl 记录
-> best trial 选择
```

第四，结果可审计。

每次实验都有独立目录，包含：

- `metrics.json`
- `train_stdout.log`
- `train_stderr.log`
- `trial_record.json`

任务级别还有：

- `results.tsv`
- `results.jsonl`
- `study.db`

这说明实验过程和结果具备可追踪性。

### 6.2 不足和风险

第一，idea-to-RTS 对具体论文方法理解不足。

自然语言 idea 输入后，当前 heuristic 只捕获了 `contrastive` 这一类通用概念，没有识别 NCL、CIFAR100-LT、long-tailed visual recognition、multi-expert、hard category mining 等关键信息。

这说明该模块目前更适合基础任务识别，不适合作为论文级自动理解的唯一入口。

第二，最新版本的完整测试存在 PyTorch 环境阻塞。

最新版本完整测试结果为：

```text
126 collected
118 passed
8 failed
```

8 个失败集中在生成 PyTorch 项目验证链路，根因是当前 Python 3.14 虚拟环境未安装 `torch`：

```text
ModuleNotFoundError: No module named 'torch'
```

因此，真实 PyTorch 生成项目验证需要额外准备兼容的 PyTorch 环境。



## 7. 综合评价

| 能力 | 评价 | 原因 |
| --- | --- | --- |
| RTS 表达能力 | 较好 | 能表达 NCL 论文案例的任务、指标、搜索空间和实验结构 |
| RTS 校验 | 较好 | NCL paper-case RTS 通过校验 |
| Requirement 生成 | 较好 | 能生成完整需求文档 |
| Implementation Plan 生成 | 可用 | 能生成计划，但缺少 NCL 专用模板，只能回退到 general_pytorch |
| Idea-to-RTS | 较弱 | NCL 专项概念捕获率仅 1/6 |
| Task card / Adapter 执行 | 较好 | 12 次实验全部成功 |
| HPO / Recorder | 较好 | 能记录全部 trial，并选出 best trial |
| 真实 PyTorch 项目验证 | 当前受阻 | 缺少 torch 环境 |
| 论文精度复现 | 未验证 | 本次是 proxy 实验，不是真实 NCL 训练 |

## 8. 结论

基于 NCL 论文的 CIFAR100-LT imbalance factor 100 实验设定，AutoResearch 当前开放模块在 **论文案例结构化、需求生成、实现计划生成、实验配置、HPO 执行、结果记录和最优实验选择** 方面是有效的。

定量上，12 次 proxy HPO 全部完成，成功率为 `100%`，约束通过率为 `100%`，最优 score 达到 `63.4889585`，最优与最差实验之间存在 `5.8150665` 的可区分差距。

定性上，系统能够形成一条可审计的研究自动化链路：

```text
论文案例
-> RTS
-> requirement
-> implementation plan
-> task card
-> HPO trial
-> results
```

但当前仍有两个关键改进点：

1. 增强 idea-to-RTS / paper-to-RTS 对具体论文方法的理解能力；
2. 为 generated project validation 提供兼容 PyTorch 的环境，或提供 torch-free smoke validation 模式。

因此，本次验证结论是：

**AutoResearch 当前开放模块可以有效支持真实论文案例驱动的实验流程，但距离自动完成真实论文复现仍需要增强论文理解、专用模板和深度学习运行环境。**
