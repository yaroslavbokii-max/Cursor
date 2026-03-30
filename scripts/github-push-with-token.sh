#!/usr/bin/env bash
# Одноразовий push без збереження токена в git config.
# 1) GitHub → Settings → Developer settings → Personal access tokens → згенеруй token (scope: repo).
# 2) У терміналі Cursor на СВОЄМУ Mac (не копіюй токен у чат):
#    export GITHUB_TOKEN=ghp_xxxxxxxx
#    ./scripts/github-push-with-token.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "Потрібна змінна GITHUB_TOKEN (PAT з правом repo)."
  echo "Приклад: export GITHUB_TOKEN=ghp_xxxx && ./scripts/github-push-with-token.sh"
  exit 1
fi

URL="$(git remote get-url origin)"
# https://github.com/owner/repo.git → owner/repo
REPO_PATH="${URL#*github.com/}"
REPO_PATH="${REPO_PATH%.git}"

git push "https://oauth2:${GITHUB_TOKEN}@github.com/${REPO_PATH}.git" HEAD:main
echo "Готово: зміни на GitHub."
