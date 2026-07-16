# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is the `~/.openclaw` configuration directory for an OpenClaw AI agent gateway. It tracks non-sensitive configuration files in git, synced to `git@github.com:ACautomata/research-agent.git`.

All changes are made via SSH to the remote server. Local clone is at `/Users/junran/Documents/research-agent/`.

## Architecture

This repo follows a **single main agent + two-layer skill** pattern. The main agent (颖姗) is bound to messaging channels and does all domain work itself using skills — it does not spawn producer agents. Cross-agent spawn is limited to `judge` (quality gate / benchmark scoring); batch/parallel orchestrators may spawn main's own isolated sub-sessions. See `CONTEXT.md` for the canonical vocabulary and `docs/adr/0001-single-main-agent-two-layer-skills.md` for the decision.

- **openclaw.json** — Main gateway configuration. All secrets use `${ENV_VAR}` references resolved from `.env` (which is gitignored).
- **agents/main/agent/models.json** — Custom model provider definitions (currently MiniMax Anthropic-compatible endpoints).
- **canvas/index.html** — OpenClaw Canvas web UI.
- **workspace/** — Main agent (颖姗) working directory (flattened — no per-agent subdirectories). Contains persona files (SOUL.md, AGENTS.md, IDENTITY.md, USER.md, TOOLS.md, MEMORY.md, HEARTBEAT.md, DREAMS.md) and `skills/`. See [docs](https://docs.openclaw.ai/concepts/agent-workspace).
- **workspace/skills/** — Two-layer skills owned by main:
  - **Predicate skills (8, atomic capabilities)**: `ingest`, `curate`, `extract`, `critic`, `design`, `spec`, `audit`, `ideate`. Each is the single source of truth for one research verb.
  - **Orchestrator skills (8, scenario composition)**: `paper-ingest` (ingest→curate), `paper-read` (ingest→extract), `paper-validate` (design→spec), `paper-audit` (audit), `literature-query` (curate), `brainstorm` (curate→ideate), `benchmark` (spawn judge), `paper-batch-ingest` (spawn self per paper). They reference predicates in text.
  - `critic` is standalone (no orchestrator wraps it); "完整分析" = main chains `paper-read` → `critic` → `paper-validate` → `paper-audit` directly.
- **judge/** — Judge workspace (sibling of `workspace/`, outside it so main stays flat). Quality gate + benchmark scoring.
- **benchmarks/** — Developer benchmarks and evaluation datasets for testing agent capabilities.
- **docs/** — Local snapshots of OpenClaw design references (Lobster, Task Flow, Hooks, Standing Orders, Commitments, Automation overview). **Read these before designing any new feature** — start with `docs/README.md` for the "designing X? read Y" index. The canonical source is <https://docs.openclaw.ai/>; refresh the local files when upstream changes.

## Key Configuration Details

- **Gateway**: loopback-bound on port 18789, token auth via `${GATEWAY_TOKEN}`.
- **Model**: Primary `minimax/MiniMax-M3`, fallback `minimax/MiniMax-M3`. Provider auth uses `minimax-oauth` (handled by the minimax plugin).
- **Channels**: Feishu configured with WebSocket mode, pairing DM policy, allowlist group policy. Requires `${FEISHU_APP_ID}` and `${FEISHU_APP_SECRET}` in `.env`.
- **Memory**: QMD backend indexing `**/*.md` in workspace.
- **TTS**: Edge TTS with `zh-CN-XiaoxiaoNeural`.
- **Browser**: Headless Chromium at `/usr/bin/chromium`, no sandbox.
- **Session**: `dmScope: "per-peer"` — each user gets an independent DM session context.

### Gotchas

- Feishu channel: `streaming` must be boolean, not string. No `tools` property at channel level.
- Config validation errors appear in gateway logs on startup.
- `plugins.installs.*.installPath` is the resolved install directory; keep managed installs as absolute paths.
- QMD `paths[].path` entries resolve relative to the agent workspace directory; use `.` for the workspace root.
- External tools (Context7, WebReader) have weekly rate limits — use Playwright to read docs.openclaw.ai as fallback.
- `.env` uses `export VAR="value"` format (shell export syntax).

## Operations

```bash
# Restart gateway after config changes
openclaw gateway restart

# Verify config after restart
openclaw logs --tail 15

# View live logs
openclaw logs --follow

# Check version
openclaw --version

