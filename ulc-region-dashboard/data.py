"""Load ULC activation cost share metrics from Databricks."""

from __future__ import annotations

import sys
from pathlib import Path

# Reuse the shared DBX client from the sibling `databricks-dbx` folder
_ROOT = Path(__file__).resolve().parent.parent
_DBX_DIR = _ROOT / "databricks-dbx"
if _DBX_DIR.is_dir() and str(_DBX_DIR) not in sys.path:
    sys.path.insert(0, str(_DBX_DIR))

from dbx import DBX  # noqa: E402

from config import BUSINESS_SEGMENT_V2_ALL, BUSINESS_SEGMENT_V2_OPTIONS, SPEND_OBJECTIVE_ACTIVATION


def _sql_str(s: str) -> str:
    """Escape single quotes for SQL string literals."""
    return (s or "").replace("'", "''")


def _segment_v2_sql_predicate(p_alias: str, segment_choice: str) -> str:
    """Filter on dim_provider_v2.business_segment_v2; ALL = no filter."""
    s = (segment_choice or BUSINESS_SEGMENT_V2_ALL).strip().upper()
    if s == BUSINESS_SEGMENT_V2_ALL or s not in BUSINESS_SEGMENT_V2_OPTIONS:
        return "1=1"
    # SMB / MM / ENT — match warehouse values case-insensitively
    safe = s.replace("'", "")
    return (
        f"UPPER(TRIM(COALESCE({p_alias}.business_segment_v2, ''))) = '{safe}'"
    )


def fetch_ulc_activation_by_country(
    countries: list[str],
    start_date: str,
    end_date: str,
    business_segment_v2: str = BUSINESS_SEGMENT_V2_ALL,
) -> "object":
    """
    Returns DataFrame: country, merchant_eur, bolt_eur, cost_share_pct.
    start_date / end_date: 'YYYY-MM-DD', both ends inclusive (string day grain in mart).
    """
    import pandas as pd

    if not countries:
        return pd.DataFrame(
            columns=[
                "country",
                "ulc_activation_spend_merchant_eur",
                "ulc_activation_spend_bolt_eur",
                "ulc_activation_cost_share_pct",
            ]
        )

    # Normalise country codes
    codes = [c.lower().strip() for c in countries]
    in_list = ", ".join("'" + c.replace("'", "") + "'" for c in codes)
    seg_pred = _segment_v2_sql_predicate("p", business_segment_v2)

    sql = f"""
    SELECT
      c.country,
      ROUND(SUM(CAST(c.provider_spend AS DOUBLE)), 2) AS ulc_activation_spend_merchant_eur,
      ROUND(SUM(CAST(c.bolt_spend AS DOUBLE)), 2) AS ulc_activation_spend_bolt_eur,
      ROUND(
        SUM(CAST(c.provider_spend AS DOUBLE))
        / NULLIF(
            SUM(CAST(c.provider_spend AS DOUBLE)) + SUM(CAST(c.bolt_spend AS DOUBLE)),
            0
          ) * 100,
        2
      ) AS ulc_activation_cost_share_pct
    FROM ng_public_spark.etl_delivery_campaign_order_metrics c
    INNER JOIN ng_delivery_spark.dim_provider_v2 p
      ON c.provider_id = p.provider_id
      AND LOWER(TRIM(p.country_code)) = LOWER(TRIM(c.country))
    WHERE c.spend_objective = '{SPEND_OBJECTIVE_ACTIVATION}'
      AND c.order_created_date >= '{start_date}'
      AND c.order_created_date <= '{end_date}'
      AND c.country IN ({in_list})
      AND {seg_pred}
    GROUP BY c.country
    ORDER BY ulc_activation_cost_share_pct DESC NULLS LAST, c.country
    """

    with DBX() as dbx:
        df = dbx.query(sql)

    return df


