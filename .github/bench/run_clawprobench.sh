#!/usr/bin/env bash
# .github/bench/run_clawprobench.sh
#
# Bootstrap (shared by CI + local) that runs the ClawProBench fork's run.py
# against ONE research scenario, targeting the existing main/颖姗 agent inside
# the openclaw-bench container. Reuses .github/bench/env_setup.sh for container
# bringup (does NOT reinvent docker orchestration).
#
# The fork is cloned at a pinned commit into mktemp (never inside the repo, so
# env_setup's repo-tar sync never sweeps it and it can't be committed).
#
# Usage:
#   bash .github/bench/run_clawprobench.sh --scenario <id> [--trials N] [--keep-container]
#
# Required env: LLM_API_KEY (and LLM_BASE_URL if non-default). LLM_MODEL is
# force-pinned to minimax/MiniMax-M3 here (env_setup's default is M2.7; an
# explicit --model is the only fail-fast against a silent M2.7 clobber).
#
# Outputs: results/result_<scenario>.json (renamed from result_main_<ts>.json)
# for the aggregate step's upload-artifact. Renaming is deterministic so the
# matrix's merge-multiple download can't collide on identical timestamps.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT}"

SCENARIO=""
TRIALS="3"
KEEP_CONTAINER=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --scenario) SCENARIO="$2"; shift 2 ;;
    --trials) TRIALS="$2"; shift 2 ;;
    --keep-container) KEEP_CONTAINER=1; shift ;;
    *) echo "::error::unknown arg: $1" >&2; exit 64 ;;
  esac
done
[[ -n "${SCENARIO}" ]] || { echo "::error::--scenario is required" >&2; exit 64; }
export BENCH_KEEP_CONTAINER="${KEEP_CONTAINER}"

CLAWPROBENCH_PIN="${CLAWPROBENCH_PIN:-5b368ea}"
CLAWPROBENCH_REPO="${CLAWPROBENCH_REPO:-https://github.com/ACautomata/ClawResearchBench.git}"
RESULTS_DIR="${ROOT}/results"
mkdir -p "${RESULTS_DIR}"

# --- 0. load local creds (docker/.env.bench) FIRST, then fail-fast, then pin M3.
#        Order matters: the fail-fast must run AFTER sourcing docker/.env.bench
#        (local runs get LLM_API_KEY from there; CI has it in the secret env and
#        docker/.env.bench is absent). Then block env_setup from re-sourcing
#        docker/.env.bench (which would re-clobber LLM_MODEL) via /dev/null. ---
if [[ -f "${ROOT}/docker/.env.bench" ]]; then
  # shellcheck disable=SC1091
  set -a; . "${ROOT}/docker/.env.bench"; set +a
fi
if [[ -z "${LLM_API_KEY:-}" ]]; then
  echo "::error::LLM_API_KEY is not set (export it or put it in docker/.env.bench)." >&2; exit 1
fi
export LLM_MODEL="minimax/MiniMax-M3"
export LLM_BASE_URL="${LLM_BASE_URL:-https://api.minimaxi.com/anthropic}"
# Enable plugin loading: main's research skills (ingest/design/paper-validate/
# audit) call the plugin-backed wiki_apply/wiki_search tools (workspace/TOOLS.md,
# ADR-0002). The bench image ships memory-wiki as a stock extension, but
# OPENCLAW_PLUGINS_ENABLED gates whether it loads; env_setup interpolates this
# into the compose env (docker-compose.bench.yml), so it must be exported BEFORE
# env_setup brings the container up. lossless-claw is NOT shipped (its installPath
# resolves to a seed cache only) and is disabled by the config patch below; the
# other enabled entries (minimax/browser/memory-core/memory-wiki) are all stock.
export OPENCLAW_PLUGINS_ENABLED=true
export BENCH_LOCAL_ENV_FILE="/dev/null"   # not a regular file, so env_setup skips sourcing it

# --- 2. bring up the container + sync repo + patch openclaw.json + wait ready.
#        FIRST, delete any residual state/openclaw.sqlite from a prior run:
#        the container's init.sh creates a fresh sqlite db on first boot. If a
#        stale/corrupted db exists (e.g. from a crashed startup migration on
#        macOS Docker Desktop virtiofs), the gateway fails with "disk I/O
#        error" or "startup migrations already running". CI always starts
#        clean (new runner), but local --keep-container reuse needs the sweep. ---
rm -f "${ROOT}/.bench-runtime/openclaw-data/state/openclaw.sqlite" \
       "${ROOT}/.bench-runtime/openclaw-data/state/openclaw.sqlite"-* 2>/dev/null || true
BENCH_RUN_ID="${BENCH_RUN_ID:-clawpro-$$}"
export BENCH_RUN_ID
echo "[clawprobench] env_setup (run_id=${BENCH_RUN_ID}, scenario=${SCENARIO}, trials=${TRIALS})"
bash "${ROOT}/.github/bench/env_setup.sh"

