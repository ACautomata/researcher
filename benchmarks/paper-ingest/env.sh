#!/usr/bin/env bash
# benchmarks/paper-ingest/env.sh
# Stages a tiny test paper into the autoresearch workspace's raw/inbox so the
# autoresearch agent can be told to ingest it.
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
log() { printf '\n[paper-ingest.env] %s\n' "$*"; }

log "staging inbox paper"
TARGET="${BENCH_MOUNT}/workspace-autoresearch/raw/inbox/bench-${BENCH_RUN_ID}"
docker exec "${BENCH_CONTAINER}" mkdir -p "${TARGET}"

# The benchmark carries a fixture string rather than a real PDF; the agent's
# wiki-organizer must handle text-only inputs gracefully.
FIXTURE='---
title: "BenchIngest: A Synthetic Note For Pipeline Testing"
authors: ["Bench Author"]
year: 2026
venue: "BenchConf"
arxiv: "0000.00000"
---
This is a synthetic paper fixture used by the CI benchmark to verify that
the autoresearch agent can ingest a new paper, produce a wiki page at
wiki/domains/bench/papers/benchingest.md, update wiki/index.md, and append
to wiki/log.md.
'
echo "${FIXTURE}" | docker exec -i "${BENCH_CONTAINER}" bash -lc \
  "cat > ${TARGET}/benchingest.md"

log "staging comparison seed papers"
docker exec "${BENCH_CONTAINER}" mkdir -p \
  "${BENCH_MOUNT}/workspace-autoresearch/wiki/domains/gnn-regularization/papers"
docker exec -i "${BENCH_CONTAINER}" bash -lc "cat > ${BENCH_MOUNT}/workspace-autoresearch/wiki/domains/gnn-regularization/papers/edge-aware.md" <<'EOF'
# Edge-aware regularization

Edge-aware regularization is evaluated on homophilous Cora and CiteSeer settings against GCN/GAT-style baselines and reports 1-3% gains in the synthetic benchmark fixture.
EOF
docker exec -i "${BENCH_CONTAINER}" bash -lc "cat > ${BENCH_MOUNT}/workspace-autoresearch/wiki/domains/gnn-regularization/papers/gated-attention.md" <<'EOF'
# Gated attention for heterophilous graphs

Gated attention is represented here as a heterophilous-graph fixture evaluated on Chameleon only, so comparisons must separate it from Cora/CiteSeer homophilous evidence.
EOF

log "staging qa.jsonl"
docker exec "${BENCH_CONTAINER}" mkdir -p \
  "${BENCH_MOUNT}/workspace-autoresearch/bench-fixtures"
docker cp "${HERE}/qa.jsonl" "${BENCH_CONTAINER}:${BENCH_MOUNT}/workspace-autoresearch/bench-fixtures/qa.jsonl"

log "env ready"
