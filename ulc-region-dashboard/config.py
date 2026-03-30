"""Region and dashboard constants — edit here to change defaults for your team."""

from __future__ import annotations

# ISO country codes (lowercase), as in ng_public_spark.etl_delivery_campaign_order_metrics.country
DEFAULT_REGION_COUNTRIES: tuple[str, ...] = (
    "az",
    "pl",
    "ua",
    "ke",
    "gh",
    "cy",
    "pt",
    "bg",
)

# Extra codes in the “all countries” filter (drill-down + multiselect)
EXTRA_COUNTRY_CODES: frozenset[str] = frozenset(
    {"cz", "ee", "lt", "lv", "mt", "ro", "sk", "ge"}
)

# UI labels (English); SQL still uses lowercase ISO codes
COUNTRY_DISPLAY_NAME: dict[str, str] = {
    "az": "Azerbaijan",
    "bg": "Bulgaria",
    "cy": "Cyprus",
    "cz": "Czechia",
    "ee": "Estonia",
    "ge": "Georgia",
    "gh": "Ghana",
    "ke": "Kenya",
    "lt": "Lithuania",
    "lv": "Latvia",
    "mt": "Malta",
    "pl": "Poland",
    "pt": "Portugal",
    "ro": "Romania",
    "sk": "Slovakia",
    "ua": "Ukraine",
}


def country_option_label(code: str) -> str:
    """Dropdown label: name + code in parentheses."""
    c = (code or "").lower().strip()
    name = COUNTRY_DISPLAY_NAME.get(c)
    if name:
        return f"{name} ({c})"
    return c or "—"


def all_selectable_country_codes() -> list[str]:
    """Sorted list of codes for multiselect / selectbox."""
    return sorted(set(DEFAULT_REGION_COUNTRIES) | EXTRA_COUNTRY_CODES)


# Bolt ULC activation in the mart = spend_objective 'activation' (not sp_activation)
SPEND_OBJECTIVE_ACTIVATION = "activation"

# Max rows in brand/partner tables (safety cap)
DEFAULT_PARTNER_TABLE_LIMIT = 2000