def fetch_region_total(
    countries: list[str],
    start_date: str,
    end_date: str,
    business_segment_v2: str = BUSINESS_SEGMENT_V2_ALL,
) -> "object":
    """Single row: sums across selected countries and blended cost share %."""
    import pandas as pd

    if not countries:
        return pd.DataFrame(
            {
                "merchant_eur": [0.0],
                "bolt_eur": [0.0],
                "ulc_activation_cost_share_pct": [None],
            }
        )

    codes = [c.lower().strip() for c in countries]
    in_list = ", ".join("'" + c.replace("'", "") + "'" for c in codes)
    seg_pred = _segment_v2_sql_predicate("p", business_segment_v2)

    sql = f"""
    SELECT
      ROUND(SUM(CAST(c.provider_spend AS DOUBLE)), 2) AS merchant_eur,
      ROUND(SUM(CAST(c.bolt_spend AS DOUBLE)), 2) AS bolt_eur,
      ROUND(
        SUM(CAST(c.provider_spend AS DOUBLE))
        / NULLIF(
            SUM(CAST(c.provider_spend AS DOUBLE)) + SUM(CAST(c.bolt_spend AS DOUBLE)),
            0
          ) * 100,
        2
      ) AS ulc_activation_cost_share_pct
    FROM ng_public_spark.etl_delivery_campaign_order_metrics c
    INNER JOIN ng_delivery_spark.dim_provider_v2 p
      ON c.provider_id = p.provider_id
      AND LOWER(TRIM(p.country_code)) = LOWER(TRIM(c.country))
    WHERE c.spend_objective = '{SPEND_OBJECTIVE_ACTIVATION}'
      AND c.order_created_date >= '{start_date}'
      AND c.order_created_date <= '{end_date}'
      AND c.country IN ({in_list})
      AND {seg_pred}
    """

    with DBX() as dbx:
        return dbx.query(sql)


def _brand_key_expr() -> str:
    """Same brand expression as dim_provider_v2 (aligned for GROUP BY / WHERE)."""
    return (
        "COALESCE(NULLIF(TRIM(p.brand_name), ''), NULLIF(TRIM(p.vendor_name), ''), 'Unknown brand')"
    )


def fetch_brands_by_gmv(
    country: str,
    start_date: str,
    end_date: str,
    limit: int = 2000,
    business_segment_v2: str = BUSINESS_SEGMENT_V2_ALL,
) -> "object":
    """
    Aggregate by brand_name (from dim_provider_v2): GMV + ULC activation cost share.
    Sorted by GMV descending. business_segment_v2 lists distinct segments across outlets.
    """
    import pandas as pd

    cc = country.lower().strip().replace("'", "")
    if not cc:
        return pd.DataFrame(
            columns=[
                "brand_name",
                "business_segment_v2",
                "gmv_eur",
                "ulc_activation_merchant_eur",
                "ulc_activation_bolt_eur",
                "ulc_activation_cost_share_pct",
            ]
        )

    lim = max(1, min(int(limit), 50_000))
    bk = _brand_key_expr()
    seg_pred = _segment_v2_sql_predicate("p", business_segment_v2)

    sql = f"""
    WITH prov AS (
      SELECT
        p.provider_id,
        {bk} AS brand_name,
        TRIM(p.business_segment_v2) AS business_segment_v2
      FROM ng_delivery_spark.dim_provider_v2 p
      WHERE LOWER(p.country_code) = LOWER('{cc}')
        AND {seg_pred}
    ),
    gmv AS (
      SELECT
        m.provider_id,
        SUM(CAST(m.gmv_eur AS DOUBLE)) AS gmv_eur
      FROM ng_public_spark.etl_delivery_order_monetary_metrics m
      INNER JOIN prov prm ON m.provider_id = prm.provider_id
      WHERE m.country = '{cc}'
        AND m.order_created_date >= '{start_date}'
        AND m.order_created_date <= '{end_date}'
      GROUP BY m.provider_id
    ),
    act AS (
      SELECT
        c.provider_id,
        SUM(CAST(c.provider_spend AS DOUBLE)) AS merchant_eur,
        SUM(CAST(c.bolt_spend AS DOUBLE)) AS bolt_eur
      FROM ng_public_spark.etl_delivery_campaign_order_metrics c
      INNER JOIN prov prc ON c.provider_id = prc.provider_id
      WHERE c.spend_objective = '{SPEND_OBJECTIVE_ACTIVATION}'
        AND c.country = '{cc}'
        AND c.order_created_date >= '{start_date}'
        AND c.order_created_date <= '{end_date}'
      GROUP BY c.provider_id
    ),
    joined AS (
      SELECT
        pr.brand_name,
        pr.business_segment_v2,
        g.gmv_eur AS gmv_provider_eur,
        COALESCE(a.merchant_eur, 0) AS merchant_eur,
        COALESCE(a.bolt_eur, 0) AS bolt_eur
      FROM gmv g
      INNER JOIN prov pr ON g.provider_id = pr.provider_id
      LEFT JOIN act a ON g.provider_id = a.provider_id
    )
    SELECT
      brand_name,
      NULLIF(
        TRIM(concat_ws(', ', sort_array(collect_set(NULLIF(TRIM(business_segment_v2), ''))))),
        ''
      ) AS business_segment_v2,
      ROUND(SUM(gmv_provider_eur), 2) AS gmv_eur,
      ROUND(SUM(merchant_eur), 2) AS ulc_activation_merchant_eur,
      ROUND(SUM(bolt_eur), 2) AS ulc_activation_bolt_eur,
      ROUND(
        SUM(merchant_eur) / NULLIF(SUM(merchant_eur) + SUM(bolt_eur), 0) * 100,
        2
      ) AS ulc_activation_cost_share_pct
    FROM joined
    GROUP BY brand_name
    ORDER BY SUM(gmv_provider_eur) DESC
    LIMIT {lim}
    """

    with DBX() as dbx:
        return dbx.query(sql)


