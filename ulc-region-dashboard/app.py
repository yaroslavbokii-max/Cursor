"""
ULC Activation Cost Share — regional dashboard.
Password: .streamlit/secrets.toml (DASHBOARD_PASSWORD) or DASHBOARD_PASSWORD env var.
Databricks token: ../databricks-dbx/.env (local) or Streamlit Cloud Secrets (DATABRICKS_TOKEN).
"""

from __future__ import annotations

import os
import sys
from calendar import monthrange
from datetime import date, timedelta
from pathlib import Path

import streamlit as st

_APP_DIR = Path(__file__).resolve().parent
if str(_APP_DIR) not in sys.path:
    sys.path.insert(0, str(_APP_DIR))


def _cloud_secrets_to_env() -> None:
    """Streamlit Cloud stores secrets in st.secrets; dbx.py reads DATABRICKS_TOKEN from os.environ."""
    if os.environ.get("DATABRICKS_TOKEN", "").strip():
        return
    try:
        tok = st.secrets.get("DATABRICKS_TOKEN")
        if tok:
            os.environ["DATABRICKS_TOKEN"] = str(tok).strip()
    except Exception:
        pass


_cloud_secrets_to_env()

import pandas as pd

from config import (
    BUSINESS_SEGMENT_V2_OPTIONS,
    DEFAULT_PARTNER_TABLE_LIMIT,
    DEFAULT_REGION_COUNTRIES,
    TOP_BRANDS_BY_BOLT_LIMIT,
    all_selectable_country_codes,
    country_option_label,
)
from data import (
    fetch_brand_cities,
    fetch_brands_by_gmv,
    fetch_providers_by_brand,
    fetch_provider_zones_in_city,
    fetch_region_total,
    fetch_top_brands_by_bolt_spend,
    fetch_ulc_activation_by_country,
)


def _dashboard_password() -> str:
    env = os.environ.get("DASHBOARD_PASSWORD", "").strip()
    if env:
        return env
    try:
        return str(st.secrets.get("DASHBOARD_PASSWORD", "")).strip()
    except Exception:
        return ""


def _require_auth() -> None:
    pw = _dashboard_password()
    if not pw:
        st.error(
            "Password not configured. Create `ulc-region-dashboard/.streamlit/secrets.toml` "
            "with `DASHBOARD_PASSWORD` or export `DASHBOARD_PASSWORD`."
        )
        st.stop()

    if "auth_ok" not in st.session_state:
        st.session_state.auth_ok = False

    if st.session_state.auth_ok:
        return

    st.title("ULC Activation — region")
    entered = st.text_input("Password", type="password", autocomplete="current-password")
    if st.button("Sign in"):
        if entered == pw:
            st.session_state.auth_ok = True
            st.rerun()
        else:
            st.error("Incorrect password")
    st.stop()


def _default_date_range() -> tuple[date, date]:
    today = date.today()
    start = date(today.year, today.month, 1)
    return start, today


def _range_this_month(today: date) -> tuple[date, date]:
    start = date(today.year, today.month, 1)
    _, last = monthrange(today.year, today.month)
    end = date(today.year, today.month, last)
    return start, min(end, today)


def _range_prev_month(today: date) -> tuple[date, date]:
    first_this = date(today.year, today.month, 1)
    last_prev = first_this - timedelta(days=1)
    start = date(last_prev.year, last_prev.month, 1)
    return start, last_prev


def _range_last_n_days(today: date, n: int) -> tuple[date, date]:
    """Last n calendar days including today (n=7 → 7 days)."""
    return today - timedelta(days=n - 1), today


def _previous_period_same_length(d_start: date, d_end: date) -> tuple[date, date]:
    """Prior window of the same length (days), non-overlapping with the selected range."""
    n_days = (d_end - d_start).days + 1
    prev_end = d_start - timedelta(days=1)
    prev_start = prev_end - timedelta(days=n_days - 1)
    return prev_start, prev_end


def _init_period_state() -> None:
    if "date_start" not in st.session_state or "date_end" not in st.session_state:
        s, e = _default_date_range()
        st.session_state.date_start = s
        st.session_state.date_end = e


st.set_page_config(
    page_title="ULC Activation — region",
    page_icon="📊",
    layout="wide",
)

_require_auth()

st.title("ULC Activation cost share — region")
st.caption(
    "Formula: **Merchant / (Merchant + Bolt)** for ULC Activation "
    "(`spend_objective = activation`). Source: `etl_delivery_campaign_order_metrics`."
)

_init_period_state()

st.subheader("Period")
st.caption("Pick dates in the calendars or use a preset — range is **inclusive** (`order_created_date`).")

