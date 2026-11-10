#!/usr/bin/env bash
# Idempotent Cloud Agent bootstrap: shared venv + all Python subproject deps.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

if ! python3 -c "import ensurepip" 2>/dev/null; then
  sudo apt-get update -qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-venv
fi

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi

.venv/bin/pip install -q -U pip wheel

for req in databricks-dbx/requirements.txt ulc-region-dashboard/requirements.txt sticker-bot/requirements.txt; do
  .venv/bin/pip install -q -r "$req"
done

echo "Cloud Agent install OK (.venv ready)"
