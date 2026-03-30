#!/usr/bin/env python3
"""
Витягує дані з Databricks (3 SQL-файли) і пише docs/dashboard-data.json для GitHub Pages.
Локально: покладіть DATABRICKS_TOKEN у databricks-dbx/.env або в змінну середовища.
У CI: секрет GitHub DATABRICKS_TOKEN.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = DOCS / "dashboard-data.json"

sys.path.insert(0, str(ROOT / "databricks-dbx"))
from dbx import DBX  # noqa: E402


def _serialize_cell(val):
    if val is None:
        return None
    if hasattr(val, "isoformat"):
        return val.isoformat()
    if isinstance(val, (float, int)):
        return val
    return str(val)


def main():
    kpi_path = ROOT / "scripts" / "dashboard_kpi.sql"
    weekly_path = ROOT / "scripts" / "dashboard_weekly.sql"
    pie_path = ROOT / "scripts" / "dashboard_pie.sql"
    for p in (kpi_path, weekly_path, pie_path):
        if not p.is_file():
            raise SystemExit(f"Missing {p}")

    with DBX() as dbx:
        kpi_df = dbx.query(kpi_path.read_text(encoding="utf-8"))
        line_df = dbx.query(weekly_path.read_text(encoding="utf-8"))
        pie_df = dbx.query(pie_path.read_text(encoding="utf-8"))

    if len(kpi_df) != 1:
        raise SystemExit(f"dashboard_kpi.sql must return exactly 1 row, got {len(kpi_df)}")

    kpi_row = kpi_df.iloc[0].to_dict()
    generated_at = kpi_row.pop("generated_at", None)
    kpi = {k: _serialize_cell(v) for k, v in kpi_row.items()}

    line_labels = line_df["day_label"].astype(str).tolist()
    line_values = [int(x) for x in line_df["orders"].tolist()]
    pie_labels = pie_df["label"].astype(str).tolist()
    pie_values = [int(x) for x in pie_df["pct"].tolist()]

    payload = {
        "generated_at": _serialize_cell(generated_at),
        "kpi": kpi,
        "line": {"labels": line_labels, "values": line_values},
        "pie": {"labels": pie_labels, "values": pie_values},
    }

    DOCS.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
