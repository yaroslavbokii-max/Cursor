# ULC Activation — regional dashboard

Streamlit app with **password before entry** (password stays out of GitHub — only in `secrets` or environment variables).

## What’s inside

- Metric: **ULC activation cost share** = Merchant / (Merchant + Bolt), `spend_objective = activation`.
- Default country list for the region: `config.py` → `DEFAULT_REGION_COUNTRIES`.
- SQL: `data.py` (table `ng_public_spark.etl_delivery_campaign_order_metrics`).

## Setup (local)

1. Databricks token lives in **`../databricks-dbx/.env`** (`DATABRICKS_TOKEN`), same as the rest of the workspace.
2. Install dependencies:

   ```bash
   cd ulc-region-dashboard
   pip3 install -r requirements.txt
   ```

3. Dashboard password — copy the example and **do not commit** the real secrets file:

   ```bash
   mkdir -p .streamlit
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   # edit DASHBOARD_PASSWORD
   ```

   Or export: `export DASHBOARD_PASSWORD='...'`

4. Run:

   ```bash
   cd ulc-region-dashboard
   streamlit run app.py
   ```

   Or: `./run_dashboard.sh` (uses `python3 -m streamlit` if `streamlit` is not on `PATH`).

## Updating for the team

Changes to **`config.py`** / **`data.py`** / **`app.py`** → commit + push → teammates `git pull` and restart Streamlit.

## GitHub

- Only **`secrets.toml.example`** goes in the repo, not `secrets.toml`.
- Databricks token stays in **`databricks-dbx/.env`** (ensure `.env` is gitignored in your monorepo).
