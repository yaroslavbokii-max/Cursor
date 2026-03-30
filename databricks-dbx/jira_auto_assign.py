"""
Auto-assign UAM Jira tickets to the responsible Account Manager.

Flow:
  1. Fetch unassigned tickets from UAM board
  2. Extract provider_id from summary/description (incl. ADF), optional custom field
  3. Query Databricks for account_manager_name
  4. Look up AM's Jira account ID (exact + fuzzy display-name match)
  5. Assign; if AM / route owner unknown → fallback (default: Joanna Lizza Ayson, configurable)

Schedule via cron:
  crontab -e
  0 9,14 * * 1-5 cd /Users/yaroslav/Desktop/cursor/databricks-dbx && /usr/bin/python3 jira_auto_assign.py >> /tmp/jira_auto_assign.log 2>&1

Env (optional, in .env):
  UAM_AUTO_ASSIGN_EXTRA_JQL   — appended to JQL (e.g. AND status = "AM Tickets")
  UAM_MAX_ISSUES              — max issues per run (default 200)
  JIRA_CUSTOM_FIELD_PROVIDER  — e.g. customfield_12345 — numeric provider id from Jira
  UAM_FALLBACK_DISPLAY_NAME   — Jira display name for fallback (default Joanna Lizza Ayson)
  UAM_FALLBACK_ACCOUNT_ID     — optional accountId; if set, skips name lookup
  UAM_DRY_RUN                 — set to 1 to log actions without assigning
  UAM_SKIP_UNKNOWN_ASSIGNEE   — set to 1 to only assign when AM / Tetiana / Anna resolves; skip others (no fallback)
  UAM_MAX_TICKET_AGE_DAYS     — only issues created within this many days (default 30). Set to 0 to disable (assign old tickets too).
  UAM_STATUS_IN               — comma-separated Jira status names to include only those columns, e.g. "All Tickets,AM TICKETS"
                              (exact spelling as in Issue → Status). Empty = all non-Done statuses. Do not duplicate status in UAM_AUTO_ASSIGN_EXTRA_JQL.

  Special routes (keyword → assignee + optional column transition):
  UAM_ROUTE_RULES_ENABLED=1   — Legal/FOP → Tetiana (SIMPLY_2PRIORITY); financial/Vchasno/invoices → Anna (MOPS TICKETS)
  UAM_ACCOUNT_ID_TETIANA / UAM_ACCOUNT_ID_ANNA — Jira accountIds (recommended); else display names resolved via search
  UAM_DISPLAY_NAME_TETIANA / UAM_DISPLAY_NAME_ANNA — fallback for user lookup
  UAM_STATUS_NAME_SIMPLY2 / UAM_STATUS_NAME_MOPS — exact Jira status names for transitions
  UAM_TRANSITION_ON_ROUTE=1   — move issue to target column after assign (default 1)
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Set

import requests
from dbx import DBX

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)

JIRA_SITE = "boltfoodops.atlassian.net"
JIRA_BASE = f"https://{JIRA_SITE}/rest/api/3"
PROJECT_KEY = "UAM"
DEFAULT_FALLBACK_DISPLAY_NAME = "Joanna Lizza Ayson"

# Default Jira status names (UAM board columns) — override via .env if your workflow uses different labels
DEFAULT_STATUS_SIMPLY2 = "SIMPLY_2PRIORITY"
DEFAULT_STATUS_MOPS = "MOPS TICKETS"

AM_JIRA_CACHE: Dict[str, Optional[str]] = {}


def _load_env() -> dict[str, str]:
    env_path = Path(__file__).parent / ".env"
    out: dict[str, str] = {}
    if not env_path.is_file():
        return out
    for line in env_path.read_text().splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


_ENV = _load_env()


def _env_bool(key: str, default: bool = False) -> bool:
    v = _ENV.get(key, os.environ.get(key, "")).strip().lower()
    if not v:
        return default
    return v in ("1", "true", "yes", "y")


def _env_int(key: str, default: int) -> int:
    v = _ENV.get(key, os.environ.get(key, "")).strip()
    if not v:
        return default
    try:
        return int(v)
    except ValueError:
        return default


def _build_status_in_jql() -> str:
    """Optional AND status in (...) from UAM_STATUS_IN (comma-separated names)."""
    raw = _ENV.get("UAM_STATUS_IN", os.environ.get("UAM_STATUS_IN", "")).strip()
    if not raw:
        return ""
    parts = [s.strip() for s in raw.split(",") if s.strip()]
    if not parts:
        return ""
    quoted: List[str] = []
    for p in parts:
        safe = p.replace("\\", "\\\\").replace('"', '\\"')
        quoted.append(f'"{safe}"')
    return " AND status in (" + ", ".join(quoted) + ")"


def resolve_fallback_account(session: requests.Session) -> tuple[str, str]:
    """
    Fallback when route owner or AM cannot be resolved.
    Returns (account_id, label for logs).
    """
    aid = _ENV.get("UAM_FALLBACK_ACCOUNT_ID", os.environ.get("UAM_FALLBACK_ACCOUNT_ID", "")).strip()
    name = (
        _ENV.get("UAM_FALLBACK_DISPLAY_NAME", os.environ.get("UAM_FALLBACK_DISPLAY_NAME", "")).strip()
        or DEFAULT_FALLBACK_DISPLAY_NAME
    )
    if aid:
        return aid, name
    jid = lookup_jira_account(session, name)
    if not jid:
        raise RuntimeError(
            f"Cannot resolve fallback assignee {name!r} in Jira user search. "
            f"Set UAM_FALLBACK_ACCOUNT_ID in .env to the user's Atlassian accountId."
        )
    return jid, name


def _load_jira_creds() -> tuple[str, str]:
    email = _ENV.get("JIRA_EMAIL", os.environ.get("JIRA_EMAIL", "")).strip()
    token = _ENV.get("JIRA_API_TOKEN", os.environ.get("JIRA_API_TOKEN", "")).strip()
    if not email or not token:
        raise RuntimeError(
            "Add JIRA_EMAIL and JIRA_API_TOKEN to .env\n"
            "Create token at https://id.atlassian.com/manage-profile/security/api-tokens"
        )
    return email, token


def jira_session() -> requests.Session:
    email, token = _load_jira_creds()
    s = requests.Session()
    s.auth = (email, token)
    s.headers["Accept"] = "application/json"
    s.headers["Content-Type"] = "application/json"
    return s


def adf_to_plain_text(node: Any) -> str:
    """Extract plain text from Jira description (Atlassian Document Format)."""
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    if isinstance(node, list):
        return "".join(adf_to_plain_text(x) for x in node)
    if isinstance(node, dict):
        parts: list[str] = []
        if "text" in node:
            parts.append(str(node["text"]))
        if "content" in node:
            parts.append(adf_to_plain_text(node["content"]))
        return "".join(parts)
    return ""


def description_to_text(raw: Any) -> str:
    if raw is None:
        return ""
    if isinstance(raw, str):
        return raw
    if isinstance(raw, dict):
        return adf_to_plain_text(raw.get("content") or raw)
    return str(raw)


def _sql_escape(s: str) -> str:
    return s.replace("'", "''")


def norm_status_name(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def classify_special_route(text: str) -> Optional[Literal["simply2", "mops"]]:
    """
    Legal / FOP changes → SIMPLY2 (Tetiana). Financial, Vchasno, invoices → MOPS (Anna).
    UA: summary/title phrases «ДУ припинення», «ДУ на зміну» → Tetiana (SIMPLY_2).
    Order: legal/FOP signals first, then financial/MOPS (to reduce false positives).
    """
    if not text or not str(text).strip():
        return None
    t = text.lower()

    # Додаткова угода (ДУ) у назві/описі — на Tetiana
    if "ду припинення" in t or "ду на зміну" in t:
        return "simply2"

    legal_fop = (
        bool(re.search(r"\b(фоп|fop)\b", t))
        or "legal entity" in t
        or "юридичн" in t
        or "зміна юридичної" in t
        or "зміна фоп" in t
        or "legal change" in t
        or "termination agreement" in t
        or "угода припинення" in t
        or "припинення співпраці" in t
        or "припинення договору" in t
        or "додаткова угода" in t
        or "additional agreement" in t
        or "simply_2" in t
        or "simply 2" in t
    )
    if legal_fop:
        return "simply2"

    mops_finance = (
        "vchasno" in t
        or "вчасно" in t
        or "invoice" in t
        or "інвойс" in t
        or "invoices" in t
        or "рахунок-фактура" in t
        or re.search(r"\bmops\b", t) is not None
        or "фінансов" in t
        or "payout" in t
        or "виплата" in t
        or "deduction" in t
        or "компенсація" in t
        or "акт звірки" in t
        or "iban" in t
        or "ібан" in t
        or "рахунок від" in t
    )
    if mops_finance:
        return "mops"

    return None


def get_current_status_name(fields: dict) -> str:
    st = fields.get("status")
    if isinstance(st, dict):
        return (st.get("name") or "").strip()
    return ""


def transition_issue_to_status(
    session: requests.Session,
    issue_key: str,
    target_status_name: str,
    dry_run: bool,
) -> bool:
    """Move issue to a workflow status (column) if a transition exists."""
    if not target_status_name.strip():
        return False
    url = f"{JIRA_BASE}/issue/{issue_key}/transitions"
    if dry_run:
        log.info("  [dry-run] would transition %s → %s", issue_key, target_status_name)
        return True
    resp = session.get(url)
    resp.raise_for_status()
    transitions = resp.json().get("transitions") or []
    want = norm_status_name(target_status_name)
    tid: Optional[str] = None
    for tr in transitions:
        to = tr.get("to") or {}
        to_name = norm_status_name((to.get("name") or ""))
        if to_name == want or want in to_name or to_name in want:
            tid = tr.get("id")
            break
    if not tid:
        log.warning(
            "No transition to status %r for %s (available to: %s)",
            target_status_name,
            issue_key,
            [(tr.get("to") or {}).get("name") for tr in transitions],
        )
        return False
    resp2 = session.post(url, json={"transition": {"id": tid}})
    if resp2.status_code in (200, 204):
        return True
    log.warning("Transition failed for %s: %s", issue_key, resp2.text)
    return False


def resolve_route_assignee(
    session: requests.Session, route: Literal["simply2", "mops"]
) -> tuple[Optional[str], str]:
    """Return (account_id, label) for Tetiana or Anna."""
    if route == "simply2":
        aid = _ENV.get("UAM_ACCOUNT_ID_TETIANA", os.environ.get("UAM_ACCOUNT_ID_TETIANA", "")).strip()
        label = "Tetiana Bondar (legal/FOP)"
        if aid:
            return aid, label
        name = _ENV.get(
            "UAM_DISPLAY_NAME_TETIANA",
            os.environ.get("UAM_DISPLAY_NAME_TETIANA", "Tetiana Bondar"),
        ).strip()
        return lookup_jira_account(session, name), label
    aid = _ENV.get("UAM_ACCOUNT_ID_ANNA", os.environ.get("UAM_ACCOUNT_ID_ANNA", "")).strip()
    label = "Anna Zaritska (MOPS/finance)"
    if aid:
        return aid, label
    name = _ENV.get(
        "UAM_DISPLAY_NAME_ANNA",
        os.environ.get("UAM_DISPLAY_NAME_ANNA", "Anna Zaritska"),
    ).strip()
    return lookup_jira_account(session, name), label


def fetch_unassigned_tickets(
    session: requests.Session,
    extra_jql: str,
    max_results: int,
    custom_field_id: Optional[str],
    max_age_days: int,
    status_in_jql: str,
) -> list[dict]:
    age_clause = ""
    if max_age_days > 0:
        age_clause = f" AND created >= -{max_age_days}d"
    jql = (
        f"project = {PROJECT_KEY} AND assignee is EMPTY AND status != Done "
        f"{age_clause}{status_in_jql}{extra_jql} ORDER BY created DESC"
    )
    fields: List[str] = ["summary", "description", "status"]
    if custom_field_id:
        fields.append(custom_field_id)

    url = f"{JIRA_BASE}/search/jql"
    body = {"jql": jql.strip(), "maxResults": max_results, "fields": fields}
    resp = session.post(url, json=body)
    resp.raise_for_status()
    return resp.json().get("issues", [])


def _parse_int_from_jira_field(val: Any) -> Optional[int]:
    if val is None:
        return None
    if isinstance(val, (int, float)) and val == int(val):
        return int(val)
    if isinstance(val, str) and val.strip().isdigit():
        return int(val.strip())
    if isinstance(val, dict):
        if "id" in val and str(val["id"]).isdigit():
            return int(val["id"])
    return None


def extract_provider_id_from_custom_field(fields: dict, field_id: Optional[str]) -> Optional[int]:
    if not field_id:
        return None
    val = fields.get(field_id)
    return _parse_int_from_jira_field(val)


_YEAR_RE = re.compile(r"^(202[0-9]|2030)$")


def extract_provider_id(summary: str, description: str) -> Optional[int]:
    """
    Prefer explicit labels, then first plausible 4–8 digit id (exclude obvious years).
    """
    combined = f"{summary}\n{description}"
    explicit = re.findall(
        r"(?i)(?:provider\s*id|provider|merchant\s*id|id)\s*[:=#]?\s*(\d{4,8})\b",
        combined,
    )
    for n in explicit:
        v = int(n)
        if _YEAR_RE.match(n):
            continue
        return v

    for text in (summary, description):
        nums = re.findall(r"\b(\d{4,8})\b", text or "")
        for n in nums:
            if _YEAR_RE.match(n):
                continue
            val = int(n)
            if 2020 <= val <= 2030 and len(n) == 4:
                continue
            return val
    return None


def candidate_restaurant_queries(summary: str) -> List[str]:
    """Build search phrases from summary when provider_id is missing."""
    s = (summary or "").strip()
    if "|" in s:
        s = s.split("|", 1)[-1].strip()
    elif " — " in s:
        s = s.split(" — ", 1)[-1].strip()
    elif " - " in s:
        tail = s.split(" - ", 1)[-1].strip()
        if len(tail) >= 3:
            s = tail
    s = re.sub(r"^\s*[A-Z][A-Z]+-\d+\s*", "", s)
    s = re.sub(r"[\[\(].*?[\]\)]", " ", s)
    words = [w for w in re.sub(r"[^\w\s\u0400-\u04FF]", " ", s).split() if len(w) >= 2]
    out: List[str] = []
    if len(words) >= 3:
        out.append(" ".join(words[:4]))
    if len(words) >= 2:
        out.append(" ".join(words[:2]))
    if words:
        out.append(words[0])
    seen: Set[str] = set()
    uniq: List[str] = []
    for q in out:
        q = q.strip()
        if len(q) >= 3 and q.lower() not in seen:
            seen.add(q.lower())
            uniq.append(q)
    return uniq[:6]


def batch_lookup_ams(provider_ids: list[int]) -> dict[int, Optional[str]]:
    if not provider_ids:
        return {}
    result: dict[int, Optional[str]] = {}
    chunk_size = 400
    for i in range(0, len(provider_ids), chunk_size):
        chunk = provider_ids[i : i + chunk_size]
        ids_str = ",".join(str(x) for x in chunk)
        sql = f"""
            SELECT provider_id, account_manager_name
            FROM ng_delivery_spark.dim_provider_v2
            WHERE provider_id IN ({ids_str})
              AND country_code = 'ua'
        """
        with DBX() as dbx:
            df = dbx.query(sql)
        for _, row in df.iterrows():
            am = row["account_manager_name"]
            result[int(row["provider_id"])] = am if am and str(am).strip() else None
    return result


def search_provider_by_name(name: str) -> Optional[str]:
    safe = _sql_escape(name.lower())
    sql = f"""
        SELECT account_manager_name
        FROM ng_delivery_spark.dim_provider_v2
        WHERE country_code = 'ua'
          AND LOWER(provider_name) LIKE '%{safe}%'
          AND account_manager_name IS NOT NULL
        LIMIT 1
    """
    try:
        with DBX() as dbx:
            df = dbx.query(sql)
        if not df.empty:
            return df.iloc[0]["account_manager_name"]
    except Exception as e:
        log.debug("search_provider_by_name failed for %r: %s", name, e)
    return None


def resolve_am_without_provider_id(summary: str) -> Optional[str]:
    for q in candidate_restaurant_queries(summary):
        am = search_provider_by_name(q)
        if am:
            return am
    return None


def _user_search(session: requests.Session, query: str, max_results: int = 20) -> list:
    if not query.strip():
        return []
    url = f"{JIRA_BASE}/user/search"
    resp = session.get(url, params={"query": query.strip(), "maxResults": max_results})
    resp.raise_for_status()
    return resp.json()


def lookup_jira_account(session: requests.Session, display_name: str) -> Optional[str]:
    if not display_name or not str(display_name).strip():
        return None
    dn = " ".join(str(display_name).split())
    if dn in AM_JIRA_CACHE:
        return AM_JIRA_CACHE[dn]

    users = _user_search(session, dn)
    dn_l = dn.lower()
    dn_norm = " ".join(dn_l.split())

    for u in users:
        d = (u.get("displayName") or "").strip()
        if d.lower() == dn_l or " ".join(d.lower().split()) == dn_norm:
            aid = u["accountId"]
            AM_JIRA_CACHE[dn] = aid
            return aid

    parts = dn.split()
    if len(parts) >= 2:
        users2 = _user_search(session, f"{parts[0]} {parts[-1]}")
        p0, pl = parts[0].lower(), parts[-1].lower()
        for u in users2:
            d = (u.get("displayName") or "").lower()
            if p0 in d and pl in d:
                aid = u["accountId"]
                AM_JIRA_CACHE[dn] = aid
                return aid

    sig = [p for p in parts if len(p) >= 2]
    if len(sig) >= 2:
        for u in users:
            d = (u.get("displayName") or "")
            dl = d.lower()
            if all(s.lower() in dl for s in sig):
                aid = u["accountId"]
                AM_JIRA_CACHE[dn] = aid
                return aid

    AM_JIRA_CACHE[dn] = None
    return None


def prefetch_jira_accounts(session: requests.Session, names: Set[str]) -> None:
    for n in sorted(names):
        if n and str(n).strip():
            lookup_jira_account(session, str(n).strip())


def assign_ticket(session: requests.Session, issue_key: str, account_id: str, dry_run: bool) -> bool:
    if dry_run:
        log.info("  [dry-run] would assign %s → accountId=%s", issue_key, account_id)
        return True
    url = f"{JIRA_BASE}/issue/{issue_key}/assignee"
    resp = session.put(url, data=json.dumps({"accountId": account_id}))
    if resp.status_code == 204:
        return True
    log.warning("Failed to assign %s to %s: %s", issue_key, account_id, resp.text)
    return False


def run() -> None:
    extra_jql = _ENV.get("UAM_AUTO_ASSIGN_EXTRA_JQL", os.environ.get("UAM_AUTO_ASSIGN_EXTRA_JQL", "")).strip()
    if extra_jql and not extra_jql.upper().startswith("AND"):
        extra_jql = " AND " + extra_jql
    max_issues = _env_int("UAM_MAX_ISSUES", 200)
    custom_field = _ENV.get("JIRA_CUSTOM_FIELD_PROVIDER", os.environ.get("JIRA_CUSTOM_FIELD_PROVIDER", "")).strip() or None
    dry_run = _env_bool("UAM_DRY_RUN", False)
    route_rules_enabled = _env_bool("UAM_ROUTE_RULES_ENABLED", True)
    transition_on_route = _env_bool("UAM_TRANSITION_ON_ROUTE", True)
    status_simply2 = (
        _ENV.get("UAM_STATUS_NAME_SIMPLY2", os.environ.get("UAM_STATUS_NAME_SIMPLY2", "")).strip()
        or DEFAULT_STATUS_SIMPLY2
    )
    status_mops = (
        _ENV.get("UAM_STATUS_NAME_MOPS", os.environ.get("UAM_STATUS_NAME_MOPS", "")).strip()
        or DEFAULT_STATUS_MOPS
    )
    skip_unknown = _env_bool("UAM_SKIP_UNKNOWN_ASSIGNEE", False)
    max_age_days = _env_int("UAM_MAX_TICKET_AGE_DAYS", 30)
    status_in_jql = _build_status_in_jql()

    log.info("=== UAM Auto-Assign started at %s ===", datetime.now().strftime("%Y-%m-%d %H:%M"))
    if dry_run:
        log.info("UAM_DRY_RUN=1 — no assignments will be made")
    if route_rules_enabled:
        log.info(
            "Route rules: Legal/FOP → %s + %s | Finance/Vchasno → %s + %s",
            status_simply2,
            "Tetiana",
            status_mops,
            "Anna",
        )
    if skip_unknown:
        log.info("UAM_SKIP_UNKNOWN_ASSIGNEE=1 — tickets without a resolved assignee will be skipped (no fallback)")
    if max_age_days > 0:
        log.info("Only tickets created in the last %d days (UAM_MAX_TICKET_AGE_DAYS)", max_age_days)
    else:
        log.info("UAM_MAX_TICKET_AGE_DAYS=0 — no filter on created date")
    if status_in_jql:
        log.info(
            "UAM_STATUS_IN — only these statuses:%s",
            _ENV.get("UAM_STATUS_IN", os.environ.get("UAM_STATUS_IN", "")).strip(),
        )
    session = jira_session()

    tickets = fetch_unassigned_tickets(
        session, extra_jql, max_issues, custom_field, max_age_days, status_in_jql
    )
    log.info(
        "Found %d unassigned tickets (excl. Done)%s%s%s",
        len(tickets),
        f" {extra_jql}" if extra_jql else "",
        f", created in last {max_age_days}d" if max_age_days > 0 else "",
        ", status allowlist" if status_in_jql else "",
    )
    if not tickets:
        log.info("Nothing to do.")
        return

    fallback_id, fallback_label = resolve_fallback_account(session)
    log.info("Fallback assignee when AM/route cannot be resolved: %s", fallback_label)

    ticket_data: List[dict[str, Any]] = []
    for issue in tickets:
        key = issue["key"]
        fields = issue["fields"]
        summary = fields.get("summary") or ""
        desc_text = description_to_text(fields.get("description"))
        pid = extract_provider_id_from_custom_field(fields, custom_field)
        if pid is None:
            pid = extract_provider_id(summary, desc_text)
        combined = f"{summary}\n{desc_text}"
        route = classify_special_route(combined) if route_rules_enabled else None
        current_status = get_current_status_name(fields)
        ticket_data.append(
            {
                "key": key,
                "summary": summary,
                "desc": desc_text,
                "provider_id": pid,
                "route": route,
                "current_status": current_status,
            }
        )

    provider_ids = [t["provider_id"] for t in ticket_data if t["provider_id"]]
    unique_ids = list(dict.fromkeys(provider_ids))
    log.info("Querying Databricks for %d unique provider IDs...", len(unique_ids))
    am_map = batch_lookup_ams(unique_ids)

    am_names: Set[str] = set()
    for t in ticket_data:
        pid = t["provider_id"]
        am_name: Optional[str] = am_map.get(pid) if pid else None
        if not am_name:
            am_name = resolve_am_without_provider_id(t["summary"])
        t["am_name"] = am_name
        if am_name:
            am_names.add(str(am_name).strip())

    prefetch_targets: Set[str] = set(am_names)
    if route_rules_enabled:
        prefetch_targets.add(
            _ENV.get(
                "UAM_DISPLAY_NAME_TETIANA",
                os.environ.get("UAM_DISPLAY_NAME_TETIANA", "Tetiana Bondar"),
            ).strip()
        )
        prefetch_targets.add(
            _ENV.get(
                "UAM_DISPLAY_NAME_ANNA",
                os.environ.get("UAM_DISPLAY_NAME_ANNA", "Anna Zaritska"),
            ).strip()
        )
    prefetch_targets.add(fallback_label)

    log.info("Prefetching %d unique Jira users...", len(prefetch_targets))
    prefetch_jira_accounts(session, prefetch_targets)

    assigned = 0
    fallback_n = 0
    skipped_n = 0
    for t in ticket_data:
        key = t["key"]
        pid = t["provider_id"]
        route = t["route"]
        cur_st = t["current_status"]

        am_name: Optional[str] = t.get("am_name")

        account_id: Optional[str] = None
        who = ""
        target_transition: Optional[str] = None
        used_fallback_assignee = False

        if route == "simply2":
            aid, who = resolve_route_assignee(session, "simply2")
            if aid:
                account_id = aid
                target_transition = status_simply2
            elif skip_unknown:
                log.info("  %s → SKIP (Legal/FOP — Tetiana not found in Jira) [provider %s]", key, pid or "?")
                skipped_n += 1
                continue
            else:
                log.warning("%s: classified as Legal/FOP but Tetiana not found in Jira — using AM", key)
        elif route == "mops":
            aid, who = resolve_route_assignee(session, "mops")
            if aid:
                account_id = aid
                target_transition = status_mops
            elif skip_unknown:
                log.info("  %s → SKIP (MOPS — Anna not found in Jira) [provider %s]", key, pid or "?")
                skipped_n += 1
                continue
            else:
                log.warning("%s: classified as MOPS/finance but Anna not found in Jira — using AM", key)

        if not account_id:
            jira_id: Optional[str] = None
            if am_name:
                jira_id = lookup_jira_account(session, am_name)
            if jira_id:
                account_id = jira_id
                who = am_name or "AM"
                target_transition = None
            elif skip_unknown:
                if am_name:
                    log.info(
                        "  %s → SKIP (AM %r — no Jira user match) [provider %s]",
                        key,
                        am_name,
                        pid or "?",
                    )
                else:
                    log.info("  %s → SKIP (no account_manager in data / name match) [provider %s]", key, pid or "?")
                skipped_n += 1
                continue
            else:
                account_id = fallback_id
                who = f"{fallback_label} (fallback)"
                used_fallback_assignee = True
                target_transition = None

        ok = assign_ticket(session, key, account_id, dry_run)
        if ok:
            assigned += 1
            if used_fallback_assignee:
                fallback_n += 1
            log.info("  %s → %s  [provider %s]", key, who, pid or "?")
        else:
            if skip_unknown:
                log.warning("%s: assign failed, not using fallback (skip-unknown mode)", key)
            elif account_id != fallback_id:
                if assign_ticket(session, key, fallback_id, dry_run):
                    assigned += 1
                    fallback_n += 1
                    log.info("  %s → fallback (previous assignee no permissions)", key)

        if (
            ok
            and transition_on_route
            and target_transition
            and norm_status_name(cur_st) != norm_status_name(target_transition)
        ):
            if transition_issue_to_status(session, key, target_transition, dry_run):
                log.info("  %s → column/status %s", key, target_transition)

    log.info("=== Done: %d assigned (%d fallback), %d skipped ===", assigned, fallback_n, skipped_n)


if __name__ == "__main__":
    run()
