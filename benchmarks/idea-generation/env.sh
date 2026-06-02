#!/usr/bin/env bash
# benchmarks/idea-generation/env.sh
# Stages a tiny paper/ directory and qa.jsonl for the main agent's
# idea-generate skill. The fixture is placed inside the
# workspace-idea-generate workspace because that is the sub-agent main
# will spawn; the staging is purely advisory (main's prompt tells it where
# to look).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
RUNTIME_ENV_FILE="${BENCH_RUNTIME_ENV_FILE:-${ROOT}/.bench-runtime/bench-runtime.env}"
if [[ -f "${RUNTIME_ENV_FILE}" ]]; then
  set -a
  # shellcheck disable=SC1090
  . "${RUNTIME_ENV_FILE}"
  set +a
fi

: "${BENCH_CONTAINER:?must be exported by env_setup.sh}"
: "${BENCH_MOUNT:?must be exported by env_setup.sh}"
: "${BENCH_RUN_ID:=local}"

HERE="$(cd "$(dirname "$0")" && pwd)"
log() { printf '\n[idea-generation.env] %s\n' "$*"; }

TARGET="${BENCH_MOUNT}/workspace-idea-generate/bench-fixtures/bench-${BENCH_RUN_ID}/paper"
log "staging paper fixture at ${TARGET}"
docker exec "${BENCH_CONTAINER}" mkdir -p "${TARGET}"

PAPER_A='---
title: "TinyRec: A Toy Recommender Note"
authors: ["Bench Author"]
year: 2026
---
We propose a tiny two-tower recommender. We use L2 normalization on item
embeddings and a temperature of 0.07. On MovieLens-1M we get Recall@20 = 0.18
vs MF baseline 0.15.
'
PAPER_B='---
title: "SparseRec: Sparse Routing For Retrieval"
authors: ["Bench Author"]
year: 2026
---
We replace dense item tower with top-k sparse routing (k=8). On the same
MovieLens-1M split we get Recall@20 = 0.16, but inference FLOPs drop 40%.
'
echo "${PAPER_A}" | docker exec -i "${BENCH_CONTAINER}" bash -lc "cat > ${TARGET}/tinyrec.md"
echo "${PAPER_B}" | docker exec -i "${BENCH_CONTAINER}" bash -lc "cat > ${TARGET}/sparserec.md"

log "staging qa.jsonl"
docker exec "${BENCH_CONTAINER}" mkdir -p \
  "${BENCH_MOUNT}/workspace-idea-generate/bench-fixtures"
docker cp "${HERE}/qa.jsonl" "${BENCH_CONTAINER}:${BENCH_MOUNT}/workspace-idea-generate/bench-fixtures/qa.jsonl"

log "ensuring run dir"
docker exec "${BENCH_CONTAINER}" mkdir -p \
  "${BENCH_MOUNT}/workspace-idea-generate/idea-runs/bench-${BENCH_RUN_ID}"

log "env ready"