def fetch_top_brands_by_bolt_spend(
    country: str,
    start_date: str,
    end_date: str,
    limit: int = 20,
    business_segment_v2: str = BUSINESS_SEGMENT_V2_ALL,
) -> "object":
    """
    Top brands by ULC activation Bolt spend (same grain as fetch_brands_by_gmv).
    """
    import pandas as pd

    cc = country.lower().strip().replace("'", "")
    if not cc:
        return pd.DataFrame(
            columns=[
                "brand_name",
                "business_segment_v2",
                "gmv_eur",
                "ulc_activation_merchant_eur",
                "ulc_activation_bolt_eur",
                "ulc_activation_cost_share_pct",
            ]
        )

    lim = max(1, min(int(limit), 500))
    bk = _brand_key_expr()
    seg_pred = _segment_v2_sql_predicate("p", business_segment_v2)

    sql = f"""
    WITH prov AS (
      SELECT
        p.provider_id,
        {bk} AS brand_name,
        TRIM(p.business_segment_v2) AS business_segment_v2
      FROM ng_delivery_spark.dim_provider_v2 p
      WHERE LOWER(p.country_code) = LOWER('{cc}')
        AND {seg_pred}
    ),
    gmv AS (
      SELECT
        m.provider_id,
        SUM(CAST(m.gmv_eur AS DOUBLE)) AS gmv_eur
      FROM ng_public_spark.etl_delivery_order_monetary_metrics m
      INNER JOIN prov prm ON m.provider_id = prm.provider_id
      WHERE m.country = '{cc}'
        AND m.order_created_date >= '{start_date}'
        AND m.order_created_date <= '{end_date}'
      GROUP BY m.provider_id
    ),
    act AS (
      SELECT
        c.provider_id,
        SUM(CAST(c.provider_spend AS DOUBLE)) AS merchant_eur,
        SUM(CAST(c.bolt_spend AS DOUBLE)) AS bolt_eur
      FROM ng_public_spark.etl_delivery_campaign_order_metrics c
      INNER JOIN prov prc ON c.provider_id = prc.provider_id
      WHERE c.spend_objective = '{SPEND_OBJECTIVE_ACTIVATION}'
        AND c.country = '{cc}'
        AND c.order_created_date >= '{start_date}'
        AND c.order_created_date <= '{end_date}'
      GROUP BY c.provider_id
    ),
    joined AS (
      SELECT
        pr.brand_name,
        pr.business_segment_v2,
        g.gmv_eur AS gmv_provider_eur,
        COALESCE(a.merchant_eur, 0) AS merchant_eur,
        COALESCE(a.bolt_eur, 0) AS bolt_eur
      FROM gmv g
      INNER JOIN prov pr ON g.provider_id = pr.provider_id
      LEFT JOIN act a ON g.provider_id = a.provider_id
    ),
    by_brand AS (
      SELECT
        brand_name,
        NULLIF(
          TRIM(concat_ws(', ', sort_array(collect_set(NULLIF(TRIM(business_segment_v2), ''))))),
          ''
        ) AS business_segment_v2,
        SUM(gmv_provider_eur) AS gmv_eur,
        SUM(merchant_eur) AS merchant_eur,
        SUM(bolt_eur) AS bolt_eur
      FROM joined
      GROUP BY brand_name
    )
    SELECT
      brand_name,
      business_segment_v2,
      ROUND(gmv_eur, 2) AS gmv_eur,
      ROUND(merchant_eur, 2) AS ulc_activation_merchant_eur,
      ROUND(bolt_eur, 2) AS ulc_activation_bolt_eur,
      ROUND(
        merchant_eur / NULLIF(merchant_eur + bolt_eur, 0) * 100,
        2
      ) AS ulc_activation_cost_share_pct
    FROM by_brand
    ORDER BY bolt_eur DESC
    LIMIT {lim}
    """

    with DBX() as dbx:
        return dbx.query(sql)