# --- 3. source the contract + bench_* helpers (bench_container_cli, bench_teardown) ---
# shellcheck disable=SC1091
. "${ROOT}/.bench-runtime/bench-runtime-env.sh"
: "${BENCH_CONTAINER:?env_setup did not export BENCH_CONTAINER}"

# --- 4. conditional teardown trap (bench_teardown has no --keep-container flag) ---
trap '${BENCH_KEEP_CONTAINER:+:} bench_teardown' EXIT

# --- 5. health self-check (gateway status, NOT openclaw health) ---
bench_container_cli exec "$BENCH_CONTAINER" openclaw gateway status >/dev/null

# --- 5b. bench-container config patches (in-container openclaw.json copy;
#        host config is never touched). Three patches, all required for 2026.7.1:
#
#        (a) context engine: 颖姗 pins plugins.slots.contextEngine=lossless-claw,
#            but the bench image does NOT ship the lossless-claw extension
#            (only a seed cache; OPENCLAW_PLUGINS_ENABLED=true now loads stock
#            plugins). At runtime the context engine fails "not registered" ->
#            session error. Swap to the built-in `legacy` engine + disable the
#            stale entry. CI does not exercise lossless-claw (accepted trade-off,
#            see CLAUDE.md).
#
#        (b) memory-wiki: ensure enabled. The stock extension ships in the image
#            and OPENCLAW_PLUGINS_ENABLED=true (exported above) lets it load,
#            but defensively flip the entry on in case env_setup's config sync
#            reset it. wiki_apply/wiki_search are required by the research
#            scenarios' workspace_live custom_checks (ADR-0002).
#
#        (c) channels: OpenClaw 2026.7.1 doctor auto-installs the feishu/discord
#            plugins, after which a channel with enabled:true requires its
#            SecretRef (FEISHU_APP_SECRET etc.) -> gateway fails to start with
#            "required secrets are unavailable" in a bench container that has
#            no channel creds. bench only runs `openclaw agent`, never channels,
#            so disable every channel account. ---
bench_container_cli exec "$BENCH_CONTAINER" python3 -c '
import json, pathlib
p = pathlib.Path("/home/node/.openclaw/openclaw.json")
d = json.loads(p.read_text(encoding="utf-8"))

# (a) context engine -> legacy
slots = d.setdefault("plugins", {}).setdefault("slots", {})
prev_ce = slots.get("contextEngine")
slots["contextEngine"] = "legacy"
entries = d["plugins"].setdefault("entries", {})
lc = entries.get("lossless-claw")
if isinstance(lc, dict):
    lc["enabled"] = False

# (b) memory-wiki -> enabled (stock extension; wiki_apply/wiki_search)
mw = entries.setdefault("memory-wiki", {})
if isinstance(mw, dict):
    mw_prev = mw.get("enabled")
    mw["enabled"] = True

# (c) disable all channel accounts
disabled = []
channels = d.get("channels", {})
if isinstance(channels, dict):
    for ch_name, ch_cfg in channels.items():
        if not isinstance(ch_cfg, dict):
            continue
        if ch_cfg.get("enabled") is not None:
            ch_cfg["enabled"] = False
            disabled.append(f"{ch_name} (top)")
        accs = ch_cfg.get("accounts", {})
        if isinstance(accs, dict):
            for acc_name, acc in accs.items():
                if isinstance(acc, dict) and acc.get("enabled") is not None:
                    acc["enabled"] = False
                    disabled.append(f"{ch_name}/{acc_name}")

p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"[clawprobench] contextEngine: {prev_ce!r} -> legacy (lossless-claw disabled)")
mw_now = mw.get("enabled") if isinstance(mw, dict) else None
print(f"[clawprobench] memory-wiki: enabled={mw_now} (was {mw_prev!r})")
_ch_summary = ", ".join(disabled) if disabled else "none present"
print(f"[clawprobench] channels disabled: {_ch_summary}")
'

# --- 6. post-patch hard assert: primary must be M3 (fail loud, not silent M2.7)
#        and memory-wiki must be enabled (research skills need wiki_apply/
#        wiki_search; a silent false here means env_setup's config sync reset it
#        and every workspace_live scenario would score 0). ---
bench_container_cli exec "$BENCH_CONTAINER" python3 -c '
import json, pathlib
d = json.loads(pathlib.Path("/home/node/.openclaw/openclaw.json").read_text())
primary = d.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "")
assert primary == "minimax/MiniMax-M3", f"primary is {primary!r}, expected minimax/MiniMax-M3 (env_setup clobbered by docker/.env.bench?)"
print(f"[clawprobench] model primary OK: {primary}")
mw = d.get("plugins", {}).get("entries", {}).get("memory-wiki", {})
mw_enabled = mw.get("enabled") if isinstance(mw, dict) else None
assert mw_enabled is True, f"memory-wiki enabled is {mw_enabled!r}, expected True (without it wiki_apply/wiki_search are unavailable)"
print(f"[clawprobench] memory-wiki enabled OK: {mw_enabled}")
'

