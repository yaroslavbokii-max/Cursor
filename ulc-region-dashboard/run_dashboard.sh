#!/usr/bin/env bash
# Run from any directory: script cd's into the dashboard folder.
set -euo pipefail
cd "$(dirname "$0")"
echo "Open: http://127.0.0.1:8501"
echo "If 'streamlit' is not on PATH, this uses: python3 -m streamlit"
exec python3 -m streamlit run app.py
