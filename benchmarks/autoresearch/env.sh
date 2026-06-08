#!/usr/bin/env bash
# benchmarks/autoresearch/env.sh
# Wiki fact-recall and cross-paper comparison benchmark.
# No container-side staging needed — wiki content comes from the repo
# (already rsync'd by env_setup.sh), and qa.jsonl is read by run_bench.py
# on the host.
set -euo pipefail

: "${BENCH_CONTAINER:?must be exported by env_setup.sh}"
: "${BENCH_MOUNT:?must be exported by env_setup.sh}"
: "${BENCH_RUN_ID:=local}"

log() { printf '\n[autoresearch.env] %s\n' "$*"; }

# Bring up a fresh openclaw-bench container.
if [[ -f "${BENCH_ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  . "${BENCH_ENV_FILE}"
  bench_force_recreate
fi

log "env ready (wiki content is whatever the repo already contains)"
