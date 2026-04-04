"""JSON-based state persistence + CSV log for approved submissions."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone

from config import STATE_FILE, APPROVED_CSV, DATA_DIR


def _ensure_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ── State I/O ───────────────────────────────────────────────────────

def load_state() -> dict:
    _ensure_dir()
    if STATE_FILE.is_file():
        state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        state.setdefault("sticker_requests", [])
        return state
    return {"update_offset": 0, "sessions": {}, "submissions": [], "sticker_requests": []}


def save_state(state: dict):
    _ensure_dir()
    STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ── Session (per-chat conversation state) ───────────────────────────

def get_session(state, chat_id) -> dict | None:
    return state["sessions"].get(str(chat_id))


def set_session(state, chat_id, data: dict):
    state["sessions"][str(chat_id)] = data


def clear_session(state, chat_id):
    state["sessions"].pop(str(chat_id), None)


# ── Submissions ─────────────────────────────────────────────────────

def add_submission(state, *, chat_id, provider_id, provider_name, city,
                   photo_file_id, username) -> dict:
    sub_id = f"sub_{len(state['submissions']) + 1:04d}"
    sub = {
        "id": sub_id,
        "chat_id": chat_id,
        "provider_id": str(provider_id),
        "provider_name": provider_name,
        "city": city,
        "photo_file_id": photo_file_id,
        "username": username,
        "submitted_at": _now_iso(),
        "status": "pending",
        "reviewed_at": None,
        "admin_message_id": None,
    }
    state["submissions"].append(sub)
    return sub


def find_submission(state, sub_id) -> dict | None:
    for s in state["submissions"]:
        if s["id"] == sub_id:
            return s
    return None


def provider_submission_status(state, provider_id: str) -> str | None:
    """Check if provider_id already has a submission.

    Returns the most relevant status:
      'approved' — already approved (block resubmission)
      'pending'  — waiting for review
      None       — no active submission (OK to proceed)
    """
    pid = str(provider_id)
    has_pending = False
    for s in state["submissions"]:
        if s["provider_id"] != pid:
            continue
        if s["status"] == "approved":
            return "approved"
        if s["status"] == "pending":
            has_pending = True
    return "pending" if has_pending else None


def add_sticker_request(state, *, chat_id, provider_id, provider_name,
                        city, phone, recipient, nova_poshta, username) -> dict:
    req = {
        "id": f"stk_{len(state['sticker_requests']) + 1:04d}",
        "chat_id": chat_id,
        "provider_id": str(provider_id),
        "provider_name": provider_name,
        "city": city,
        "recipient": recipient,
        "phone": phone,
        "nova_poshta": nova_poshta,
        "username": username,
        "created_at": _now_iso(),
        "status": "pending_delivery",
    }
    state["sticker_requests"].append(req)
    return req


def mark_submission(state, sub_id, status: str) -> dict | None:
    sub = find_submission(state, sub_id)
    if not sub:
        return None
    sub["status"] = status
    sub["reviewed_at"] = _now_iso()
    if status == "approved":
        _append_csv(sub)
    return sub


def _append_csv(sub: dict):
    _ensure_dir()
    write_header = not APPROVED_CSV.is_file()
    with open(APPROVED_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow([
                "submission_id", "provider_id", "provider_name", "city",
                "partner_chat_id", "partner_username",
                "submitted_at", "approved_at", "promo_status",
            ])
        w.writerow([
            sub["id"], sub["provider_id"], sub["provider_name"], sub["city"],
            sub["chat_id"], sub["username"],
            sub["submitted_at"], sub["reviewed_at"], "pending_promo",
        ])
