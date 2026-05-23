# Idea Generate Task Requirements

本文档根据 `任务说明(1).docx` 将 Idea Generate agent 的开发任务细化为可提交、可测试、可 PR 审查的需求。

## 任务范围

Idea Generate agent 负责把论文、wiki 笔记、实验记录、代码约束和用户研究目标转化为结构化 research idea cards。它不负责真正执行实验、不负责写完整 PRD、不负责替用户选择唯一最终方案。

## 四项交付

### 1. Benchmark 构建与自测

交付物：

- `benchmarks/seed-qa.md`: 人工构建的 seed QA。
- `benchmarks/benchmark-spec.md`: 完整 benchmark 构建规则和扩充规则。
- `benchmarks/self-test-report-template.md`: 自测报告模板。
- `docs/progress-report.md`: 四项任务进展总览, 用于 PR 汇报。

基本要求：

- 每条 QA 必须包含输入材料、问题、标准答案、评价要点。
- LLM 扩充 QA 时必须基于人工 seed，不允许脱离 idea-generate 任务域。
- 自测必须在干净 session 中逐条喂给 agent，并记录输出是否满足标准答案。
- PR 中必须说明覆盖的题型、通过情况、失败样例和后续修正计划。

### 2. Agent 设计范式选择

交付物：

- `docs/design-paradigm.md`

结论：

- Idea Generate 采用混合范式。
- 用户侧使用 checklist 风格的 brief，约束输入信息和研究边界。
- 生成侧使用 harness 风格的边界规则，允许 agent 在边界内综合论文证据、失败记录和代码约束生成 idea。

### 3. 全流程输入输出说明

交付物：

- `docs/io-spec.md`

必须说明：

- 用户可输入的文件类型、目录结构和最小必需字段。
- 中间阶段产生的 artifacts。
- 最终用户拿到的 Markdown 和 JSON 文件。
- 每个阶段的失败条件和可降级行为。

### 4. Skill 拆分

交付物：

- `docs/skill-split.md`

当前结论：

- 当前只有一个主 skill: `idea-generate`。
- 暂不立刻拆成多个专用 skills，避免过早拆分。
- 先识别可复用模块边界，为后续拆分到 `skills/shared/` 做准备。

## PR 验收标准

- `docs/progress-report.md` 能清楚说明四项任务状态、产出、待完成项。
- `workspace-idea-generate/AGENTS.md` 指向这些需求文档。
- `skills/idea-generate/SKILL.md` 的 workflow 与需求文档一致。
- benchmark seed 至少覆盖 paper-only、paper+code、paper+failed-log、weak-evidence、constraint-heavy 五类场景。
- 所有 idea card 都能被 `validate_idea_cards.py` 检查。
- 运行产物仍进入 `idea-runs/`，不提交到配置仓库。
