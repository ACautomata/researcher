# benchmark

## 概述 / Overview

Benchmark execution and evaluation skill. Orchestrates the main agent through running QA benchmarks, collecting candidate answers, and routing them through the judge subagent for quality-gated scoring.

**Trigger words:** "run benchmark", "run eval", "跑 benchmark", "评估", "benchmark 评测", "QA 测评"

## 应用场景 / Scenario

- Run evaluation benchmarks from `benchmarks/` directory
- Score candidate answers against gold answers and rubrics
- Quality-gate subagent outputs before reporting to user
- Ad-hoc evaluation of agent responses against defined criteria

## Subagent 调用链 / Agent Chain

1. **judge** — Independent quality gate. Produces PASS/FAIL/NEEDS_HUMAN_REVIEW verdicts, numeric scores (0-1), and actionable fix prompts. Evaluates against gold_answer, must_contain, rubric, and pass_threshold.

## 编排步骤 / Orchestration Steps

### Step 1: Load benchmark specification

- Read `benchmarks/<name>/qa.jsonl` to load QA items
- Each item has: `question`, `gold_answer` (optional), `must_contain` (optional), `rubric` (optional), `pass_threshold` (optional)
- If running a single QA or ad-hoc evaluation, accept the item directly from user input

### Step 2: Execute QA against main agent (self)

- For each QA item, formulate the question and process it through normal task routing
- Main agent may delegate to subagents (autoresearch, paper-review, idea-generate) as needed
- Collect the candidate answer (final reply text + any artifact paths)
- Record the answer alongside the original QA item for judging

### Step 3: Route to judge for evaluation

```
sessions_spawn(
  agentId: "judge",
  task: """Evaluate the following benchmark candidate answer.

## Benchmark Question
{qa.question}

## Candidate Answer
{candidate answer text}

## Artifact Paths
{file paths; or "none"}

## Evaluation Criteria
- gold_answer: {qa.gold_answer or "not provided"}
- must_contain: {qa.must_contain or "not provided"}
- rubric: {qa.rubric or "not provided"}
- pass_threshold: {qa.pass_threshold or 0.8}

## Output Requirements
Output VERDICT (PASS/FAIL/NEEDS_HUMAN_REVIEW), SCORE (0.00-1.00), and rationale.
If FAIL, provide a Fix prompt for the original agent.""",
  mode: "run",
  runTimeoutSeconds: 300
)
```

### Step 4: Process judge verdict

- **PASS**: Record score, include in pass_rate calculation, report to user
- **FAIL**: Optionally send fix prompt back to the answering session for retry (max 1 retry per QA item). Re-judge after retry.
- **NEEDS_HUMAN_REVIEW**: Flag item for user attention, include in report with judge's cannot_verify details

### Step 5: Aggregate and report

- Calculate `pass_rate` = passed items / total items
- Calculate `avg_score` = mean of all scores
- Output `bench-report.json` at top level with `pass_rate` and `avg_score`
- Present summary to user with per-item breakdown

### Error handling

- Judge spawn failure: log error, mark item as NEEDS_HUMAN_REVIEW with score 0, continue with remaining items
- Timeout (judge > 300s, main agent > 600s per item): mark item as timed out, score 0, continue
- Invalid QA schema: skip item, log warning, do not halt the full run

## 输入规范 / Input Specification

**Named benchmark run:**
- Benchmark name (must match a directory under `benchmarks/`)
- Optional: specific QA indices to run (default: all)

**Ad-hoc evaluation:**
- Question text
- Candidate answer or agent session reference
- Evaluation criteria: gold_answer, must_contain, rubric, pass_threshold (any combination)

## 输出规范 / Output Specification

**Console report:**
```
Benchmark: {name}
Items: {total} | Pass: {passed} | Fail: {failed} | Needs Review: {review}
pass_rate: {rate} | avg_score: {avg}
Per-item details:
  [{index}] {PASS/FAIL/REVIEW} score={score} — {one-line summary}
```

**bench-report.json:**
```json
{
  "benchmark": "{name}",
  "pass_rate": 0.00,
  "avg_score": 0.00,
  "items": [
    {
      "index": 0,
      "verdict": "PASS|FAIL|NEEDS_HUMAN_REVIEW",
      "score": 0.00,
      "summary": "..."
    }
  ]
}
```

## 示例 / Examples

### Example 1: Run a named benchmark

User: "Run the paper-review benchmark"

Main agent:
1. Load `benchmarks/paper-review/qa.jsonl`
2. For each QA, process the question through normal routing
3. Spawn judge for each candidate answer (timeout: 300s per item)
4. Aggregate results, write `bench-report.json`
5. Report: "paper-review benchmark complete: pass_rate=0.85, avg_score=0.82 (17/20 passed)"

### Example 2: Ad-hoc evaluation of a subagent output

User: "Evaluate this idea-generate output against the idea quality rubric"

Main agent:
1. Collect the idea-generate session's final reply and artifact paths
2. Spawn judge with the candidate answer, rubric from user, and any must_contain criteria
3. Report verdict and score; if FAIL, offer to route fix prompt back to idea-generate session
