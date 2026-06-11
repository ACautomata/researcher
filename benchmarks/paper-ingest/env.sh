#!/usr/bin/env bash
# benchmarks/paper-ingest/env.sh
# Stages a tiny test paper into the ingest workspace's raw/inbox.
# qa.jsonl is read by run_bench.py on the host — no need to stage it.
set -euo pipefail

: "${BENCH_CONTAINER:?must be exported by env_setup.sh}"
: "${BENCH_MOUNT:?must be exported by env_setup.sh}"
: "${BENCH_RUN_ID:=local}"

HERE="$(cd "$(dirname "$0")" && pwd)"
log() { printf '\n[paper-ingest.env] %s\n' "$*"; }

# Bring up a fresh container.
if [[ -f "${BENCH_ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  . "${BENCH_ENV_FILE}"
  bench_force_recreate
fi

# Stage a synthetic paper into the ingest inbox.
TARGET="${BENCH_MOUNT}/workspace/ingest/raw/inbox/bench-${BENCH_RUN_ID}"
log "staging inbox paper at ${TARGET}"
docker exec "${BENCH_CONTAINER}" mkdir -p "${TARGET}"

FIXTURE='---
title: "BenchIngest: A Synthetic Note For Pipeline Testing"
authors: ["Bench Author"]
year: 2026
venue: "BenchConf"
arxiv: "0000.00000"
---
This is a synthetic paper fixture used by the CI benchmark to verify that
the ingest agent can process a new paper, produce a wiki page at
wiki/domains/bench/papers/benchingest.md, update wiki/index.md, and append
to wiki/log.md.
'
echo "${FIXTURE}" | docker exec -i "${BENCH_CONTAINER}" bash -lc \
  "cat > ${TARGET}/benchingest.md"

log "env ready"
