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

# --- 0. fail-fast on the model pin (CI secret / local must both be M3) ---
if [[ -z "${LLM_API_KEY:-}" ]]; then
  echo "::error::LLM_API_KEY is not set." >&2; exit 1
fi

# --- 1. model anti-clobber: load creds from docker/.env.bench, THEN pin M3,
#        THEN block env_setup from re-sourcing docker/.env.bench (which
#        hardcodes M2.7 and would silently overwrite the pin). ---
if [[ -f "${ROOT}/docker/.env.bench" ]]; then
  # shellcheck disable=SC1091
  set -a; . "${ROOT}/docker/.env.bench"; set +a
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

# --- 6. post-patch hard assert: primary must be M3 (fail loud, not silent M2.7) ---
bench_container_cli exec "$BENCH_CONTAINER" python3 -c '
import json, pathlib
d = json.loads(pathlib.Path("/home/node/.openclaw/openclaw.json").read_text())
primary = d.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "")
assert primary == "minimax/MiniMax-M3", f"primary is {primary!r}, expected minimax/MiniMax-M3 (env_setup clobbered by docker/.env.bench?)"
print(f"[clawprobench] model primary OK: {primary}")
'

# --- 7. clone the fork into mktemp (NEVER inside the repo) + cp into container ---
FORK_SRC="$(mktemp -d)/clawprobench"
git clone --depth 1 "${CLAWPROBENCH_REPO}" "${FORK_SRC}" >/dev/null 2>&1
git -C "${FORK_SRC}" fetch --depth 1 origin "${CLAWPROBENCH_PIN}" >/dev/null 2>&1
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

# --- 9. run the fork's run.py: --agent main, explicit --model M3, explicit --results-dir ---
echo "[clawprobench] run.py --scenario ${SCENARIO} --trials ${TRIALS}"
bench_container_cli exec -i \
  -e LLM_API_KEY -e LLM_BASE_URL \
  "$BENCH_CONTAINER" bash -lc '
    set -e
    cd /home/node/.openclaw
    /tmp/crb-venv/bin/python clawprobench/run.py run \
      --agent main \
      --model minimax/MiniMax-M3 \
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
