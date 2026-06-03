# Benchmarks

Evaluation benchmarks for testing agent capabilities in this multi-agent research system.
The CI workflow (`.github/workflows/benchmark.yml`) runs every benchmark in a dockerized
OpenClaw environment and posts the results as a PR comment.

## Structure

```
benchmarks/
├── README.md                          # This file
├── _common/                           # Shared CI interface (do not put a benchmark here)
│   ├── qa_schema.json                 # JSON Schema for qa.jsonl
│   ├── env_setup.sh                   # Unified env: docker compose + health check
│   ├── run_bench.py                   # Generic driver; all metrics.py shim to this
│   ├── judge.py                       # Reusable rule/agent judges
│   └── report_pr.py                   # Aggregator + PR comment via `gh api`
├── idea-generate/                     # Benchmarks — each must have env.sh + metrics.py + qa.jsonl
├── paper-review/
├── paper-review-pipeline/
├── paper-ingest/
├── idea-generation/
└── autoresearch/
```

## CI policy (binding — see CLAUDE.md "Benchmark 流程")

1. **Main agent only for benchmark tasks.** The CI invokes `openclaw agent --agent main ...` for each QA task.
   Each QA may declare `target_agent` (autoresearch / paper-review / idea-generate / reviewer);
   `run_bench.py` wraps the prompt with a `[BENCHMARK DIRECTIVE]` instructing main to
   use `sessions_spawn(agentId=target_agent, task=...)` and return the sub-agent's
   final reply verbatim. No benchmark task is allowed to call a task sub-agent directly.
   When `judge: "agent"` is used, the reusable judge runs the dedicated `reviewer`
   agent for scoring.
2. **Unified env first.** `benchmarks/_common/env_setup.sh` must run before any
   benchmark's own `env.sh`. It pulls `justlikemaki/openclaw-docker-cn-im`,
   brings up `docker-compose.bench.yml`, rsyncs the repo into the container at
   `/home/node/.openclaw`, and waits for `openclaw health`.
3. **QA schema.** Each `benchmarks/<name>/qa.jsonl` is one JSON per line, conformant
   with `benchmarks/_common/qa_schema.json`. Required: `qa_id`, `question`,
   `agent: "main"`. Optional but recommended: `target_agent`, `gold_answer`,
   `rubric`, `expected_artifacts`. Use `judge: "agent"` when scoring needs the
   strict reviewer LLM judge instead of rule coverage.
4. **Metrics reuse.** `metrics.py` is a 6-line shim that calls
   `benchmarks/_common/run_bench.py:main(name, agent_id="main")`. Custom
   judges must be added in `benchmarks/_common/judge.py`, not duplicated.
5. **PR comment.** `report_pr.py` reads every `bench-results/<name>.json` and
   posts (or upserts) a single Markdown comment with per-benchmark pass rate
   and average score.

## Adding a new benchmark

1. Create `benchmarks/<name>/{env.sh,metrics.py,qa.jsonl}`. Keep `env.sh` small
   (fixture staging only); the heavy lifting is `qa.jsonl`.
2. Add `<name>` to the `BENCH_TARGETS` list in `.github/workflows/benchmark.yml`.
3. Open a PR. The CI workflow will pick it up automatically; the PR comment
   will include the new benchmark's results.

## Running locally

```bash
# 1) Prepare the .env (one-time)
cp docker/.env.bench.example docker/.env.bench
# then edit docker/.env.bench and set MINIMAX_API_KEY.

# 2) Unified env (one per shell; it exports BENCH_CONTAINER etc.)
bash benchmarks/_common/env_setup.sh

# 3) Run any benchmark
bash benchmarks/idea-generate/env.sh
python3 benchmarks/idea-generate/metrics.py
cat benchmarks/idea-generate/bench-report.json | jq

# 4) Or run the whole suite + post a comment
for b in $BENCH_TARGETS; do
  bash benchmarks/$b/env.sh
  python3 benchmarks/$b/metrics.py
done
python3 benchmarks/_common/report_pr.py
```

## Legacy notes

The original `spec.md` files remain under each benchmark directory; the unified
QA schema and CI contract are the source of truth for *how* benchmarks run, but
the spec files still describe the *what* (capability, scoring intent, examples).
