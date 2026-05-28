# Idea Generate Benchmark Spec

## 目标

Benchmark 用于测试 Idea Generate agent 是否能稳定生成证据约束、可比较、可验证的 idea cards。

## Benchmark 题型

- Paper-only: 只有论文摘要或 snippets。
- Paper plus code: 有代码或实现边界。
- Failed experiment driven: 有失败实验或负面结果。
- Weak evidence: 证据不足，需要低置信标注。
- Constraint-heavy: 资源、数据、时间约束很强。
- Cross-paper contradiction: 多篇论文结论冲突，需要识别 tension。
- Transfer-driven: 从相邻任务迁移方法，但需要说明适用条件。

## 每条样例格式

```text
qa_id:
task_type:
input_material:
question:
gold_answer:
rubric:
failure_modes:
```

## LLM 扩充规则

用 `seed-qa.md` 作为 seed 扩充时，必须满足：

- 保持 idea-generate 任务域，不生成 paper-review 或 experiment-execution 题。
- 每条新 QA 至少包含一个明确约束，例如 metric、compute、code boundary、weak evidence。
- gold answer 不要求唯一文本，但必须列出必备要点。
- rubric 必须能判断输出是否违反 hard rules。
- 不得在 gold answer 中引入输入材料没有提供的论文事实。

## 自测流程

1. 为每条 QA 开一个干净 session。
2. 输入 `input_material` 和 `question`。
3. 保存 agent 输出。
4. 对照 `gold_answer` 和 `rubric` 打分。
5. 记录失败原因。
6. 汇总到 `self-test-report-template.md`。

## 评分维度

每条样例按 0-2 分评分：

- Evidence grounding: 是否基于输入证据。
- Constraint following: 是否遵守代码、数据、计算和风险偏好。
- Idea card completeness: 是否包含必填字段。
- Testability: 是否有最小验证实验和指标。
- Risk honesty: 是否写出风险并处理弱证据。
- Output usability: 输出是否便于用户比较、保存和传入后续验证流程。

总分建议：

- 9-10: 通过。
- 7-8: 基本通过，但需要修正小问题。
- 0-6: 不通过，需要调整 prompt、rules 或 validation。

## 自测报告应包含

- benchmark 规模和题型覆盖。
- 每条 QA 的得分、PASS/FAIL 和主要问题。
- 至少一个成功样例和一个失败或边界样例。
- 对失败原因的归类: 证据不足、字段缺失、约束违反、实验不可测、风险标注不足、输出不可用。
- 下一步修正计划。

## 自动化 runner 预留

当前阶段不强制实现 runner, 但后续可补充:

- `run_benchmark.py`: 逐条运行 QA, 保存 agent 输出。
- `judge_outputs.py`: 按 rubric 做 LLM 或规则评判。
- `expand_benchmark.py`: 用 seed QA 扩充 benchmark。
- `report_results.py`: 汇总为 `self-test-report.md`。