# Feishu pairing management
openclaw pairing list feishu
openclaw pairing approve feishu <CODE>
```

## Architectural Rules

### Workspace Naming

There are exactly two workspaces:

- **Main agent**: `workspace/` (flattened — persona files and `skills/` live directly here, no per-agent subdirectories). Maps to `~/.openclaw/workspace`.
- **Judge**: `judge/` (sibling of `workspace/`, outside it so main stays flat). Maps to `~/.openclaw/judge`.

Both `id` fields match `openclaw.json` → `agents.list[]` (which contains only `main` and `judge`). Producer capabilities (ingest/curate/extract/critic/design/spec/audit/ideate) are **predicate skills** under `workspace/skills/`, not separate workspaces.

### Agent Design Pattern

The system uses a **single main agent + two-layer skills** model. Main does all domain work itself; cross-agent spawn is limited to `judge`, while batch/parallel orchestrators may spawn main's own isolated sub-sessions.

1. **Main agent (颖姗)** — bound to messaging channels, handles user-facing conversation, runs skills directly, and spawns `judge` only for quality gating / benchmark scoring.
2. **Predicate skills** — live at `workspace/skills/<predicate>/`. Each is one atomic, reusable research capability (single source of truth for its task, inputs, output shape, completion gate):
   - `ingest` — Paper PDF→wiki page.
   - `curate` — Wiki linting, cross-paper comparison, literature queries.
   - `extract` — Deep experiment extraction (12-section).
   - `critic` — Reviewer-perspective problem analysis (standalone, no orchestrator wraps it).
   - `design` — Validation experiment design (10-section).
   - `spec` — claude-code task prompt generation.
   - `audit` — Analysis-chain quality audit.
   - `ideate` — Research idea card generation.
3. **Orchestrator skills** — live at `workspace/skills/<orchestrator>/`. Compose predicates by **reference** (textual: "run the `ingest` skill"); main loads and runs the referenced predicate. There are 8:
   - `paper-ingest` — ingest→curate.
   - `paper-read` — ingest→extract.
   - `paper-validate` — design→spec (requires `critic` output already in wiki).
   - `paper-audit` — audit.
   - `literature-query` — curate.
   - `brainstorm` — curate→ideate.
   - `benchmark` — main runs QA, spawns `judge` to score.
   - `paper-batch-ingest` — per paper, spawns a self subagent (isolated context) to run `ingest`.
4. **Full analysis** — no router skill. Main directly chains `paper-read` → `critic` → `paper-validate` → `paper-audit`, persisting each stage to the wiki.

**Constraints:**

- **Single minimal function per predicate.** Each predicate implements exactly one atomic capability. Litmus test: can you describe it in a single verb phrase? If not, split it.
- Orchestrators are thin: they reference predicates and define order/preconditions, never reimplement predicate logic.
- Predicates remain model-invoked (keep a `description`) so orchestrators can reference them and each can fire independently when the operator asks for a single verb.
- The `agents.defaults.subagents.allowAgents` list in `openclaw.json` is `["judge"]` — main may cross-agent spawn only judge. spawn self (`sessions_spawn` without `agentId`, isolated context) is the default capability and needs no allowAgents entry; use it for batch/parallel work (e.g. `paper-batch-ingest`).
- `delegationMode` is `suggest` (not `prefer`) so main is not pushed to delegate; real enforcement is `allowAgents`.
- **Delivery rule (one standing order in `workspace/AGENTS.md`):** a predicate writes its full output to the wiki (via `wiki_apply`) and returns the content in its reply. Main is the single context: within one orchestrator, full-inline passing is fine; cross-orchestrator handoff goes through the wiki. Producer skills never write outputs to the filesystem for other agents to find by path.

### Benchmark CI 流程

仓库 `benchmarks/` 下任何 benchmark **必须**遵守以下约束，缺一不可，PR 校验会失败：

1. **统一入口**：每个 benchmark 目录必须有 `env.sh` 和 `metrics.py` 两个入口，CI 流程按统一方式调用。CI 调度脚本在 `benchmarks/_common/run_bench.py`，自定义 metrics.py 必须通过它路由。
2. **QA schema**：benchmark 题目必须符合 `benchmarks/_common/qa_schema.json`；每条 QA 一行 JSON，存在 `benchmarks/<name>/qa.jsonl`。schema 接受额外字段（`additionalProperties: true`），但禁止删掉必填字段。
3. **强制 main agent 路由**：CI 流程的 benchmark 任务**只**调用 `openclaw agent --agent main ...`，不允许在 `metrics.py`、qa.jsonl 或 prompt 里直接指定其他任务 agent id。所有 QA 直接发给 main，由 main 自行决定是否委派给子 agent（通过 sessions_spawn）或自己处理。`run_bench.py` 对非 main 任务调用做了 hard assert 保护；但 `judge: "agent"` 的 LLM 评分必须使用专门的 `judge` agent。
4. **统一 env 前置**：在跑任何 benchmark 自己的 `env.sh` 之前，CI 必先跑 `benchmarks/_common/env_setup.sh`，启动容器（默认用 Docker Compose，也支持 Apple `container` CLI），把当前仓库同步进容器内 `/home/node/.openclaw`，等 `openclaw health` 就绪，再跑一次 `--agent main --message "ping" --local` 冒烟。benchmark 的 `env.sh` 只能在此基础上做 fixture 写入，**禁止**重启容器、改镜像、或重写统一 env。
5. **Metrics 可复用**：`metrics.py` 必须直接调用 `benchmarks/_common/run_bench.py`（即 6 行 shim），不要自己写 `docker exec openclaw agent`。判分优先用 `benchmarks/_common/judge.py` 提供的 `judge_with_rules` / `judge_with_agent`；自己写 judge 时必须基于 QA 的 `gold_answer.must_contain` 或 `rubric`，禁止用硬编码字符串比对。
6. **PR 评论字段**：CI 会在 PR 评论里汇总每个 benchmark 的 `pass_rate` 和 `avg_score`；新增 benchmark 必须能输出这两个汇总字段（在 `bench-report.json` 顶层），否则不会出现在 PR 评论里。
7. **本地可复现**：推荐使用 `benchmarks/_common/run_local_benchmark.sh <name>` 一键运行单个 benchmark（自动选择 Docker 或 Apple `container` CLI）。手动等价：`bash benchmarks/_common/env_setup.sh && bash benchmarks/<name>/env.sh && python3 benchmarks/<name>/metrics.py`；CI 与本地行为一致。
8. **不要把 secrets 写进仓库**：`LLM_API_KEY` 走 GitHub Actions secret；本地开发用 `docker/.env.bench`（已 gitignore 候选）。`docker/.env.bench.example` 是只读模板。

GitHub 仓库必须配置以下 secret（你最后手动加）：

| Secret | 必填 | 用途 |
| --- | --- | --- |
| `LLM_API_KEY` | 是 | LLM provider key，给 main agent 和 LLM judge 用。未配置时 workflow fail-fast。 |
| `LLM_BASE_URL` | 否 | 默认 `https://api.minimaxi.com/anthropic` |
| `LLM_MODEL` | 否 | 默认 `minimax/MiniMax-M2.7` |
| `BENCH_BASE_RESULTS_JSON` | 否 | 上次 main 跑出的 summary（base64 字符串），用于 PR 评论做 delta 对比 |

