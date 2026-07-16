---
name: benchmark
description: Run a QA benchmark and score it — main runs each QA itself, spawns judge to score. Triggers: run benchmark, run eval, 跑 benchmark, 评估, benchmark 评测, QA 测评.
---

# benchmark — benchmark 执行与评分

执行 QA benchmark 并评分。main 自己跑每条 QA，spawn `judge`（本系统唯一 spawn 的子 agent）做独立质量门评分。

## 流程

1. **加载 benchmark 规格** — 读 `benchmarks/<name>/qa.jsonl`。每条含 `question`、`gold_answer`/`must_contain`/`rubric`/`pass_threshold`（可选）。
2. **执行 QA** — main 按正常任务路由处理每条 QA（按需用 predicate skill），收集候选答案（最终 reply 文本）。
3. **spawn `judge` 评分** — judge 按 gold_answer/must_contain/rubric/pass_threshold 评估，输出 VERDICT、SCORE (0.00-1.00)、rationale；FAIL 时给 fix prompt。
4. **处理结论** — PASS 计入 pass_rate；FAIL 可选重试（每 QA 最多 1 次）；NEEDS_HUMAN_REVIEW 标记。
5. **汇总** — `pass_rate` = 通过数/总数，`avg_score` = 分数均值；输出 `bench-report.json`（顶层含 `pass_rate` + `avg_score`），呈现逐条摘要。

## 输入

**命名 benchmark 运行**：benchmark 名称（匹配 `benchmarks/` 下目录）；可选 QA 索引（默认全部）。

**Ad-hoc 评估**：问题文本、候选答案、评估标准（任意组合）。

## 输出

`bench-report.json`:

```json
{
  "benchmark": "{name}",
  "pass_rate": 0.00,
  "avg_score": 0.00,
  "items": [
    {"index": 0, "verdict": "PASS|FAIL|NEEDS_HUMAN_REVIEW", "score": 0.00, "summary": "..."}
  ]
}
```
