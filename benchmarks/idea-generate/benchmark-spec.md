# Idea Generate Benchmark Spec

## 目标

Benchmark 用于测试 Idea Generate agent 是否能稳定生成证据约束、可比较、可验证的 idea cards。评估框架融合了三个方法论来源的核心理念：

- **good-question**（Rimagination）：好问题的 7 个检查——重要性、具体性、竞争性解释、可证伪性、可行性、负结果价值、证据追溯
- **ARIS**（Auto-claude-code-research-in-sleep）：跨模型对抗审、research wiki 持久记忆、AI 科研失败模式目录
- **academic-research-skills**（Imbad0202）：结构化质量门禁、完整性验证、Devil''s Advocate 让步阈值

## Benchmark 题型（9 种）

| task_type | 测试能力 | 关键约束 |
|---|---|---|
| `paper-only` | 纯论文摘要 → idea 生成 | 无代码，依赖文本证据，必须引用论文 limitation |
| `paper-plus-code` | 有代码边界 → 低成本 idea | 不能改 backbone / 重训练大模型，必须给出实现范围 |
| `failed-experiment-driven` | 从失败实验诊断 → 改进方向 | 必须引用失败实验具体数据，不能提出改模型结构的方案 |
| `weak-evidence` | 弱证据 → 诚实标注 | 必须标注 low-confidence，不能声称优于 SOTA，优先 baseline 复现 |
| `constraint-heavy` | 极强资源约束 → 可行方案 | 必须有时间/算力估算，体现 compute constraint |
| `cross-paper-contradiction` | 识别论文间矛盾 → 解决 idea | 必须明确指出矛盾根因，提出 controlled re-evaluation |
| `transfer-driven` | 跨域迁移评估 → 适配方案 | 必须真正评估可行性而非简单套用，逐组件分析可复用性 |
| `assumption-challenge` | 挑战文献默认假设 → 范式级 idea | 必须识别并挑战领域默认假设，不能只做 gap-spotting；引用 Alvesson & Sandberg (2011) problematization 方法论 |
| `lineage-contextualized` | 论文谱系中定位 idea → 贡献评估 | 给定研究方向的论文谱系（related work + follow-up），agent 必须说明其 idea 在谱系中的精确位置和真实增量 |

## 每条样例格式 (qa.jsonl)

每行一个 JSON，符合 `benchmarks/_common/qa_schema.json`：

```json
{
  "qa_id": "QA-001",
  "agent": "main",
  "target_agent": "idea-generate",
  "skill": "idea-generate",
  "task_type": "paper-only",
  "input_material": "...",
  "question": "...",
  "gold_answer": {"must_contain": ["..."], "fields": ["..."]},
  "rubric": "...",
  "rubric_dimensions": [
    "evidence_grounding",
    "constraint_following",
    "idea_completeness",
    "testability",
    "falsifiability",
    "importance",
    "rival_awareness",
    "contribution_positioning",
    "risk_honesty"
  ],
  "pass_threshold": 0.5,
  "judge": "rules",
  "weight": 1.0
}
```

## 评分维度（9 维）

| # | 维度 | 含义 | 方法论来源 |
|---|------|------|-----------|
| 1 | `evidence_grounding` | 是否基于输入证据，不编造论文事实；证据 vs 推断明确标注 | good-question #7 (grounded) |
| 2 | `constraint_following` | 是否遵守代码、数据、计算和风险偏好约束 | good-question #5 (feasible) |
| 3 | `idea_completeness` | 是否包含必填字段：机制、最小实验、指标、风险 | good-question #2 (specific) |
| 4 | `testability` | 是否有可执行的最小验证实验和可量化指标 | good-question #5, Platt 强推断 |
| 5 | `falsifiability` | 是否说明什么结果会削弱或推翻该 idea | good-question #4 (can fail) |
| 6 | `importance` | 是否说清楚谁在乎、什么会改变；不只是 novelty | good-question #1 (it matters), Heilmeier Catechism |
| 7 | `rival_awareness` | 是否承认竞争性解释，将 idea 与之区分 | good-question #3 (has rivals), Platt 强推断 |
| 8 | `contribution_positioning` | 是否正确定位 idea 在研究谱系中的位置：向后追溯 related work、向前扫描 follow-up work、诚实评估真实增量（范式级 / 方法改进 / 微调变体） | 本项目原创维度，综合 ARIS research wiki 记忆 + academic-research-skills 完整性验证 |
| 9 | `risk_honesty` | 是否诚实写出风险；对弱证据标注低置信度；负结果价值 | good-question #6 (teaches when negative), ARIS 失败模式 |

