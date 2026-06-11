# paper-pipeline

## 概述 / Overview

End-to-end deep paper analysis and validation. Orchestrates 6 subagents in a strict linear chain from ingestion to quality audit.

**Trigger words**: "完整分析", "full pipeline", "deep review", "S1-S6", "全流程分析", "paper pipeline", "端到端审稿"

## 应用场景 / Scenario

Deep paper analysis and validation. User provides a paper (PDF/URL) and receives a complete chain: wiki entry, experiment extraction, problem critique, validation design, implementation spec, and quality audit.

## Subagent 调用链 / Agent Chain

| # | Agent | Stage | Role |
|---|-------|-------|------|
| 1 | **ingest** | S1 | Paper PDF ingestion, structured wiki page creation |
| 2 | **extract** | S2 | Deep experiment extraction from paper text |
| 3 | **critic** | S3 | Reviewer-perspective problem and claim analysis |
| 4 | **design** | S4 | Validation experiment design for identified problems |
| 5 | **spec** | S5 | Implementation spec and claude-code task prompt generation |
| 6 | **audit** | S6 | Cross-stage quality auditing and consistency check |

## 编排步骤 / Orchestration Steps

### Pre-pipeline

Read wiki index (`workspace/shared/memory-wiki/index.md`). If paper entry exists, pass path to all stages; otherwise ingest (S1) will create it.

### Per-stage spawn pattern

Each stage follows the same pattern: spawn, wait, verify output, proceed.

**S1 — ingest** | Timeout: 900s (15 min)
- `sessions_spawn(agentId: "ingest", task: "将以下论文入库。标题：{title}。PDF路径：{path}。按 Capture→Extract→Create Paper Page→Update Index 流程执行。", mode: "run", runTimeoutSeconds: 900)`
- Output: Wiki page path, raw source path, evidence_level
- Gate: Wiki page >= 100 lines, at least one numeric result

**S2 — extract** | Timeout: 1800s (30 min)
- `sessions_spawn(agentId: "extract", task: "对以下论文执行实验深度提取（S2）。标题：{title}。Wiki路径：{wiki}。输出到 outputs/{slug}/{slug}-experiment.md。", mode: "run", runTimeoutSeconds: 1800)`
- Input: Wiki path from S1, PDF as fallback
- Output: `{slug}-experiment.md`
- Gate: File exists with all 11 sections per extract skill template

**S3 — critic** | Timeout: 1200s (20 min)
- `sessions_spawn(agentId: "critic", task: "对以下论文执行审稿式问题分析（S3）。标题：{title}。Wiki路径：{wiki}。S2产出：{S2 output path}。输出到 outputs/{slug}/{slug}-problem.md。", mode: "run", runTimeoutSeconds: 1200)`
- Input: Wiki path, S2 experiment doc
- Output: `{slug}-problem.md`
- Gate: >= 1 concrete problem with evidence traceability

**S4 — design** | Timeout: 1200s (20 min)
- `sessions_spawn(agentId: "design", task: "对以下论文执行验证实验设计（S4）。标题：{title}。Wiki路径：{wiki}。S3产出：{S3 output path}。输出到 outputs/{slug}/{slug}-validation.md。", mode: "run", runTimeoutSeconds: 1200)`
- Input: Wiki path, S3 problem doc
- Output: `{slug}-validation.md`
- Gate: Each experiment maps to an S3 problem with expected results

**S5 — spec** | Timeout: 600s (10 min)
- `sessions_spawn(agentId: "spec", task: "生成 claude-code 任务提示词（S5）。S3：{S3 path}。S4：{S4 path}。代码仓库：{repo, optional}。输出到 outputs/{slug}/{slug}-codex-prompt.md。", mode: "run", runTimeoutSeconds: 600)`
- Input: S3 + S4 outputs, optional code repo
- Output: `{slug}-codex-prompt.md`
- Gate: File-level specific, no unfilled placeholders

**S6 — audit** | Timeout: 600s (10 min)
- `sessions_spawn(agentId: "audit", task: "执行流水线质量审计（S6）。产出文件：{list all S2-S5 paths}。输出到 outputs/{slug}/{slug}-audit.md。", mode: "run", runTimeoutSeconds: 600)`
- Input: All S2-S5 output paths
- Output: `{slug}-audit.md`
- Gate: Covers all 6 audit dimensions; blocking issues are actionable

### Error Handling

- **Stage fails**: Log failure, inform user with stage + error detail. Offer retry or checkpoint resume.
- **Checkpoint resume**: Record completed stages. Pass completed output paths and resume from failed stage.
- **Quality gate failure**: Re-spawn same agent with output attached + fix instructions. One retry per stage max.

## 输入规范 / Input Specification

| Field | Required | Description |
|-------|----------|-------------|
| Paper title | Yes | Full paper title |
| PDF path or URL | Yes | Absolute path or accessible URL |
| Code repo | No | Local path or remote URL |
| User notes | No | Focus areas, constraints, questions |
| Start stage | No | Default S1; set to "S3" etc. for checkpoint resume |

## 输出规范 / Output Specification

All outputs under `outputs/{slug}/`:

| File | Stage | Content |
|------|-------|---------|
| `{slug}-experiment.md` | S2 | Structured experiment extraction |
| `{slug}-problem.md` | S3 | Prioritized problem and claim analysis |
| `{slug}-validation.md` | S4 | Validation experiment designs |
| `{slug}-codex-prompt.md` | S5 | Ready-to-use claude-code task prompt |
| `{slug}-audit.md` | S6 | Cross-stage quality audit report |

User receives: top 3 problems, priority validation experiments, audit verdict, next steps.

## 示例 / Examples

### Example 1: Full pipeline

User: "帮我完整分析这篇论文 /Users/papers/attention.pdf"

1. Check wiki: no entry. 2. Spawn **ingest** (S1). Wiki page created. 3. Spawn **extract** (S2). `outputs/attention/attention-experiment.md` created. 4. Spawn **critic** (S3). `outputs/attention/attention-problem.md` created. 5. Spawn **design** (S4). `outputs/attention/attention-validation.md` created. 6. Spawn **spec** (S5). `outputs/attention/attention-codex-prompt.md` created. 7. Spawn **audit** (S6). `outputs/attention/attention-audit.md` created. 8. Report summary.

### Example 2: Checkpoint resume

User: "从S3继续分析 attention-is-all-you-need"

1. Verify S2 output at `outputs/attention/attention-experiment.md`. 2. Spawn **critic** (S3) with wiki + S2 output. 3. Continue S4-S6 normally.
