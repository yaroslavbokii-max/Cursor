# Databricks + Cursor Setup Guide

This guide will get your Cursor AI agent connected to Bolt's Databricks SQL warehouse so it can run queries for you on command.

**Time needed:** ~10 minutes.

---

## Step 1: Create a project folder

Create a folder anywhere on your machine. This will be your working directory for Databricks queries.

```bash
mkdir ~/databricks-setup && cd ~/databricks-setup
```

---

## Step 2: Install Python dependencies

Make sure you have Python 3 installed, then run:

```bash
pip3 install databricks-sql-connector pandas
```

(Optional, if you want charting: `pip3 install plotly streamlit`)

---

## Step 3: Generate a Databricks Personal Access Token

1. Go to [https://bolt-incentives.cloud.databricks.com](https://bolt-incentives.cloud.databricks.com)
2. Click your profile icon (top-right) > **Settings**
3. Go to **Developer** > **Access tokens**
4. Click **Generate new token**
5. Give it a description (e.g. "Cursor") and set the lifetime (e.g. 90 days)
6. Copy the token immediately (you won't see it again)

---

## Step 4: Create your `.env` file

In your project folder, create a file called `.env` with your token:

```
DATABRICKS_TOKEN=paste-your-token-here
```

**Do not share this file or commit it to git.**

---

## Step 5: Create the `dbx.py` connection file

Create a file called `dbx.py` in your project folder with this exact content:

```python
"""
Databricks Connection Class
Authenticates with a Personal Access Token loaded from .env.

Usage:
    from dbx import DBX

    dbx = DBX()
    df = dbx.query("SELECT * FROM table LIMIT 10")
    dbx.close()

Or as context manager:
    with DBX() as dbx:
        df = dbx.query("SELECT * FROM table")
"""

from databricks import sql
from pathlib import Path
import pandas as pd

SERVER_HOSTNAME = "bolt-incentives.cloud.databricks.com"
HTTP_PATH = "sql/protocolv1/o/2472566184436351/0221-081903-9ag4bh69"

def _load_token():
    env_path = Path(__file__).parent / ".env"
    for line in env_path.read_text().splitlines():
        if line.startswith("DATABRICKS_TOKEN="):
            return line.split("=", 1)[1].strip()
    raise RuntimeError("DATABRICKS_TOKEN not found in .env")


class DBX:
    """Databricks connection wrapper that returns pandas DataFrames."""

    def __init__(self, http_path=None):
        self.conn = sql.connect(
            server_hostname=SERVER_HOSTNAME,
            http_path=http_path or HTTP_PATH,
        	access_token=_load_token(),
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def query(self, q, params=None):
        """Execute SQL query and return pandas DataFrame."""
        with self.conn.cursor() as cur:
            cur.execute(q, params or None)
            columns = [desc[0] for desc in cur.description]
            return pd.DataFrame(cur.fetchall(), columns=columns)

    def query_to_csv(self, q, filepath, params=None):
        """Execute query and save directly to CSV."""
        df = self.query(q, params)
        df.to_csv(filepath, index=False)
        print(f"Saved {len(df)} rows to {filepath}")
        return df

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    print("Testing connection...")
    with DBX() as dbx:
        df = dbx.query("SELECT 1 AS test")
        print("Connected successfully!" if len(df) else "Something went wrong")
    print("Done.")
```

---

## Step 6: Test the connection

From your project folder, run:

```bash
python3 dbx.py
```

You should see:
```
Testing connection...
Connected successfully!
Done.
```

If you get "PERMISSION_DENIED", you may need access to the Growth Analytics cluster. Ask your manager or check if you have a different cluster, then update the `HTTP_PATH` in `dbx.py`.

---

## Step 7: Add the Cursor rule

This is the key step that teaches your Cursor AI agent how to query Databricks.

Create the file `.cursor/rules/databricks-query.mdc` inside your project folder:

```bash
mkdir -p .cursor/rules
```

Then create `.cursor/rules/databricks-query.mdc` with this content:

```
---
description: Query Bolt's Databricks SQL warehouse when the user includes "dbx" in their message
alwaysApply: true
---

# Databricks Querying (trigger: `dbx`)

ONLY query Databricks when the user includes the word **dbx** in their message.
If the user does NOT say `dbx`, do NOT attempt to query Databricks.

## How to run a query

Use the Shell tool. Replace <YOUR_FOLDER_PATH> below with the absolute path to your project folder (the one containing dbx.py):

` ` `bash
cd <YOUR_FOLDER_PATH> && python3 -c "
from dbx import DBX
with DBX() as dbx:
    df = dbx.query('''<SQL HERE>''')
    print(df.to_string())
"
` ` `

- Always use `with DBX() as dbx:` so the connection closes properly.
- Add `LIMIT` for large results to avoid flooding the terminal.
- Set Shell `block_until_ms` to at least 60000 (queries can take a while).
- To save results: `df.to_csv('/tmp/output.csv', index=False)`.

## Connection details

- Server: `bolt-incentives.cloud.databricks.com`
- HTTP path: `sql/protocolv1/o/2472566184436351/0221-081903-9ag4bh69`
- Auth: Personal Access Token (stored in `.env`)

## Available tables

**ng_public_spark:** `etl_delivery_order_monetary_metrics`, `etl_delivery_campaign_order_metrics`, `etl_delivery_campaigns_enrollments`, `etl_eater_cohorts_lcs_weekly_by_city`, `mart_delivery_eater_primary_city_zone_weekly`, `etl_incentives_provider_targeting_features`

**ng_delivery_spark:** `fact_order_delivery`, `dim_provider_v2`, `dim_delivery_city`, `dim_user_delivery`, `dim_basket_item_delivery`, `dim_order_delivery` *(basket-item grain, not orders; use `fact_order_delivery` for order-level)*, `etl_delivery_order_user_basket_item_v2`, `delivery_provider_provider_trait`, `delivery_campaign_provider`, `delivery_eater_campaign_targeted_campaign`, `dim_courier`, `fact_courier_daily_v2`, `fact_courier_weekly`, `delivery_courier_fleet`, `delivery_order_order_courier_earning`, `delivery_pricing_courier_earning_component`

**ng_delivery_store_spark:** `etl_delivery_store_order_item_cogs`

**core_models_spark:** `fact_user_subscriptions`, `fact_provider_smart_promo_offer_campaign_enrollment`

## Tips

- Discover columns: `DESCRIBE <table_name>`
- Preview data: `SELECT * FROM <table_name> LIMIT 5`
- Common date column: `order_created_date`, works with `DATE_SUB(CURRENT_DATE(), N)`
- **Always filter `order_state = 'delivered'`** for analytics queries (excludes cancelled/rejected orders).
- **Always include the partition column** in WHERE clauses to avoid full table scans. Key partitions: `order_created_date`, `date`, `week_date`, `metric_timestamp_partition`, `basket_item_created_date`.
- **Country column varies by table** (ISO 2-letter codes). Examples for Malta: `city_country_code = 'mt'` (fact_order_delivery), `country = 'mt'` (monetary metrics), `country_code = 'mt'` (dim_provider_v2, eater cohorts), `provider_country_code = 'mt'` (provider targeting), `city_id IN (324, 831)` (courier/basket tables with no country col).
- `order_created_date` in `etl_delivery_order_monetary_metrics` is a **STRING**, not a date. Use string comparison (`>= '2026-01-01'`).
- Courier fact tables use **weighted averages**: `SUM(metric * weight) / NULLIF(SUM(weight), 0)`.
```

**Important:** In the rule above, replace `<YOUR_FOLDER_PATH>` with the actual absolute path to the project folder (e.g. `/Users/yourname/databricks-setup`).

**Note on the backticks:** The triple backticks inside the `.mdc` file above are shown with spaces between them (`` ` ` ` ``) to avoid formatting issues in this guide. When you create the actual file, use normal triple backticks with no spaces (```).

---

## Step 8: Open the folder in Cursor

Open your project folder in Cursor:

```bash
cursor ~/databricks-setup
```

Or use **File > Open Folder** in Cursor and select your folder.

---

## How to use it

Once set up, just include the word **dbx** in your message to Cursor and it will know to query Databricks. Examples:

- "dbx how many orders did we have last week in Malta?"
- "dbx show me the top 10 merchants by GMV in the last 30 days"
- "dbx what's our daily order trend for the past 2 weeks?"
- "dbx describe the fact_order_delivery table"

Cursor will automatically write the SQL, run it against Databricks, and return the results.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `DATABRICKS_TOKEN not found in .env` | Make sure `.env` exists in the same folder as `dbx.py` and contains `DATABRICKS_TOKEN=your-token` |
| `ModuleNotFoundError: databricks` | Run `pip3 install databricks-sql-connector` |
| `PERMISSION_DENIED` | Your token may not have access to this cluster. Try generating a new token or ask for cluster access |
| Cursor doesn't query when you say "dbx" | Make sure `.cursor/rules/databricks-query.mdc` exists in your project folder and the folder is open in Cursor |
| Token expired | Generate a new token (Step 3) and update `.env` |

---

## Folder structure when done

```
~/databricks-setup/
├── .cursor/
│   └── rules/
│       └── databricks-query.mdc    # Cursor rule (teaches AI to query)
├── .env                             # Your Databricks token (DO NOT SHARE)
└── dbx.py                           # Python connection wrapper
```
