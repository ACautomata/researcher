#!/usr/bin/env bash
# Shard of paper-review benchmark.
set -euo pipefail

: "${BENCH_CONTAINER:?must be exported by env_setup.sh}"
: "${BENCH_MOUNT:?must be exported by env_setup.sh}"
: "${BENCH_RUN_ID:=local}"

HERE="$(cd "$(dirname "$0")" && pwd)"
PARENT="$(cd "${HERE}/../paper-review" && pwd)"
# shellcheck disable=SC1090
. "${PARENT}/_env_shared.sh"
