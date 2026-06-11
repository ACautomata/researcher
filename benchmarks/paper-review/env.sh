#!/usr/bin/env bash
# benchmarks/paper-review/env.sh
# Paper-review benchmark (full set — for local testing; CI uses shards).
# qa.jsonl is read by run_bench.py on the host — no need to stage it.
set -euo pipefail

: "${BENCH_CONTAINER:?must be exported by env_setup.sh}"
: "${BENCH_MOUNT:?must be exported by env_setup.sh}"
: "${BENCH_RUN_ID:=local}"

HERE="$(cd "$(dirname "$0")" && pwd)"

# Delegate to shared env (stages wiki vault + links benchmarks).
# shellcheck disable=SC1090
. "${HERE}/_env_shared.sh"
