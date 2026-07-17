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
export BENCH_LOCAL_ENV_FILE="/dev/null"   # /dev/null is not a regular file → env_setup skips sourcing

# --- 2. bring up the container + sync repo + patch openclaw.json + wait ready ---
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

# --- 5b. swap context engine to built-in `legacy` for the bench run.
#        颖姗's production config pins plugins.slots.contextEngine=lossless-claw,
#        but the bench image does NOT ship the lossless-claw extension
#        (OPENCLAW_PLUGINS_ENABLED=false + installPath absent). At runtime the
#        context engine fails to resolve -> "not registered" -> session error,
#        aborting every trial in ~11s. We swap the in-container openclaw.json
#        copy (host config is never touched) to the built-in `legacy` engine
#        and disable the stale lossless-claw entry. This changes which context
#        engine 颍姗 runs under in CI (not its skills/persona), so CI does not
#        exercise lossless-claw - an accepted trade-off (see CLAUDE.md). ---
bench_container_cli exec "$BENCH_CONTAINER" python3 -c '
import json, pathlib
p = pathlib.Path("/home/node/.openclaw/openclaw.json")
d = json.loads(p.read_text(encoding="utf-8"))
slots = d.setdefault("plugins", {}).setdefault("slots", {})
prev = slots.get("contextEngine")
slots["contextEngine"] = "legacy"
entries = d["plugins"].setdefault("entries", {})
lc = entries.get("lossless-claw")
if isinstance(lc, dict):
    lc["enabled"] = False
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"[clawprobench] contextEngine: {prev!r} -> legacy (lossless-claw disabled in bench)")
'

# --- 6. post-patch hard assert: primary must be M3 (fail loud, not silent M2.7) ---
bench_container_cli exec "$BENCH_CONTAINER" python3 -c '
import json, pathlib
d = json.loads(pathlib.Path("/home/node/.openclaw/openclaw.json").read_text())
primary = d.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "")
assert primary == "minimax/MiniMax-M3", f"primary is {primary!r}, expected minimax/MiniMax-M3 (env_setup clobbered by docker/.env.bench?)"
print(f"[clawprobench] model primary OK: {primary}")
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
#        own the session file, matching how the legacy benchmarks invoked main. ---
echo "[clawprobench] run.py --scenario ${SCENARIO} --trials ${TRIALS}"
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
