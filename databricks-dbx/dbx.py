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
import os
import pandas as pd

SERVER_HOSTNAME = "bolt-incentives.cloud.databricks.com"
HTTP_PATH = "sql/protocolv1/o/2472566184436351/0221-081903-9ag4bh69"


def _load_token():
    token = os.environ.get("DATABRICKS_TOKEN", "").strip().strip('"').strip("'")
    if token:
        return token
    if os.environ.get("GITHUB_ACTIONS", "").lower() == "true":
        raise RuntimeError(
            "DATABRICKS_TOKEN is empty or unset. In GitHub: repo Settings → Secrets and variables → "
            "Actions → New repository secret named exactly DATABRICKS_TOKEN (your Databricks PAT). "
            "Then re-run the workflow."
        )
    env_path = Path(__file__).parent / ".env"
    if not env_path.is_file():
        raise RuntimeError(
            f"Missing {env_path}. Copy .env.example to .env and set DATABRICKS_TOKEN."
        )
    for line in env_path.read_text().splitlines():
        stripped = line.strip()
        if stripped.startswith("#") or not stripped:
            continue
        if stripped.startswith("DATABRICKS_TOKEN="):
            return stripped.split("=", 1)[1].strip().strip('"').strip("'")
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
