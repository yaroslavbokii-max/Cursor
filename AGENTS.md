# AGENTS.md

## Cursor Cloud specific instructions

This repo is a **Python-only monorepo** of internal Bolt Food analytics/ops tools plus many
static HTML dashboards, CSV/JSON data files, and a large markdown "Agents" prompt library.
There is no Node.js project, no build step, and no test suite.

### Environment

- Python **3.12** (system). Dependencies are installed into a virtualenv at repo root **`.venv/`**
  by the startup update script (it installs all three `requirements.txt`). `.venv/` is gitignored.
- Activate with `source .venv/bin/activate`, or call binaries directly, e.g. `.venv/bin/python`,
  `.venv/bin/streamlit`. CI pins Python 3.11, but 3.12 works for all dependencies here.

### Runnable components (three Python subprojects)

| Component | Path | Run command | External secret needed for full run |
|---|---|---|---|
| Databricks SQL client + Jira auto-assign | `databricks-dbx/` | `.venv/bin/python dbx.py` (connection test) | `DATABRICKS_TOKEN` |
| ULC Region Dashboard (Streamlit) | `ulc-region-dashboard/` | `.venv/bin/python -m streamlit run app.py` (or `./run_dashboard.sh`), serves on `:8501` | `DASHBOARD_PASSWORD` (login gate) + `DATABRICKS_TOKEN` (data) |
| Sticker Bot (Telegram) | `sticker-bot/` | `.venv/bin/python bot.py` (poll) / `--once` / `--webhook` | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ADMIN_CHAT_ID` |

Everything else (`scripts/` ETL, `docs/` + root `*.html` dashboards, `Agents/` markdown, data
folders) is static/optional and needs no runtime.

### Secrets / how they are loaded (non-obvious)

- All Python tools read `DATABRICKS_TOKEN` from the environment; locally they fall back to
  **`databricks-dbx/.env`** (copy from `databricks-dbx/.env.example`). The Databricks host and
  HTTP path are hardcoded in `databricks-dbx/dbx.py` and `sticker-bot/config.py`.
- `ulc-region-dashboard/app.py` and `scripts/*` **`sys.path`-import `dbx.py` from
  `databricks-dbx/`**, so the sibling folder layout must be preserved (true monorepo).
- Streamlit login: set `DASHBOARD_PASSWORD` env var (or `ulc-region-dashboard/.streamlit/secrets.toml`).
  Without it the app renders an error and stops; with it you get a password gate before the dashboard.
  The app also copies `DATABRICKS_TOKEN` from `st.secrets` into `os.environ` for `dbx.py`.
- `sticker-bot/bot.py` exits immediately with `ERROR: TELEGRAM_BOT_TOKEN not set` if the token is
  missing — expected behavior, not a setup failure.

### Lint / test / build

- **No linter, formatter, or test framework** is configured in the repo. The available syntax check is
  `.venv/bin/python -m py_compile <files>` (all tracked `.py` files compile). There is nothing to build.

### CI reference

- `.github/workflows/` runs the sticker-bot cron and the two dashboard-data export scripts on
  Python 3.11 using `pip install -r <subproject>/requirements.txt`. `sticker-bot/render.yaml`
  deploys the bot on Render (`python bot.py --webhook`).
