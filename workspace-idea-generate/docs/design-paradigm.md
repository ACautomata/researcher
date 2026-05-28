# Idea Generate Design Paradigm

## 结论

Idea Generate 采用混合范式：

- Checklist: 用于用户输入和 brief 归一化。
- Harness: 用于生成阶段的边界约束。

这个选择的原因是：idea 生成既需要结构化输入来控制研究边界，又需要 agent 在证据范围内做跨论文综合、迁移和可行性判断。纯 checklist 会限制生成质量，纯黑箱又容易产生不可控的泛化建议。

## 用户侧 Checklist

用户不一定一次给全，但 agent 必须尝试补齐或标注假设。

必填或强建议字段：

- `research_topic`: 研究主题。
- `target_task`: 目标任务或实验设定。
- `current_baseline`: 当前 baseline 或已有方法。
- `available_data`: 可用数据集、数据规模、标注状态。
- `available_code`: 可用代码仓库、框架、能改动的模块。
- `available_compute`: GPU/CPU、时间预算、实验规模。
- `preferred_metrics`: 优先关注指标。
- `hard_constraints`: 不能违反的约束。
- `known_failures`: 已失败实验或负面现象。
- `desired_risk_level`: 低风险、中风险或高探索性。

## 生成侧 Harness 规则

agent 可以自由组织分析，但必须满足以下边界：

- 只能基于论文 context、wiki、用户材料、实验记录或明确标注的假设生成 idea。
- 每个 idea 必须有机制说明，不接受只有方法名的建议。
- 每个 idea 必须包含 minimum experiment。
- 每个 idea 必须至少命名一个 expected metric。
- 每个 idea 必须写 risk 或 failure mode。
- 证据不足时必须标为 `low-confidence`。
- 不允许把 idea 写成已经被验证成功的结论。
- 不允许默认推荐唯一最终 winner，除非用户要求排序或选择。

## 面向用户的交互方式

当输入不足时，优先继续推进，并在 brief 中显式写出假设。只有以下情况才需要追问：

- 完全没有 research topic。
- 没有任何论文、wiki、实验记录或代码上下文可用。
- 用户要求严格受限的实现方案，但缺少硬约束。

## 输出控制

最终输出应让用户能快速比较不同 idea：

- 证据强度。
- 实现成本。
- 预期收益。
- 最小验证实验。
- 主要风险。
- 推荐理由。

