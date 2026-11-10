#!/usr/bin/env bash
# Boot ULC Region Dashboard (primary runnable UI). Secrets override the dev default.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

if [[ ! -x .venv/bin/python ]]; then
  echo "Missing .venv — run install first" >&2
  exit 1
fi

export DASHBOARD_PASSWORD="${DASHBOARD_PASSWORD:-cursor-cloud-dev}"

exec .venv/bin/python -m streamlit run ulc-region-dashboard/app.py \
  --server.address=127.0.0.1 \
  --server.port=8501 \
  --server.headless=true