today = date.today()
p1, p2, p3, p4 = st.columns(4)
with p1:
    if st.button(
        "This month",
        use_container_width=True,
        help="First day of current month through last day of month (or today if month not finished)",
    ):
        s, e = _range_this_month(today)
        st.session_state.date_start = s
        st.session_state.date_end = e
        st.rerun()
with p2:
    if st.button("Previous month", use_container_width=True):
        st.session_state.date_start, st.session_state.date_end = _range_prev_month(today)
        st.rerun()
with p3:
    if st.button("Last 7 days", use_container_width=True):
        st.session_state.date_start, st.session_state.date_end = _range_last_n_days(today, 7)
        st.rerun()
with p4:
    if st.button("Last 30 days", use_container_width=True):
        st.session_state.date_start, st.session_state.date_end = _range_last_n_days(today, 30)
        st.rerun()

cal1, cal2 = st.columns(2)
with cal1:
    d_start = st.date_input(
        "From",
        key="date_start",
        max_value=today,
        help="Click the field to open the calendar. Dates not after today.",
        format="DD/MM/YYYY",
    )
with cal2:
    d_end = st.date_input(
        "To",
        key="date_end",
        min_value=d_start,
        max_value=today,
        help="End of period not after today.",
        format="DD/MM/YYYY",
    )

if d_start > d_end:
    st.warning("“From” is after “To” — adjust one of the calendars.")
    st.stop()

start_s = d_start.isoformat()
end_s = d_end.isoformat()

st.subheader("Country detail")
st.caption(
    "Metrics and drill-down use **`dim_provider_v2.business_segment_v2`** "
    "(SMB / MM / ENT). **ALL** = no segment filter."
)

col_a, col_b, col_c = st.columns([1, 1.2, 0.8])
with col_a:
    st.caption(f"**Selected:** {d_start.strftime('%d/%m/%Y')} — {d_end.strftime('%d/%m/%Y')}")
with col_b:
    countries = st.multiselect(
        "Countries",
        options=all_selectable_country_codes(),
        default=list(DEFAULT_REGION_COUNTRIES),
        format_func=country_option_label,
    )
with col_c:
    segment_v2 = st.selectbox(
        "Business segment v2",
        options=list(BUSINESS_SEGMENT_V2_OPTIONS),
        index=0,
        help="Filter providers (and orders joined through them) to this segment.",
    )

_prev_seg = st.session_state.get("ui_segment_v2")
if _prev_seg is not None and _prev_seg != segment_v2:
    st.session_state.drill_brands_df = None
    st.session_state.drill_top20_df = None
    st.session_state.drill_providers_df = None
    st.session_state.drill_cities_df = None
    st.session_state.drill_zones_df = None
    st.session_state.drill_cities_cache = None
    st.session_state.drill_zones_cache = None
st.session_state.ui_segment_v2 = segment_v2

run = st.button("Refresh data", type="primary")

if "last_df" not in st.session_state:
    st.session_state.last_df = None
if "last_df_prev" not in st.session_state:
    st.session_state.last_df_prev = None
if "last_total" not in st.session_state:
    st.session_state.last_total = None
if "prev_period_label" not in st.session_state:
    st.session_state.prev_period_label = ""

if run and countries:
    with st.spinner("Querying Databricks…"):
        st.session_state.last_df = fetch_ulc_activation_by_country(
            countries, start_s, end_s, business_segment_v2=segment_v2
        )
        st.session_state.last_total = fetch_region_total(
            countries, start_s, end_s, business_segment_v2=segment_v2
        )
        p_start, p_end = _previous_period_same_length(d_start, d_end)
        st.session_state.last_df_prev = fetch_ulc_activation_by_country(
            countries,
            p_start.isoformat(),
            p_end.isoformat(),
            business_segment_v2=segment_v2,
        )
        st.session_state.prev_period_label = (
            f"{p_start.strftime('%d/%m/%Y')} — {p_end.strftime('%d/%m/%Y')}"
        )
        st.session_state.last_query_segment_v2 = segment_v2
elif run and not countries:
    st.warning("Select at least one country.")

df = st.session_state.last_df
df_prev = st.session_state.last_df_prev
total = st.session_state.last_total

