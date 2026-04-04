"""Nova Poshta API helper — warehouse search by city name and type."""

from __future__ import annotations

import logging
import requests

log = logging.getLogger("sticker-bot")

NP_API = "https://api.novaposhta.ua/v2.0/json/"
PAGE_SIZE = 8

TYPE_POSTOMAT = "841339c7-591a-42e2-8233-7a0a00f0ed6f"
TYPE_BRANCH = "9a68df70-0267-42a8-bb5c-37f427e36ee4"

_city_ref_cache: dict[str, str | None] = {}


def _call(method: str, props: dict) -> tuple[list[dict], int]:
    """Call NP API. Returns (data_list, total_count)."""
    try:
        resp = requests.post(NP_API, json={
            "apiKey": "",
            "modelName": "Address",
            "calledMethod": method,
            "methodProperties": props,
        }, timeout=10)
        body = resp.json()
        if body.get("success"):
            total = body.get("info", {}).get("totalCount", 0)
            return body.get("data", []), int(total)
        log.warning("NP API %s error: %s", method, body.get("errors"))
    except Exception as e:
        log.error("NP API %s failed: %s", method, e)
    return [], 0


def get_city_ref(city_name: str) -> str | None:
    if city_name in _city_ref_cache:
        return _city_ref_cache[city_name]
    cities, _ = _call("getCities", {"FindByString": city_name, "Limit": "1"})
    ref = cities[0].get("Ref") if cities else None
    _city_ref_cache[city_name] = ref
    return ref


def _parse_warehouses(raw: list[dict]) -> list[dict]:
    results = []
    for w in raw:
        results.append({
            "number": w.get("Number", "?"),
            "description": w.get("Description", ""),
            "short": f"#{w.get('Number', '?')} — {w.get('ShortAddress', w.get('Description', ''))}",
        })
    return results


def list_warehouses(
    city_name: str,
    warehouse_type: str | None = None,
    page: int = 1,
    query: str = "",
) -> tuple[list[dict], int]:
    """List warehouses with pagination and optional type/search filter.

    Returns (warehouses, total_count).
    """
    city_ref = get_city_ref(city_name)
    if not city_ref:
        return [], 0

    props: dict = {
        "CityRef": city_ref,
        "Page": str(page),
        "Limit": str(PAGE_SIZE),
    }
    if warehouse_type:
        props["TypeOfWarehouseRef"] = warehouse_type
    if query:
        props["FindByString"] = query

    raw, total = _call("getWarehouses", props)
    return _parse_warehouses(raw), total