def fetch_providers_by_brand(
    country: str,
    brand_name: str,
    start_date: str,
    end_date: str,
    limit: int = 2000,
    business_segment_v2: str = BUSINESS_SEGMENT_V2_ALL,
) -> "object":
    """Partners (provider_id) within the selected brand; sorted by GMV descending."""
    import pandas as pd

    cc = country.lower().strip().replace("'", "")
    bq = _sql_str(brand_name)
    if not cc or not brand_name.strip():
        return pd.DataFrame(
            columns=[
                "provider_id",
                "provider_name",
                "business_segment_v2",
                "gmv_eur",
                "ulc_activation_merchant_eur",
                "ulc_activation_bolt_eur",
                "ulc_activation_cost_share_pct",
            ]
        )

    lim = max(1, min(int(limit), 50_000))
    bk = _brand_key_expr()
    seg_pred = _segment_v2_sql_predicate("p", business_segment_v2)

    sql = f"""
    WITH prov AS (
      SELECT
        p.provider_id,
        MAX(p.provider_name) AS provider_name,
        MAX(TRIM(p.business_segment_v2)) AS business_segment_v2
      FROM ng_delivery_spark.dim_provider_v2 p
      WHERE LOWER(p.country_code) = LOWER('{cc}')
        AND {bk} = '{bq}'
        AND {seg_pred}
      GROUP BY p.provider_id
    ),
    gmv AS (
      SELECT
        m.provider_id,
        SUM(CAST(m.gmv_eur AS DOUBLE)) AS gmv_eur
      FROM ng_public_spark.etl_delivery_order_monetary_metrics m
      INNER JOIN prov pr0 ON m.provider_id = pr0.provider_id
      WHERE m.country = '{cc}'
        AND m.order_created_date >= '{start_date}'
        AND m.order_created_date <= '{end_date}'
      GROUP BY m.provider_id
    ),
    act AS (
      SELECT
        c.provider_id,
        SUM(CAST(c.provider_spend AS DOUBLE)) AS merchant_eur,
        SUM(CAST(c.bolt_spend AS DOUBLE)) AS bolt_eur
      FROM ng_public_spark.etl_delivery_campaign_order_metrics c
      INNER JOIN prov pr0 ON c.provider_id = pr0.provider_id
      WHERE c.spend_objective = '{SPEND_OBJECTIVE_ACTIVATION}'
        AND c.country = '{cc}'
        AND c.order_created_date >= '{start_date}'
        AND c.order_created_date <= '{end_date}'
      GROUP BY c.provider_id
    )
    SELECT
      g.provider_id,
      COALESCE(pr.provider_name, CAST(g.provider_id AS STRING)) AS provider_name,
      pr.business_segment_v2,
      ROUND(g.gmv_eur, 2) AS gmv_eur,
      ROUND(COALESCE(a.merchant_eur, 0), 2) AS ulc_activation_merchant_eur,
      ROUND(COALESCE(a.bolt_eur, 0), 2) AS ulc_activation_bolt_eur,
      ROUND(
        COALESCE(a.merchant_eur, 0)
        / NULLIF(COALESCE(a.merchant_eur, 0) + COALESCE(a.bolt_eur, 0), 0) * 100,
        2
      ) AS ulc_activation_cost_share_pct
    FROM gmv g
    INNER JOIN prov pr ON g.provider_id = pr.provider_id
    LEFT JOIN act a ON g.provider_id = a.provider_id
    ORDER BY g.gmv_eur DESC
    LIMIT {lim}
    """

    with DBX() as dbx:
        return dbx.query(sql)


