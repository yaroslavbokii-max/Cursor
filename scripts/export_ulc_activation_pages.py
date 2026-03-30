#!/usr/bin/env python3
"""
Експорт тижневих рядів ULC activation cost share у ulc-activation-data/ для статичного дашборда на GitHub Pages.
Логіка збігається з ulc-region-dashboard/data.py (spend_objective = activation).

Локально: DATABRICKS_TOKEN у databricks-dbx/.env або в оточенні.
GitHub Actions: секрет DATABRICKS_TOKEN.

Список країн — змініть DEFAULT_COUNTRIES нижче під свій регіон.
"""
from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "ulc-activation-data"

sys.path.insert(0, str(ROOT / "databricks-dbx"))
from dbx import DBX  # noqa: E402

# Малі літери, як у колонці country у mart
DEFAULT_COUNTRIES: list[str] = ["mt", "ee"]

WEEKS_LOOKBACK = 12


def week_sql(country: str, start: str, end: str) -> str:
    c = country.replace("'", "")
    return f"""
SELECT
  date_format(date_trunc('week', TO_DATE(order_created_date)), 'yyyy-MM-dd') AS week,
  ROUND(SUM(CAST(provider_spend AS DOUBLE)), 2) AS merchant_spend_eur,
  ROUND(SUM(CAST(bolt_spend AS DOUBLE)), 2) AS bolt_spend_eur,
  ROUND(
    SUM(CAST(provider_spend AS DOUBLE))
    / NULLIF(SUM(CAST(provider_spend AS DOUBLE)) + SUM(CAST(bolt_spend AS DOUBLE)), 0) * 100,
    2
  ) AS cost_share_pct
FROM ng_public_spark.etl_delivery_campaign_order_metrics
WHERE spend_objective = 'activation'
  AND LOWER(country) = LOWER('{c}')
  AND order_created_date >= '{start}'
  AND order_created_date <= '{end}'
GROUP BY date_format(date_trunc('week', TO_DATE(order_created_date)), 'yyyy-MM-dd')
ORDER BY week
"""


def main() -> None:
    end_d = date.today()
    start_d = end_d - timedelta(weeks=WEEKS_LOOKBACK)
    start = start_d.strftime("%Y-%m-%d")
    end = end_d.strftime("%Y-%m-%d")
    OUT.mkdir(parents=True, exist_ok=True)
    countries_meta: list[dict] = []
    refreshed = date.today().isoformat()

    with DBX() as dbx:
        for cc in DEFAULT_COUNTRIES:
            df = dbx.query(week_sql(cc, start, end))
            if df.empty:
                df = pd.DataFrame(
                    columns=["week", "merchant_spend_eur", "bolt_spend_eur", "cost_share_pct"]
                )
            path = OUT / f"{cc.lower()}.csv"
            df.to_csv(path, index=False)
            merchant = float(df["merchant_spend_eur"].sum()) if len(df) else 0.0
            bolt = float(df["bolt_spend_eur"].sum()) if len(df) else 0.0
            blended = (100.0 * merchant / (merchant + bolt)) if (merchant + bolt) > 0 else None
            countries_meta.append(
                {
                    "code": cc.lower(),
                    "merchant_eur": round(merchant, 2),
                    "bolt_eur": round(bolt, 2),
                    "cost_share_pct": round(blended, 2) if blended is not None else None,
                    "weeks_loaded": int(len(df)),
                }
            )

    payload = {
        "metric": "ULC activation — cost share",
        "definition": (
            "Merchant spend / (Merchant + Bolt) × 100%, spend_objective = activation. "
            "Таблиця: ng_public_spark.etl_delivery_campaign_order_metrics."
        ),
        "refreshed": refreshed,
        "countries": countries_meta,
    }
    (OUT / "countries.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUT} for {DEFAULT_COUNTRIES} ({start} … {end})")


if __name__ == "__main__":
    main()