### Adding New Skills

The system has exactly two agents (`main`, `judge`). New capabilities are **skills**, not agents:

1. **New predicate** — create `workspace/skills/<verb>/SKILL.md` with `name`, `description` (model-invoked triggers), Mission, scope (do/don't), inputs, output structure, completion gate. Keep it the single source of truth for one verb.
2. **New orchestrator** — create `workspace/skills/<scenario>/SKILL.md` that references predicates by name and defines order/preconditions. Keep it thin.
3. If a scenario needs independent quality gating, spawn `judge` (already in `allowAgents`).
4. Adding a new **agent** is rare and reserved for hard external requirements (like `judge` for CI-mandated independent scoring); update `openclaw.json` `agents.list`, create the workspace, and add to `allowAgents`.

## PR Rules

- **Do not open upstream PRs before required verification.** 严禁在没有完成本地测试、或 forked repo 的 GitHub Actions benchmark CI 尚未通过时，向上游仓库开 PR。
- **Benchmark results required.** When a PR touches `benchmarks/` or any skill/agent that has benchmark coverage, first run the relevant benchmark locally with `benchmarks/_common/run_local_benchmark.sh <name>`, then run the forked-repo `Benchmark` GitHub Actions workflow and wait for it to pass. Paste both local and forked-repo CI benchmark results into the PR description or a PR comment. Do not open a PR without them.
- **Test new features before PR.** Every new feature (skill, agent, workflow, config change) must be tested via OpenClaw — actually trigger the agent in conversation and verify it works end-to-end. Do not open the PR without doing this.

## Gitignore Strategy

`.env` and `auth-profiles.json` contain secrets — never track them. Runtime data (`logs/`, `tasks/`, `*.sqlite`), QMD caches (`qmd/`, `agents/*/qmd/`), CLI-managed dirs (`extensions/`), and channel data (`qqbot/`) are excluded. Agent workspaces and their checked-in skills are tracked, while runtime state inside those workspaces is ignored. `openclaw.json` is tracked because all tokens are env var references.

## Agent skills

### Issue tracker

Issues for this repo live as GitHub issues in `ACautomata/research-agent` via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Five default triage labels: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context — one `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.