def fetch_brand_cities(
    country: str,
    brand_name: str,
    start_date: str,
    end_date: str,
    business_segment_v2: str = BUSINESS_SEGMENT_V2_ALL,
) -> "object":
    """
    City breakdown for **all brand outlets** (all provider_id with the same brand_key in country).
    GMV and ULC activation aggregated by city_id across those partners.
    """
    import pandas as pd

    cc = country.lower().strip().replace("'", "")
    bq = _sql_str(brand_name)
    if not cc or not brand_name.strip():
        return pd.DataFrame(
            columns=[
                "city_id",
                "city_name",
                "gmv_eur",
                "ulc_activation_merchant_eur",
                "ulc_activation_bolt_eur",
                "ulc_activation_cost_share_pct",
            ]
        )

    bk = _brand_key_expr()
    seg_pred = _segment_v2_sql_predicate("p", business_segment_v2)

    sql = f"""
    WITH prov AS (
      SELECT p.provider_id
      FROM ng_delivery_spark.dim_provider_v2 p
      WHERE LOWER(p.country_code) = LOWER('{cc}')
        AND {bk} = '{bq}'
        AND {seg_pred}
    ),
    gmv AS (
      SELECT
        m.city_id,
        SUM(CAST(m.gmv_eur AS DOUBLE)) AS gmv_eur
      FROM ng_public_spark.etl_delivery_order_monetary_metrics m
      WHERE m.country = '{cc}'
        AND m.provider_id IN (SELECT provider_id FROM prov)
        AND m.order_created_date >= '{start_date}'
        AND m.order_created_date <= '{end_date}'
      GROUP BY m.city_id
    ),
    act AS (
      SELECT
        c.city_id,
        SUM(CAST(c.provider_spend AS DOUBLE)) AS merchant_eur,
        SUM(CAST(c.bolt_spend AS DOUBLE)) AS bolt_eur
      FROM ng_public_spark.etl_delivery_campaign_order_metrics c
      WHERE c.spend_objective = '{SPEND_OBJECTIVE_ACTIVATION}'
        AND c.country = '{cc}'
        AND c.provider_id IN (SELECT provider_id FROM prov)
        AND c.order_created_date >= '{start_date}'
        AND c.order_created_date <= '{end_date}'
      GROUP BY c.city_id
    ),
    cities AS (
      SELECT city_id, MAX(city_name) AS city_name
      FROM ng_delivery_spark.dim_delivery_city
      WHERE LOWER(country_code) = LOWER('{cc}')
      GROUP BY city_id
    )
    SELECT
      COALESCE(g.city_id, a.city_id) AS city_id,
      COALESCE(ct.city_name, CAST(COALESCE(g.city_id, a.city_id) AS STRING)) AS city_name,
      ROUND(COALESCE(g.gmv_eur, 0), 2) AS gmv_eur,
      ROUND(COALESCE(a.merchant_eur, 0), 2) AS ulc_activation_merchant_eur,
      ROUND(COALESCE(a.bolt_eur, 0), 2) AS ulc_activation_bolt_eur,
      ROUND(
        COALESCE(a.merchant_eur, 0)
        / NULLIF(COALESCE(a.merchant_eur, 0) + COALESCE(a.bolt_eur, 0), 0) * 100,
        2
      ) AS ulc_activation_cost_share_pct
    FROM gmv g
    FULL OUTER JOIN act a ON g.city_id = a.city_id
    LEFT JOIN cities ct ON COALESCE(g.city_id, a.city_id) = ct.city_id
    ORDER BY COALESCE(g.gmv_eur, 0) DESC
    """

    with DBX() as dbx:
        return dbx.query(sql)