### `contribution_positioning` 维度的四个检查项

| 子项 | 含义 | 打分信号 |
|------|------|---------|
| `backward_trace` | idea 是否正确引用了它声称基于的 related work？有没有漏掉关键前置工作？ | 正确引用输入中的论文谱系节点 |
| `forward_scan` | 是否意识到该方向已有的 follow-up work？有没有人已经做了类似的事？ | 不声称"首次"除非输入材料证明如此 |
| `delta_honesty` | 在已有工作面前，诚实评估 idea 的真实增量 | 显式标注：范式级 / 方法改进 / 微调变体 |
| `positioning` | idea 是否精确锚定在已有工作的缺口上 | 不是笼统的"combine A and B"，而是"A 解决 X 但留下 Y，B 解决部分 Y，本 idea 解决剩余 Y" |

### 各维度在各题型中的权重（9×9 矩阵）

●●● = 核心维度 · ●● = 加重权重 · ● = 基础权重

| task_type | evidence | constraint | completeness | testability | falsifiability | importance | rival | contribution_positioning | risk |
|-----------|----------|------------|-------------|-------------|----------------|------------|-------|--------------------------|------|
| paper-only | ●● | ● | ●● | ●● | ●● | ●● | ● | ● | ●● |
| paper-plus-code | ● | ●●● | ●● | ●● | ●● | ● | ● | ● | ● |
| failed-experiment | ●●● | ●● | ●● | ●● | ●● | ●● | ● | ● | ●● |
| weak-evidence | ●●● | ● | ● | ● | ● | ● | ● | ● | ●●● |
| constraint-heavy | ● | ●●● | ●● | ●●● | ● | ● | ● | ● | ●● |
| cross-paper-contradiction | ●● | ● | ●● | ●● | ●● | ●●● | ●●● | ●● | ● |
| transfer-driven | ●● | ●● | ●● | ●● | ●● | ●● | ●● | ●● | ● |
| assumption-challenge | ●● | ● | ●● | ● | ●●● | ●●● | ●●● | ●● | ●● |
| lineage-contextualized | ●● | ● | ●● | ●● | ●● | ●●● | ●● | ●●● | ●● |

## Judge 模式

| 模式 | 适用场景 | 评分方式 | 使用的 QA |
|---|---|---|---|
| `rules` | 可量化检查（关键词覆盖、约束遵守） | `judge_with_rules`：对 `gold_answer.must_contain` 做关键词命中率 | QA-001/002/005/006/008/009/010/012 |
| `agent` | 需语义质量判断（弱证据处理、失败诊断深度、域迁移可行性、假设挑战质量、谱系定位质量） | `judge_with_agent`：通过专用 `reviewer` agent 按 9 维 rubric 综合评分 | QA-003/004/007/011 |

`agent` 模式题目 rubric 含详细加减分规则，weight 为 1.5。

## LLM 扩充规则

从现有 QA 扩充时，必须满足：

- 保持 idea-generate 任务域，不生成 paper-review 或 experiment-execution 题。
- 每条新 QA 至少包含一个明确约束，例如 metric、compute、code boundary、weak evidence。
- gold answer 不要求唯一文本，但必须列出必备要点（`must_contain` 关键词 >=8）。
- rubric 必须覆盖 9 维中的关键维度；对 `lineage-contextualized` 题型，falsifiability、importance、contribution_positioning 为必测维度。
- 不得在 gold answer 中引入输入材料没有提供的论文事实。
- `lineage-contextualized` 题型的 input_material 必须包含完整论文谱系（>=3 篇论文，标注年份和关系）。

