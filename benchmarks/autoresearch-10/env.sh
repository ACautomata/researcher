#!/usr/bin/env bash
set -euo pipefail
: "${BENCH_CONTAINER:?}"
: "${BENCH_MOUNT:?}"
: "${BENCH_RUN_ID:=local}"
HERE="$(cd "$(dirname "$0")" && pwd)"
PARENT="$(cd "${HERE}/../autoresearch" && pwd)"
. "${PARENT}/_env_shared.sh"
