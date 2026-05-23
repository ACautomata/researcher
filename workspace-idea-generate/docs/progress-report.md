# Idea Generate Agent：四项任务进展总览

> 2026-05-23 | 对应任务 1-4

---

## 任务 1：Benchmark 构建与自测

**状态：Seed QA 与评测设计已完成，自动化自测待执行**

### 产出

- 5 条手工 Seed QA，覆盖 paper-only、paper+code、failed experiment、weak evidence、constraint-heavy 五类场景：`benchmarks/seed-qa.md`
- Benchmark 构建规则与 LLM 扩充规则：`benchmarks/benchmark-spec.md`
- 自测报告模板：`benchmarks/self-test-report-template.md`
- 现有 idea card 字段级校验脚本：`skills/idea-generate/scripts/validate_idea_cards.py`
- 6 维评判体系：evidence grounding / constraint following / idea card completeness / testability / risk honesty / output usability

### 自测结果

- 尚未执行 clean-session 全量自测。
- 当前已完成 benchmark seed、benchmark 设计和报告格式，后续需要把 seed QA 扩充为完整 benchmark 后逐条测试。
- `validate_idea_cards.py` 已覆盖 idea card 必填字段、证据链、指标、最小实验等基础质量检查，但尚未覆盖 agent 端到端回答质量。

### 待完成

- 将 5 条 seed QA 扩充到 20-30 条完整 benchmark。
- 执行 clean-session 自测并生成最终 `self-test-report.md`。
- 视需要补充自动化 runner，将 agent 输出、rubric 评分和报告生成串起来。

**交付物**：`benchmarks/seed-qa.md`、`benchmarks/benchmark-spec.md`、`benchmarks/self-test-report-template.md`

---

## 任务 2：Agent 设计范式选择

**状态：已完成**

### 结论

**Checklist 输入约束 + Harness 生成边界**

| 场景 | 范式 | 原因 |
| --- | --- | --- |
| 用户 brief 归一化 | Checklist | 约束研究主题、baseline、数据、代码、算力、指标和风险偏好 |
| idea 生成 | Harness | 允许跨论文综合和迁移，但受证据、实验、指标、风险边界约束 |
| 证据不足场景 | Harness | 允许继续生成低置信 idea，但必须显式标注缺失信息 |

### 核心理由

Idea Generate 的输入需要结构化，否则 idea 容易脱离用户约束；但生成过程本身需要开放综合能力，否则无法发现跨论文 gap、失败实验信号和可迁移机制。因此采用混合范式。

**交付物**：`docs/design-paradigm.md`

---

## 任务 3：全流程输入输出说明

**状态：已完成**

### 6 阶段流水线

```text
用户 brief / paper / wiki / logs
  -> [Stage 1] Brief 归一化
  -> [Stage 2] Paper Context 构建
  -> [Stage 3] Evidence Analysis
  -> [Stage 4] Candidate Idea Draft
  -> [Stage 5] Dedup + Validation
  -> [Stage 6] Markdown Export
```

### 输入输出规范

- 输入: 研究主题、论文文件、wiki 笔记、实验记录、代码约束、数据/算力/指标偏好。
- 中间输出: `paper-context.json`, `paper-context.md`, `paper-analysis.md`, `draft-ideas.json`, `ideas.dedup.json`, `validation.json`。
- 最终输出: `recommended-ideas.md`。
- 异常处理: 缺失字段写 `ASSUMPTION:`, 证据不足标 `low-confidence`, 抽取失败记录 unavailable extraction, 不伪造指标或论文事实。

**交付物**：`docs/io-spec.md`

---

## 任务 4：Skill 拆分

**状态：已完成设计，暂不实际拆分**

### 识别结果

当前只有一个专用 skill：`skills/idea-generate/`。为了避免过早拆分，目前保留单 skill，但识别出 5 个未来可共享模块：

- `brief-schema` — brief 字段、缺失字段处理、假设标注。
- `idea-card-schema` — idea card 字段、字段含义、允许值。
- `evidence-anchor-rules` — paper snippets、wiki、实验日志、代码位置的证据引用规则。
- `quality-gates` — idea 质量检查、自测评价标准、validation 规则。
- `markdown-artifact-rules` — 最终 Markdown artifact 的结构和风格。

### 收益

- 先保持 subagent 高内聚，降低主流程复杂度。
- 后续新增 `idea-evaluate`、`idea-to-experiment`、`idea-to-prd` 时可复用 shared 模块。
- 避免 brief schema、idea card schema 和质量规则在多个文件里漂移。

**交付物**：`docs/skill-split.md`

---

## 整体交付检查

| 任务 | 状态 | 关键产出 |
| --- | --- | --- |
| 1. Benchmark 构建与自测 | Seed 与设计完成，自测待执行 | Seed QA + benchmark spec + self-test template |
| 2. 设计范式选择 | 已完成 | Checklist + Harness 混合范式 |
| 3. 全流程 I/O 说明 | 已完成 | 6 阶段流水线 + artifacts 规范 |
| 4. Skill 拆分 | 已完成设计 | 暂不拆分 + 5 个 shared 边界 |

---

## 当前额外完成项

- 将 `docs/progress-report.md` 纳入 `AGENTS.md` 和 `TOOLS.md`，作为 PR 汇报入口。
- 将任务说明中的四项要求沉淀为 `docs/task-requirements.md`。
- 在 `skills/idea-generate/SKILL.md` 中补充 requirement alignment、benchmark/self-test 规则和更细的 demo workflow。
- 在 `references/brief-template.md` 中细化 brief 字段含义和追问边界。
- 在 `references/output-spec.md` 中补充最终导出前的质量检查项。
