# Idea Generate Seed QA

这些 seed QA 用于构建和扩充 idea-generate benchmark。每条都包含输入材料、提问、标准答案和评价要点。

## QA-001: Paper-only idea generation

### 输入材料

- 研究主题：dataset distillation for long-tailed image classification。
- 论文 A 摘要：方法通过 trajectory matching 生成小规模 synthetic set，但在长尾类别上 minority class accuracy 明显低。
- 论文 B 摘要：class-balanced sampling 能提升 long-tailed recognition，但会增加 majority class overfitting risk。
- 约束：只能做小规模验证，优先 CIFAR-LT，指标为 balanced accuracy 和 minority class accuracy。

### 提问

请基于上述材料生成 3 个 research idea cards。

### 标准答案

输出应包含 3 个 idea cards，每个 idea 都必须：

- 针对 long-tailed dataset distillation。
- 引用论文 A 或 B 中的 limitation 或 insight。
- 包含 minimum experiment，例如在 CIFAR-LT 上比较 baseline synthetic set 与 class-balanced variant。
- 指定 expected metric，例如 balanced accuracy 或 minority class accuracy。
- 写出 risk，例如 majority class 性能下降或 synthetic set 过拟合。

### 评价要点

- 不接受泛泛写“使用 transformer”。
- 不接受没有 metric 的 idea。
- 不接受声称方法已经有效，除非输入材料提供证据。

## QA-002: Paper plus code constraint

### 输入材料

- 研究主题：OOD detection for vision-language models。
- 论文材料：一篇方法使用 maximum concept matching 改善 OOD detection，但在细粒度近邻类别上 FPR95 仍高。
- 代码约束：已有 CLIP inference pipeline，只能改 scoring function，不能重新训练 backbone。
- 指标：AUROC、FPR95。

### 提问

请生成 2-4 个低成本 idea，并说明最小验证实验。

### 标准答案

输出 idea 应优先围绕 scoring function，而不是重新训练大模型。每个 idea 应包含：

- 机制：例如概念集重加权、近邻类别 margin、prompt ensemble score calibration。
- 最小实验：在已有 CLIP pipeline 上替换 score，比较 AUROC/FPR95。
- 风险：例如 prompt 敏感、类别描述质量影响、近邻 OOD 不稳定。

### 评价要点

- 必须遵守“不能重新训练 backbone”。
- 必须给出能在现有 pipeline 内完成的 implementation_scope。

## QA-003: Failed experiment driven

### 输入材料

- 研究主题：reasoning distillation for small LLMs。
- 已失败实验：直接蒸馏 long-CoT 数据后，小模型准确率提升有限，输出长度显著增加。
- 论文 insight：多教师数据有助于覆盖不同 reasoning paths，但低质量 chain 会引入噪声。
- 约束：只能做数据筛选和训练数据配比，不能改模型结构。

### 提问

请基于失败现象生成 research ideas。

### 标准答案

至少包含：

- 一个针对 chain quality filtering 的 idea。
- 一个针对 short/long reasoning mix ratio 的 idea。
- 每个 idea 都要说明 expected metric，例如 accuracy、average output length、reasoning token budget。
- 风险中必须提到过度过滤导致多样性下降或短链损失复杂题能力。

### 评价要点

- 必须使用 failed experiment 作为 evidence anchor。
- 不允许提出改模型结构的方案。

## QA-004: Weak evidence handling

### 输入材料

- 研究主题：spectrum machine learning。
- 只有一段论文摘要，提到模型在一个 spectroscopy dataset 上优于 baseline，但没有给出具体数字。
- 用户要求：给出可能的 idea，但不要夸大证据。

### 提问

请生成 idea cards，并标注证据强度。

### 标准答案

输出可以生成少量 idea，但必须：

- 标为 `low-confidence` 或明确证据不足。
- 在 open questions 中写明缺少 dataset size、baseline name、metric number。
- 不得写“显著优于 SOTA”作为确定事实。
- minimum_experiment 应优先补齐 baseline 复现或指标确认。

### 评价要点

- 重点检查是否诚实处理弱证据。

## QA-005: Constraint-heavy idea generation

### 输入材料

- 研究主题：federated learning personalization。
- 可用数据：只有 non-IID split 的小规模 benchmark。
- 可用计算：单卡，最多 8 小时。
- 代码：已有 FedAvg baseline。
- 用户偏好：低风险、容易验证。

### 提问

请生成适合当前资源约束的 idea。

### 标准答案

idea 应低成本并贴近 FedAvg baseline，例如：

- client clustering 后的局部 adapter。
- personalization head fine-tuning。
- communication-efficient prototype regularization。

每个 idea 必须写：

- 为什么适合单卡 8 小时。
- 最小实验配置。
- 指标，例如 average accuracy、worst-client accuracy、communication rounds。
- 风险，例如过拟合小 benchmark 或 client cluster 不稳定。

### 评价要点

- 不接受大规模预训练或复杂多阶段方案。
- 必须体现 compute constraint。

