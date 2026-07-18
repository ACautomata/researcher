# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is the `~/.openclaw` configuration directory for an OpenClaw AI agent gateway. It tracks non-sensitive configuration files in git, synced to `git@github.com:ACautomata/research-agent.git`.

All changes are made via SSH to the remote server. Local clone is at `/Users/junran/Documents/research-agent/`.

## Architecture

This repo follows a **single main agent + two-layer skill** pattern. The main agent is bound to messaging channels and does all domain work itself using skills — it does not spawn producer agents. Cross-agent spawn is limited to `judge` (independent quality gate for key outputs); batch/parallel orchestrators may spawn main's own isolated sub-sessions. See `CONTEXT.md` for the canonical vocabulary and `docs/adr/0001-single-main-agent-two-layer-skills.md` for the decision.

- **openclaw.json** — Main gateway configuration. All secrets use `${ENV_VAR}` references resolved from `.env` (which is gitignored).
- **agents/main/agent/models.json** — Custom model provider definitions (currently MiniMax Anthropic-compatible endpoints).
- **canvas/index.html** — OpenClaw Canvas web UI.
- **workspace/** — Main agent working directory (flattened — no per-agent subdirectories). Contains core workspace files (SOUL.md, AGENTS.md, IDENTITY.md, USER.md, TOOLS.md, MEMORY.md, HEARTBEAT.md, DREAMS.md) and `skills/`. See [docs](https://docs.openclaw.ai/concepts/agent-workspace).
- **workspace/skills/** — Two-layer skills owned by main:
  - **Predicate skills (8, atomic capabilities)**: `ingest`, `curate`, `extract`, `critic`, `design`, `spec`, `audit`, `ideate`. Each is the single source of truth for one research verb.
  - **Orchestrator skills (7, scenario composition)**: `paper-ingest` (ingest→curate), `paper-read` (ingest→extract), `paper-validate` (design→spec), `paper-audit` (audit), `literature-query` (curate), `brainstorm` (curate→ideate), `paper-batch-ingest` (spawn self per paper). They reference predicates in text.
  - `critic` is standalone (no orchestrator wraps it); "完整分析" = main chains `paper-read` → `critic` → `paper-validate` → `paper-audit` directly.
- **judge/** — Judge workspace (sibling of `workspace/`, outside it so main stays flat). Independent quality gate for key outputs.
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

1. **Main agent** — bound to messaging channels, handles user-facing conversation, runs skills directly, and spawns `judge` only for independent quality gating of key outputs.
2. **Predicate skills** — live at `workspace/skills/<predicate>/`. Each is one atomic, reusable research capability (single source of truth for its task, inputs, output shape, completion gate):
   - `ingest` — Paper PDF→wiki page.
   - `curate` — Wiki linting, cross-paper comparison, literature queries.
   - `extract` — Deep experiment extraction (12-section).
   - `critic` — Reviewer-perspective problem analysis (standalone, no orchestrator wraps it).
   - `design` — Validation experiment design (10-section).
   - `spec` — claude-code task prompt generation.
   - `audit` — Analysis-chain quality audit.
   - `ideate` — Research idea card generation.
3. **Orchestrator skills** — live at `workspace/skills/<orchestrator>/`. Compose predicates by **reference** (textual: "run the `ingest` skill"); main loads and runs the referenced predicate. There are 7:
   - `paper-ingest` — ingest→curate.
   - `paper-read` — ingest→extract.
   - `paper-validate` — design→spec (requires `critic` output already in wiki).
   - `paper-audit` — audit.
   - `literature-query` — curate.
   - `brainstorm` — curate→ideate.
   - `paper-batch-ingest` — per paper, spawns a self subagent (isolated context) to run `ingest`.
4. **Full analysis** — no router skill. Main directly chains `paper-read` → `critic` → `paper-validate` → `paper-audit`, persisting each stage to the wiki.

**Constraints:**

- **Single minimal function per predicate.** Each predicate implements exactly one atomic capability. Litmus test: can you describe it in a single verb phrase? If not, split it.
- Orchestrators are thin: they reference predicates and define order/preconditions, never reimplement predicate logic.
- Predicates remain model-invoked (keep a `description`) so orchestrators can reference them and each can fire independently when the operator asks for a single verb.
- The `agents.defaults.subagents.allowAgents` list in `openclaw.json` is `["judge"]` — main may cross-agent spawn only judge. spawn self (`sessions_spawn` without `agentId`, isolated context) is the default capability and needs no allowAgents entry; use it for batch/parallel work (e.g. `paper-batch-ingest`).
- `delegationMode` is `suggest` (not `prefer`) so main is not pushed to delegate; real enforcement is `allowAgents`.
- **Delivery rule (one standing order in `workspace/AGENTS.md`):** a predicate writes its full output to the wiki (via `wiki_apply`) and returns the content in its reply. Main is the single context: within one orchestrator, full-inline passing is fine; cross-orchestrator handoff goes through the wiki. Producer skills never write outputs to the filesystem for other agents to find by path.

### ClawProBench fork CI（active — 颖姗 research 能力门）

CI 实际门控走 **ClawProBench fork**（`ACautomata/ClawResearchBench:fork/target-main`，CI `git clone` 钉定 commit，不进本仓库 git 树），门控 `main`/颖姗跑 research 场景，确定性 `custom_check` grading。控制代码全在 `.github/bench/`（`env_setup.sh` + `run_clawprobench.sh` + `report_clawprobench.py`）+ `.github/workflows/clawprobench.yml`。决策见 [ADR-0002](./docs/adr/0002-clawprobench-fork-target-main.md)。

要点：

- **门控 main agent**：fork 以 `--agent main` 门控颖姗（ADR-0002 核心）。bootstrap 显式 `--model minimax/MiniMax-M3` + post-patch 断言 primary==M3（env_setup 默认 M2.7，必须 pin）。
- **确定性 grading**：fork 用自己的 `run.py` + scenario YAML + `custom_checks/*.py`，从 agent workspace 产物取分，**不依赖 judge agent**；汇总 `pass@3-rate`/`pass^3-rate`/`avg_score`，读 `result_main_<ts>.json` 的 `scenarios[]` 重聚合（见 `report_clawprobench.py`）。
- **本地复现**：`bash .github/bench/run_clawprobench.sh --scenario <id> --trials 1 --keep-container`（先 1 场景×1 trial 冒烟，验证 main 真写出 custom_check 能读到的产物）。scenario id 取 fork `scenarios/research/*.yaml` 顶层 `id:` 字段。
- **secrets**：`LLM_API_KEY`（必填，未配置 fail-fast；fork PR 的 `pull_request` 事件拿不到 secret，用 `workflow_dispatch` 在分支上触发）、`LLM_BASE_URL`（可选，默认 `https://api.minimaxi.com/anthropic`）、`BENCH_BASE_RESULTS_JSON`（可选，映射 `BENCH_BASE_SUMMARY` env 做 PR 评论 delta）。`LLM_MODEL` 不作为 secret--`run_clawprobench.sh` 强制 pin `minimax/MiniMax-M3`。
- **安全**：fork commit pin（默认 `5b368ea`）只经 base-branch repo Variable `CLAWPROBENCH_PIN` 覆盖，**绝不**从 PR-controllable 字段取（run.py 在容器内带 `LLM_API_KEY` 执行）。

### Adding New Skills

The system has exactly two agents (`main`, `judge`). New capabilities are **skills**, not agents:

1. **New predicate** — create `workspace/skills/<verb>/SKILL.md` with `name`, `description` (model-invoked triggers), Mission, scope (do/don't), inputs, output structure, completion gate. Keep it the single source of truth for one verb.
2. **New orchestrator** — create `workspace/skills/<scenario>/SKILL.md` that references predicates by name and defines order/preconditions. Keep it thin.
3. If a scenario needs independent quality gating, spawn `judge` (already in `allowAgents`).
4. Adding a new **agent** is rare and reserved for hard external requirements (like `judge` for independent quality gating); update `openclaw.json` `agents.list`, create the workspace, and add to `allowAgents`.

## PR Rules

- **Do not open upstream PRs before required verification.** 严禁在没有完成本地测试、或 forked repo 的 GitHub Actions benchmark CI 尚未通过时，向上游仓库开 PR。
- **Benchmark results required.** When a PR touches `.github/bench/`, `.github/workflows/clawprobench.yml`, or any skill/agent that has benchmark coverage, first run the relevant scenario locally — `bash .github/bench/run_clawprobench.sh --scenario <id> --trials 1 --keep-container` (smoke one scenario first). Then run the forked-repo `ClawProBench` GitHub Actions workflow (`.github/workflows/clawprobench.yml`; it triggers on `pull_request` for same-repo branches, or use `workflow_dispatch` on the branch to single out a scenario) and wait for it to pass. Paste both local and forked-repo CI benchmark results into the PR description or a PR comment. Do not open a PR without them.
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
