#!/usr/bin/env bash
# Публікує папку docs/ на GitHub (потрібен один раз налаштований git push: SSH або gh auth / збережений пароль).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

MSG="${1:-Update docs $(date -u +%Y-%m-%dT%H:%MZ)}"

git add docs/
if git diff --staged --quiet; then
  echo "Немає змін у docs/ — нічого комітити."
  exit 0
fi

git commit -m "$MSG"
git push origin main
echo "Готово: зміни в docs/ відправлено на GitHub. Pages оновиться за ~1 хв."