if df is not None and total is not None and len(total) > 0:
    m = float(total.iloc[0]["merchant_eur"])
    b = float(total.iloc[0]["bolt_eur"])
    pct = total.iloc[0]["ulc_activation_cost_share_pct"]
    _lq_seg = st.session_state.get("last_query_segment_v2", "ALL")
    st.caption(f"**Segment filter (this load):** {_lq_seg}")

    k1, k2, k3 = st.columns(3)
    k1.metric("Region: Merchant €", f"{m:,.2f}".replace(",", " "))
    k2.metric("Region: Bolt €", f"{b:,.2f}".replace(",", " "))
    k3.metric(
        "Region: cost share %",
        f"{pct:.2f}%" if pct is not None and pct == pct else "—",
    )

    st.subheader("By country")
    if df.empty:
        st.warning("No rows for the selected filters (no ULC activation spend in this period).")
    else:
        merged = df.copy()
        if df_prev is not None and not df_prev.empty:
            prev_pct = df_prev[["country", "ulc_activation_cost_share_pct"]].rename(
                columns={"ulc_activation_cost_share_pct": "cost_share_prev_pct"}
            )
            merged = merged.merge(prev_pct, on="country", how="left")
        else:
            merged["cost_share_prev_pct"] = float("nan")

        merged["delta_pp"] = merged["ulc_activation_cost_share_pct"] - merged[
            "cost_share_prev_pct"
        ]

        display = pd.DataFrame(
            {
                "Country": merged["country"].map(
                    lambda x: country_option_label(str(x)) if pd.notna(x) else "—"
                ),
                "Merchant €": merged["ulc_activation_spend_merchant_eur"],
                "Bolt €": merged["ulc_activation_spend_bolt_eur"],
                "Cost share %": merged["ulc_activation_cost_share_pct"].map(
                    lambda x: f"{x:.2f}%" if pd.notna(x) else "—"
                ),
                "Δ p.p. (vs prior period)": merged.apply(
                    lambda r: (
                        f"{r['delta_pp']:+.2f} p.p."
                        if pd.notna(r["cost_share_prev_pct"])
                        else "—"
                    ),
                    axis=1,
                ),
            }
        )
        if st.session_state.prev_period_label:
            st.caption(
                f"Prior period for Δ: **{st.session_state.prev_period_label}** "
                "(same number of days, immediately before the selected range)."
            )
        st.dataframe(display, use_container_width=True, hide_index=True)
else:
    st.info("Click **Refresh data** to load the table from Databricks.")

st.divider()
st.subheader("Drill-down: brand → partner → city → zone")
st.caption(
    "**1)** Brands — aggregate on `brand_name` / `vendor_name` from `dim_provider_v2` "
    "(same **Business segment v2** as in Country detail). "
    "**2)** Partners — individual `provider_id` within the brand. "
    "**3)** **Cities** — all brand outlets in the country (GMV / ULC sums per `city_id`). "
    "**4)** **Zones** — selected outlet + city (`dim_order_delivery`; first load up to ~1 min)."
)

_partner_opts = all_selectable_country_codes()
_default_idx = _partner_opts.index("ua") if "ua" in _partner_opts else 0

c_p1, c_p2 = st.columns(2)
with c_p1:
    partner_country = st.selectbox(
        "Country (drill-down)",
        options=_partner_opts,
        index=_default_idx,
        format_func=country_option_label,
        key="partner_country_select",
    )
with c_p2:
    partner_limit = st.number_input(
        "Max rows (brands / partners)",
        min_value=50,
        max_value=5000,
        value=min(DEFAULT_PARTNER_TABLE_LIMIT, 5000),
        step=50,
        help="Cap on TOP rows after sorting by GMV.",
    )

load_brands = st.button("1. Load brands", type="secondary")

if "drill_brands_df" not in st.session_state:
    st.session_state.drill_brands_df = None
if "drill_providers_df" not in st.session_state:
    st.session_state.drill_providers_df = None
if "drill_cities_df" not in st.session_state:
    st.session_state.drill_cities_df = None
if "drill_zones_df" not in st.session_state:
    st.session_state.drill_zones_df = None
if "drill_top20_df" not in st.session_state:
    st.session_state.drill_top20_df = None

if load_brands:
    with st.spinner("Loading brands…"):
        st.session_state.drill_brands_df = fetch_brands_by_gmv(
            partner_country,
            start_s,
            end_s,
            limit=int(partner_limit),
            business_segment_v2=segment_v2,
        )
        st.session_state.drill_top20_df = fetch_top_brands_by_bolt_spend(
            partner_country,
            start_s,
            end_s,
            limit=TOP_BRANDS_BY_BOLT_LIMIT,
            business_segment_v2=segment_v2,
        )
        st.session_state.drill_providers_df = None
        st.session_state.drill_cities_df = None
        st.session_state.drill_zones_df = None
        st.session_state.drill_cities_cache = None
        st.session_state.drill_zones_cache = None