# --- 7. clone the fork into mktemp (NEVER inside the repo) + cp into container ---
# --- 7. clone the fork into mktemp (NEVER inside the repo) + cp into container.
#        --filter=blob:none (partial clone) lets us checkout an arbitrary pinned
#        commit SHA without fetching the full history; GitHub rejects shallow
#        fetch-by-SHA for non-HEAD commits. The pin defaults to 5b368ea (PR #7
#        merge = current fork main HEAD); override only via a base-branch
#        Variable (CLAWPROBENCH_PIN), never PR-controllable input. ---
FORK_SRC="$(mktemp -d)/clawprobench"
# --filter=blob:none: partial clone (no history blobs) that still lets us
# checkout any reachable pinned commit. GitHub rejects shallow fetch-by-SHA
# for non-HEAD commits, so --depth 1 is the wrong tool here. The fetch of the
# default ref brings in the commit graph; checkout then resolves the SHA.
git clone --quiet --filter=blob:none --no-checkout "${CLAWPROBENCH_REPO}" "${FORK_SRC}"
git -C "${FORK_SRC}" fetch --quiet origin
git -C "${FORK_SRC}" checkout -q "${CLAWPROBENCH_PIN}"
echo "[clawprobench] fork pinned at ${CLAWPROBENCH_PIN}"
bench_container_cli cp "${FORK_SRC}" "${BENCH_CONTAINER}:/home/node/.openclaw/clawprobench"

# --- 8. install fork deps into an isolated venv (don't perturb openclaw's system python) ---
bench_container_cli exec "$BENCH_CONTAINER" bash -lc '
  set -e
  if [ ! -d /tmp/crb-venv ]; then
    python3 -m venv /tmp/crb-venv
  fi
  /tmp/crb-venv/bin/pip install -q --upgrade pip >/dev/null 2>&1 || true
  /tmp/crb-venv/bin/pip install -q -r /home/node/.openclaw/clawprobench/requirements.txt
  echo "[clawprobench] fork deps installed into /tmp/crb-venv"
'
bench_container_cli exec "$BENCH_CONTAINER" openclaw gateway status >/dev/null \
  && echo "[clawprobench] openclaw runtime healthy after venv install"

# --- 9. run the fork's run.py: --agent main, explicit --model M3, explicit --results-dir.
#        --local-agent: make the fork pass --local to `openclaw agent` (embedded
#        mode). Without it, fork runs gateway mode but passes a self-generated
#        --session-id that clashes with the gateway's own session bookkeeping,
#        surfacing as "session file changed while embedded prompt lock was
#        released" and aborting every trial in ~15s. Embedded mode has the fork
#        own the session file, matching how the legacy benchmarks invoked main.
#        --benchmark-status all: research scenarios are benchmark_status=incubating
#        (ADR-0002); the fork's default `core` profile filters to status=active
#        and select_scenarios drops non-matching ids EVEN when --scenario names
#        one explicitly (harness/loader.py:269), so every research_* matrix job
#        would resolve zero scenarios without this override. ---
echo "[clawprobench] run.py --scenario ${SCENARIO} --trials ${TRIALS} --benchmark-status all"
bench_container_cli exec -i \
  -e LLM_API_KEY -e LLM_BASE_URL \
  "$BENCH_CONTAINER" bash -lc '
    set -e
    cd /home/node/.openclaw
    /tmp/crb-venv/bin/python clawprobench/run.py run \
      --agent main \
      --model minimax/MiniMax-M3 \
      --local-agent \
      --scenario "'"${SCENARIO}"'" \
      --trials "'"${TRIALS}"'" \
      --benchmark-status all \
      --execution-mode live \
      --results-dir /home/node/.openclaw/results
  '

# --- 10. copy out the report + rename deterministically (avoid artifact collisions) ---
REMOTE_REPORT="$(bench_container_cli exec "$BENCH_CONTAINER" bash -lc '
  ls -1t /home/node/.openclaw/results/result_main_*.json 2>/dev/null | head -1
')"
[[ -n "${REMOTE_REPORT}" ]] || { echo "::error::no result_main_*.json produced for ${SCENARIO}" >&2; exit 1; }
OUT="${RESULTS_DIR}/result_${SCENARIO}.json"
bench_container_cli cp "${BENCH_CONTAINER}:${REMOTE_REPORT}" "${OUT}"
echo "[clawprobench] wrote ${OUT}"
