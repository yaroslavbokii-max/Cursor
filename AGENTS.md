# AGENTS.md

## Cursor Cloud specific instructions

This repo is a **Python-only monorepo** of internal Bolt Food analytics/ops tools plus many
static HTML dashboards, CSV/JSON data files, and a large markdown "Agents" prompt library.
There is no Node.js project, no build step, and no test suite.

### Environment

- Python **3.12** (system, at `/usr/bin/python3`). The startup update script creates a
  virtualenv at repo root **`.venv/`** and installs all three `requirements.txt` into it.
  `.venv/` is gitignored.
- Activate with `source .venv/bin/activate`, or call binaries directly, e.g.
  `.venv/bin/python`, `.venv/bin/streamlit`.
- System package `python3.12-venv` is required to create the venv; it is part of the base
  environment/snapshot (installed once via `apt`), so the update script does not reinstall it.
- CI pins Python 3.11, but 3.12 works for all dependencies here.

### Runnable components (three Python subprojects)

| Component | Path | Run command | External secret needed for full run |
|---|---|---|---|
| Databricks SQL client + Jira auto-assign | `databricks-dbx/` | `.venv/bin/python dbx.py` (connection test) | `DATABRICKS_TOKEN` |
| ULC Region Dashboard (Streamlit) | `ulc-region-dashboard/` | `.venv/bin/python -m streamlit run app.py` (or `./run_dashboard.sh`), serves on `127.0.0.1:8501` | `DASHBOARD_PASSWORD` (login gate) + `DATABRICKS_TOKEN` (data) |
| Sticker Bot (Telegram) | `sticker-bot/` | `.venv/bin/python bot.py` (poll) / `--once` / `--webhook` | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ADMIN_CHAT_ID` |

Everything else (`scripts/` ETL, `docs/` + root `*.html` dashboards, `coffeego-prototype/`,
`Agents/` markdown, data folders) is static/optional and needs no runtime.

### Secrets / how they are loaded (non-obvious)

- All Python tools read `DATABRICKS_TOKEN` from the environment; locally they fall back to
  **`databricks-dbx/.env`** (copy from `databricks-dbx/.env.example`). The Databricks host and
  HTTP path are hardcoded in `databricks-dbx/dbx.py` and `sticker-bot/config.py`.
- `ulc-region-dashboard/app.py` and `scripts/*` **`sys.path`-import `dbx.py` from
  `databricks-dbx/`**, so the sibling folder layout must be preserved (true monorepo).
- Streamlit login: set `DASHBOARD_PASSWORD` env var (or `ulc-region-dashboard/.streamlit/secrets.toml`).
  Without it the app renders an error and stops; with it you get a password gate before the dashboard.
  After login the dashboard UI renders immediately; data only loads when you click **Refresh data**,
  which needs `DATABRICKS_TOKEN` (the app copies it from `st.secrets` into `os.environ` for `dbx.py`).
- `sticker-bot/bot.py` exits immediately with `ERROR: TELEGRAM_BOT_TOKEN not set` if the token is
  missing — expected behavior, not a setup failure. Likewise `dbx.py` raises a clear
  "Missing .env / DATABRICKS_TOKEN" error without a token — also expected.

### Lint / test / build

- **No linter, formatter, or test framework** is configured in the repo. The available syntax check is
  `.venv/bin/python -m py_compile $(git ls-files '*.py')` (all tracked `.py` files compile). Nothing to build.

### CI reference

- `.github/workflows/` runs the sticker-bot cron and the two dashboard-data export scripts on
  Python 3.11 using `pip install -r <subproject>/requirements.txt`. `sticker-bot/render.yaml`
  deploys the bot on Render (`python bot.py --webhook`).