def fetch_provider_cities(
    country: str,
    provider_id: int,
    start_date: str,
    end_date: str,
) -> "object":
    """City breakdown for a single provider_id."""
    import pandas as pd

    cc = country.lower().strip().replace("'", "")
    try:
        pid = int(provider_id)
    except (TypeError, ValueError):
        return pd.DataFrame(
            columns=[
                "city_id",
                "city_name",
                "gmv_eur",
                "ulc_activation_merchant_eur",
                "ulc_activation_bolt_eur",
                "ulc_activation_cost_share_pct",
            ]
        )

    if not cc:
        return pd.DataFrame()

    sql = f"""
    WITH gmv AS (
      SELECT
        m.city_id,
        SUM(CAST(m.gmv_eur AS DOUBLE)) AS gmv_eur
      FROM ng_public_spark.etl_delivery_order_monetary_metrics m
      WHERE m.country = '{cc}'
        AND m.provider_id = {pid}
        AND m.order_created_date >= '{start_date}'
        AND m.order_created_date <= '{end_date}'
      GROUP BY m.city_id
    ),
    act AS (
      SELECT
        c.city_id,
        SUM(CAST(c.provider_spend AS DOUBLE)) AS merchant_eur,
        SUM(CAST(c.bolt_spend AS DOUBLE)) AS bolt_eur
      FROM ng_public_spark.etl_delivery_campaign_order_metrics c
      WHERE c.spend_objective = '{SPEND_OBJECTIVE_ACTIVATION}'
        AND c.country = '{cc}'
        AND c.provider_id = {pid}
        AND c.order_created_date >= '{start_date}'
        AND c.order_created_date <= '{end_date}'
      GROUP BY c.city_id
    ),
    cities AS (
      SELECT city_id, MAX(city_name) AS city_name
      FROM ng_delivery_spark.dim_delivery_city
      WHERE LOWER(country_code) = LOWER('{cc}')
      GROUP BY city_id
    )
    SELECT
      COALESCE(g.city_id, a.city_id) AS city_id,
      COALESCE(ct.city_name, CAST(COALESCE(g.city_id, a.city_id) AS STRING)) AS city_name,
      ROUND(COALESCE(g.gmv_eur, 0), 2) AS gmv_eur,
      ROUND(COALESCE(a.merchant_eur, 0), 2) AS ulc_activation_merchant_eur,
      ROUND(COALESCE(a.bolt_eur, 0), 2) AS ulc_activation_bolt_eur,
      ROUND(
        COALESCE(a.merchant_eur, 0)
        / NULLIF(COALESCE(a.merchant_eur, 0) + COALESCE(a.bolt_eur, 0), 0) * 100,
        2
      ) AS ulc_activation_cost_share_pct
    FROM gmv g
    FULL OUTER JOIN act a ON g.city_id = a.city_id
    LEFT JOIN cities ct ON COALESCE(g.city_id, a.city_id) = ct.city_id
    ORDER BY COALESCE(g.gmv_eur, 0) DESC
    """

    with DBX() as dbx:
        return dbx.query(sql)


