#!/usr/bin/env bash
# benchmarks/autoresearch/_env_shared.sh
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
log() { printf '\n[autoresearch.env] %s\n' "$*"; }
if [[ -f "${BENCH_ENV_FILE}" ]]; then
  . "${BENCH_ENV_FILE}"
  bench_force_recreate
fi
log "linking repo benchmarks into workspace"
docker exec "${BENCH_CONTAINER}" bash -lc   "for ws in workspace workspace/curate workspace/judge; do
     mkdir -p '${BENCH_MOUNT}/\${ws}'
     rm -f '${BENCH_MOUNT}/\${ws}/benchmarks'
     ln -s '${BENCH_MOUNT}/benchmarks' '${BENCH_MOUNT}/\${ws}/benchmarks'
   done"
log "env ready"