brands_df = st.session_state.drill_brands_df
if brands_df is not None:
    if brands_df.empty:
        st.warning("No brand data for this period / country.")
    else:
        _bs_b = (
            brands_df["business_segment_v2"].fillna("—").astype(str).replace({"nan": "—"})
            if "business_segment_v2" in brands_df.columns
            else pd.Series(["—"] * len(brands_df), index=brands_df.index)
        )
        disp_b = pd.DataFrame(
            {
                "Brand": brands_df["brand_name"],
                "Business segment v2": _bs_b,
                "GMV €": brands_df["gmv_eur"],
                "ULC act. Merchant €": brands_df["ulc_activation_merchant_eur"],
                "ULC act. Bolt €": brands_df["ulc_activation_bolt_eur"],
                "Cost share %": brands_df["ulc_activation_cost_share_pct"].map(
                    lambda x: f"{x:.2f}%" if pd.notna(x) else "—"
                ),
            }
        )
        st.caption(
            f"Sorted by **GMV** (top {int(partner_limit)}). Segment filter: **{segment_v2}**."
        )
        st.dataframe(disp_b, use_container_width=True, hide_index=True)

        top20_df = st.session_state.drill_top20_df
        if top20_df is not None and not top20_df.empty:
            st.subheader(
                f"Top {TOP_BRANDS_BY_BOLT_LIMIT} brands by ULC Bolt spend (same country & segment)"
            )
            _bs_t = (
                top20_df["business_segment_v2"].fillna("—").astype(str).replace({"nan": "—"})
                if "business_segment_v2" in top20_df.columns
                else pd.Series(["—"] * len(top20_df), index=top20_df.index)
            )
            disp_t20 = pd.DataFrame(
                {
                    "Brand": top20_df["brand_name"],
                    "Business segment v2": _bs_t,
                    "GMV €": top20_df["gmv_eur"],
                    "ULC act. Merchant €": top20_df["ulc_activation_merchant_eur"],
                    "ULC act. Bolt €": top20_df["ulc_activation_bolt_eur"],
                    "Cost share %": top20_df["ulc_activation_cost_share_pct"].map(
                        lambda x: f"{x:.2f}%" if pd.notna(x) else "—"
                    ),
                }
            )
            st.dataframe(disp_t20, use_container_width=True, hide_index=True)

        brand_pick = st.selectbox(
            "2. Select brand",
            options=brands_df["brand_name"].tolist(),
            key="drill_brand_pick",
        )
        load_providers = st.button("2. Load partners for this brand", type="secondary")

        if load_providers:
            with st.spinner("Loading partners…"):
                st.session_state.drill_providers_df = fetch_providers_by_brand(
                    partner_country,
                    brand_pick,
                    start_s,
                    end_s,
                    limit=int(partner_limit),
                    business_segment_v2=segment_v2,
                )
                st.session_state.drill_cities_df = None
                st.session_state.drill_zones_df = None
                st.session_state.drill_cities_cache = None
                st.session_state.drill_zones_cache = None

