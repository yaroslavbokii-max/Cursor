-- Один рядок KPI. Замініть на свій запит до mart / ETL (див. tables-reference у workspace).
-- Колонки нижче мають збігатися з тим, що читає scripts/export_dashboard_data.py
SELECT
  current_timestamp() AS generated_at,
  CAST(12480 AS BIGINT) AS orders,
  CAST(284 AS BIGINT) AS gmv_k_eur,
  CAST(4.6 AS DOUBLE) AS conversion_pct,
  CAST(42 AS INT) AS nps,
  CAST(8.2 AS DOUBLE) AS orders_delta_pct,
  CAST(3.1 AS DOUBLE) AS gmv_delta_pct,
  CAST(-0.2 AS DOUBLE) AS conversion_delta_pp,
  CAST(2 AS INT) AS nps_delta