## 评分标准

- **rules judge**：score = `must_contain` 关键词命中数 / 总数，pass_threshold = 0.5
- **agent judge**：reviewer 按 9 维 rubric 综合给出 score (0-1)，pass_threshold = 0.5
- **总分**：weighted average（agent judge 题 weight 1.5，rules 题 weight 1.0）

## Good Question Card 参考模板（增强版）

以下是 idea-generate 产出的 idea card 应覆盖的字段（对齐 good-question 的 10 字段 + contribution_positioning）：

```markdown
**暂定题目：** ...
**核心研究问题：** ...
**为什么值得做：** ...                    ← importance 维度
**研究谱系定位：** ...                    ← contribution_positioning
  - 基于的前置工作：...（related work）
  - 已有 follow-up：...（哪些人已经做了什么）
  - 本 idea 的真实增量：范式级/方法改进/微调变体
  - 为什么已有的没覆盖这个缺口：...
**它挑战了什么默认假设：** ...             ← rival_awareness 维度
**竞争性解释：** ...                       ← rival_awareness 维度
**关键判别证据或实验：** ...               ← testability 维度
**什么结果会推翻它：** ...                 ← falsifiability 维度
**两周内可做的 pilot：** ...               ← constraint_following 维度
**最强评审质疑：** ...                     ← risk_honesty 维度
**下一步动作：** ...
```

## CI 自动化

CI 通过 `benchmarks/_common/` 下的共享组件自动运行：

| 组件 | 作用 |
|---|---|
| `_common/env_setup.sh` | 统一环境准备（Docker + health check） |
| `_common/run_bench.py` | 通用 Driver：加载 qa.jsonl → 逐条调用 main agent → 评分 → 写 bench-report.json |
| `_common/judge.py` | `judge_with_rules` + `judge_with_agent` 评分函数 |
| `_common/report_pr.py` | 汇总各 benchmark 报告并发布 PR comment |

每个 benchmark 只需提供：
- `env.sh` — fixture staging
- `metrics.py` — 6 行 shim 调用 `run_bench.main()`
- `qa.jsonl` — 测试用例
- `benchmark-spec.md` — 本文档

## 自测流程

1. 为每条 QA 开一个干净 session。
2. 输入 `input_material` 和 `question`。
3. 保存 agent 输出。
4. 对照 `gold_answer` 和 `rubric` 打分。
5. 记录失败原因及归类（证据不足 / 字段缺失 / 约束违反 / 实验不可测 / 无可证伪条件 / 未说明重要性 / 无竞争性解释 / 谱系定位错误 / 风险标注不足）。
6. 汇总结果，确认 9 种题型覆盖率和 pass rate。

## 方法论来源

| 来源 | 本项目吸收了什么 |
|------|----------------|
| good-question (Rimagination, 2026) | 7 检查框架：重要性、具体性、竞争性解释、可证伪性、可行性、负结果价值、证据追溯；Good Question Card 模板 |
| ARIS (wanshuiyin, 2026) | 跨模型对抗审、research wiki 持久记忆、AI 科研失败模式目录（实现 bug、幻觉结果、捷径依赖、frame-lock、引用幻觉） |
| academic-research-skills (Imbad0202, 2026) | 结构化质量门禁、0-100 rubric 评分、Devil''s Advocate 让步阈值、完整性验证 gate |
| Alon (2009), Fischbach (2024) | 选问题是一种可训练能力，要比较问题、识别陷阱，不要方法先行 |
| Platt (1964) | 强推断：好问题应产生竞争性假设和判别实验 |
| Alvesson & Sandberg (2011) | 不要只找 gap，要挑战文献背后的默认假设（problematization） |
| Heilmeier Catechism (DARPA) | proposal 必须说清楚目标、受众、风险、成功标准和失败标准 |
| contribution_positioning（本项目原创） | 将 idea 锚定在研究谱系中：向后追溯 related work、向前扫描 follow-up、诚实评估真实增量 |