providers_df = st.session_state.drill_providers_df
if providers_df is not None:
    if providers_df.empty:
        st.warning("No partners with GMV for this brand in the period.")
    else:
        disp_pr = pd.DataFrame(
            {
                "Partner": providers_df["provider_name"],
                "Provider ID": providers_df["provider_id"].map(
                    lambda x: str(int(x)) if pd.notna(x) else "—"
                ),
                "Business segment v2": (
                    providers_df["business_segment_v2"].fillna("—").astype(str).replace({"nan": "—"})
                    if "business_segment_v2" in providers_df.columns
                    else pd.Series(["—"] * len(providers_df), index=providers_df.index)
                ),
                "GMV €": providers_df["gmv_eur"],
                "ULC act. Merchant €": providers_df["ulc_activation_merchant_eur"],
                "ULC act. Bolt €": providers_df["ulc_activation_bolt_eur"],
                "Cost share %": providers_df["ulc_activation_cost_share_pct"].map(
                    lambda x: f"{x:.2f}%" if pd.notna(x) else "—"
                ),
            }
        )
        st.dataframe(disp_pr, use_container_width=True, hide_index=True)

        _brand_for_cities = str(st.session_state.get("drill_brand_pick", "")).strip()
        _cities_cache_key = (
            _brand_for_cities,
            start_s,
            end_s,
            partner_country,
            segment_v2,
        )
        if _brand_for_cities and st.session_state.get(
            "drill_cities_cache"
        ) != _cities_cache_key:
            with st.spinner("Loading city stats for all brand outlets…"):
                st.session_state.drill_cities_df = fetch_brand_cities(
                    partner_country,
                    _brand_for_cities,
                    start_s,
                    end_s,
                    business_segment_v2=segment_v2,
                )
            st.session_state.drill_cities_cache = _cities_cache_key
            st.session_state.drill_zones_df = None
            st.session_state.drill_zones_cache = None

        cities_df = st.session_state.drill_cities_df
        if cities_df is not None:
            st.subheader("By city (all brand outlets)")
            st.caption(
                "Aggregate across **all partners** of this brand in the country: per city, sum of GMV "
                "and ULC activation across all brand locations in that city for the period."
            )
            if cities_df.empty:
                st.warning(
                    "No city breakdown for this brand in the period (no orders / campaigns)."
                )
                st.session_state.drill_zones_df = None
                st.session_state.drill_zones_cache = None
            else:
                disp_c = pd.DataFrame(
                    {
                        "City": cities_df["city_name"],
                        "City ID": cities_df["city_id"].map(
                            lambda x: str(int(x)) if pd.notna(x) else "—"
                        ),
                        "GMV €": cities_df["gmv_eur"],
                        "ULC act. Merchant €": cities_df["ulc_activation_merchant_eur"],
                        "ULC act. Bolt €": cities_df["ulc_activation_bolt_eur"],
                        "Cost share %": cities_df["ulc_activation_cost_share_pct"].map(
                            lambda x: f"{x:.2f}%" if pd.notna(x) else "—"
                        ),
                    }
                )
                st.dataframe(disp_c, use_container_width=True, hide_index=True)

        _prov_labels = [
            f"{row['provider_name']} ({int(row['provider_id'])})"
            for _, row in providers_df.iterrows()
        ]
        _prov_ids = [int(x) for x in providers_df["provider_id"].tolist()]
        st.selectbox(
            "3. Select outlet (partner) — for zones in a city below",
            options=range(len(_prov_ids)),
            format_func=lambda i: _prov_labels[i],
            key="drill_provider_pick",
        )
        prov_pick_idx = int(st.session_state.get("drill_provider_pick", 0))
        prov_pick_idx = min(prov_pick_idx, len(_prov_ids) - 1) if _prov_ids else 0
        pid = _prov_ids[prov_pick_idx]

        cities_df = st.session_state.drill_cities_df
        if cities_df is not None and not cities_df.empty:
            _city_ids = [int(x) for x in cities_df["city_id"].tolist()]
            _city_labels = [
                f"{n} (id {i})"
                for n, i in zip(cities_df["city_name"].tolist(), _city_ids)
            ]
            st.selectbox(
                "4. Select city — zones for the **selected outlet** in this city",
                options=range(len(_city_ids)),
                format_func=lambda i: _city_labels[i],
                key="drill_city_pick",
            )
            city_pick_idx = int(st.session_state.get("drill_city_pick", 0))
            city_pick_idx = (
                min(city_pick_idx, len(_city_ids) - 1) if _city_ids else 0
            )
            cid = _city_ids[city_pick_idx]

            _zones_cache_key = (pid, cid, start_s, end_s, partner_country)
            if st.session_state.get("drill_zones_cache") != _zones_cache_key:
                with st.spinner(
                    "Loading zone stats for the city (up to ~1 min)…"
                ):
                    st.session_state.drill_zones_df = fetch_provider_zones_in_city(
                        partner_country,
                        pid,
                        cid,
                        start_s,
                        end_s,
                    )
                st.session_state.drill_zones_cache = _zones_cache_key

            zones_df = st.session_state.drill_zones_df
            if zones_df is not None:
                st.subheader("By zone / location (selected city)")
                if zones_df.empty:
                    st.warning(
                        "No zone data or zones could not be loaded for this period."
                    )
                else:
                    disp_z = pd.DataFrame(
                        {
                            "Zone (location)": zones_df["zone_name"],
                            "GMV €": zones_df["gmv_eur"],
                            "ULC act. Merchant €": zones_df[
                                "ulc_activation_merchant_eur"
                            ],
                            "ULC act. Bolt €": zones_df["ulc_activation_bolt_eur"],
                            "Cost share %": zones_df[
                                "ulc_activation_cost_share_pct"
                            ].map(lambda x: f"{x:.2f}%" if pd.notna(x) else "—"),
                        }
                    )
                    st.dataframe(disp_z, use_container_width=True, hide_index=True)

st.divider()
st.markdown(
    "**Updating logic:** edit `config.py` (default countries) and `data.py` (SQL) in the repo — "
    "then teammates `git pull` and restart Streamlit."
)