def fetch_provider_zones_in_city(
    country: str,
    provider_id: int,
    city_id: int,
    start_date: str,
    end_date: str,
) -> "object":
    """
    Delivery zone breakdown (dim_order_delivery: provider_zone_name / user_delivery_zone_name).
    """
    import pandas as pd

    cc = country.lower().strip().replace("'", "")
    try:
        pid = int(provider_id)
        cid = int(city_id)
    except (TypeError, ValueError):
        return pd.DataFrame(
            columns=[
                "zone_name",
                "gmv_eur",
                "ulc_activation_merchant_eur",
                "ulc_activation_bolt_eur",
                "ulc_activation_cost_share_pct",
            ]
        )

    if not cc:
        return pd.DataFrame()

    sql = f"""
    WITH gmv AS (
      SELECT
        COALESCE(
          NULLIF(TRIM(d.provider_zone_name), ''),
          NULLIF(TRIM(d.user_delivery_zone_name), ''),
          'Unknown zone'
        ) AS zone_name,
        SUM(CAST(m.gmv_eur AS DOUBLE)) AS gmv_eur
      FROM ng_public_spark.etl_delivery_order_monetary_metrics m
      INNER JOIN ng_delivery_spark.dim_order_delivery d ON m.order_id = d.order_id
      WHERE m.country = '{cc}'
        AND m.provider_id = {pid}
        AND m.city_id = {cid}
        AND m.order_created_date >= '{start_date}'
        AND m.order_created_date <= '{end_date}'
        AND d.order_created_date_local >= CAST('{start_date}' AS DATE)
        AND d.order_created_date_local <= CAST('{end_date}' AS DATE)
      GROUP BY 1
    ),
    act AS (
      SELECT
        COALESCE(
          NULLIF(TRIM(d.provider_zone_name), ''),
          NULLIF(TRIM(d.user_delivery_zone_name), ''),
          'Unknown zone'
        ) AS zone_name,
        SUM(CAST(c.provider_spend AS DOUBLE)) AS merchant_eur,
        SUM(CAST(c.bolt_spend AS DOUBLE)) AS bolt_eur
      FROM ng_public_spark.etl_delivery_campaign_order_metrics c
      INNER JOIN ng_delivery_spark.dim_order_delivery d ON c.order_id = d.order_id
      WHERE c.spend_objective = '{SPEND_OBJECTIVE_ACTIVATION}'
        AND c.country = '{cc}'
        AND c.provider_id = {pid}
        AND c.city_id = {cid}
        AND c.order_created_date >= '{start_date}'
        AND c.order_created_date <= '{end_date}'
        AND d.order_created_date_local >= CAST('{start_date}' AS DATE)
        AND d.order_created_date_local <= CAST('{end_date}' AS DATE)
      GROUP BY 1
    )
    SELECT
      COALESCE(g.zone_name, a.zone_name) AS zone_name,
      ROUND(COALESCE(g.gmv_eur, 0), 2) AS gmv_eur,
      ROUND(COALESCE(a.merchant_eur, 0), 2) AS ulc_activation_merchant_eur,
      ROUND(COALESCE(a.bolt_eur, 0), 2) AS ulc_activation_bolt_eur,
      ROUND(
        COALESCE(a.merchant_eur, 0)
        / NULLIF(COALESCE(a.merchant_eur, 0) + COALESCE(a.bolt_eur, 0), 0) * 100,
        2
      ) AS ulc_activation_cost_share_pct
    FROM gmv g
    FULL OUTER JOIN act a ON g.zone_name = a.zone_name
    ORDER BY COALESCE(g.gmv_eur, 0) DESC
    """

    with DBX() as dbx:
        return dbx.query(sql)
