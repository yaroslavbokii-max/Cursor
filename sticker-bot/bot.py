#!/usr/bin/env python3
"""
Sticker verification Telegram bot.

Modes:
  python bot.py           — continuous polling (local dev)
  python bot.py --once    — single poll cycle (GitHub Actions cron)
"""

from __future__ import annotations

import json
import logging
import sys
import time

import requests

from config import (
    TELEGRAM_BOT_TOKEN, ADMIN_CHAT_ID,
    DATABRICKS_TOKEN, DATABRICKS_HOST, DATABRICKS_HTTP_PATH,
    MSG,
)
from storage import (
    load_state, save_state,
    get_session, set_session, clear_session,
    add_submission, find_submission, mark_submission,
    provider_submission_status,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
)
log = logging.getLogger("sticker-bot")

API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


# ── Telegram API helpers ────────────────────────────────────────────

def tg(method: str, **kwargs):
    payload = {k: v for k, v in kwargs.items() if v is not None}
    resp = requests.post(f"{API}/{method}", json=payload, timeout=30).json()
    if not resp.get("ok"):
        log.error("Telegram %s failed: %s", method, resp.get("description"))
    return resp


def _esc(text: str) -> str:
    """Escape Markdown special characters in user-provided values."""
    for ch in ("_", "*", "`", "["):
        text = text.replace(ch, f"\\{ch}")
    return text


def send_msg(chat_id, text, **kw):
    return tg("sendMessage", chat_id=chat_id, text=text,
              parse_mode="Markdown", **kw)


def send_photo(chat_id, photo, caption=None, **kw):
    return tg("sendPhoto", chat_id=chat_id, photo=photo,
              caption=caption, parse_mode="Markdown", **kw)


def answer_cb(callback_query_id, text=""):
    tg("answerCallbackQuery", callback_query_id=callback_query_id, text=text)


def get_updates(offset=0, timeout=5):
    try:
        r = requests.get(
            f"{API}/getUpdates",
            params={"offset": offset, "timeout": timeout},
            timeout=timeout + 10,
        )
        r.raise_for_status()
        return r.json().get("result", [])
    except Exception as e:
        log.error("getUpdates failed: %s", e)
        return []


# ── Databricks provider lookup ──────────────────────────────────────

def lookup_provider(pid: str) -> dict | None:
    if not DATABRICKS_TOKEN:
        return None
    try:
        from databricks import sql as dbsql

        conn = dbsql.connect(
            server_hostname=DATABRICKS_HOST,
            http_path=DATABRICKS_HTTP_PATH,
            access_token=DATABRICKS_TOKEN,
        )
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT provider_id, provider_name, country_code, city_id "
                    "FROM ng_delivery_spark.dim_provider_v2 "
                    f"WHERE provider_id = {int(pid)} AND country_code = 'ua' "
                    "LIMIT 1"
                )
                row = cur.fetchone()
                if row:
                    cols = [d[0] for d in cur.description]
                    return dict(zip(cols, row))
        finally:
            conn.close()
    except Exception as e:
        log.warning("Databricks lookup failed: %s", e)
    return None


# ── Update routing ──────────────────────────────────────────────────

def process_update(update: dict, state: dict):
    if "callback_query" in update:
        _handle_callback(update["callback_query"], state)
        return

    msg = update.get("message")
    if not msg:
        return

    chat_id = msg["chat"]["id"]
    text = (msg.get("text") or "").strip()

    if text == "/start":
        set_session(state, chat_id, {"step": "awaiting_provider_id"})
        send_msg(chat_id, MSG["welcome"])
        return

    if text == "/myid":
        send_msg(chat_id, MSG["myid"].format(chat_id=chat_id))
        return

    if text == "/status":
        _handle_status(chat_id, state)
        return

    session = get_session(state, chat_id)
    if not session:
        send_msg(chat_id, "Натисніть /start щоб розпочати.")
        return

    step = session.get("step")

    if step == "awaiting_provider_id":
        _handle_provider_id(chat_id, text, session, state)
    elif step == "awaiting_photo":
        if "photo" in msg:
            _handle_photo(msg, session, state)
        else:
            send_msg(chat_id, MSG["send_photo"])
    elif step == "submitted":
        send_msg(chat_id, MSG["already_submitted"])


# ── Step handlers ───────────────────────────────────────────────────

def _handle_provider_id(chat_id, text, session, state):
    pid = text.strip()
    if not pid.isdigit():
        send_msg(chat_id, "Provider ID має бути числом. Спробуйте ще раз:")
        return

    # Anti-fraud: check if this provider already has a submission
    existing = provider_submission_status(state, pid)
    if existing == "approved":
        send_msg(chat_id, MSG["already_approved"].format(pid=pid))
        clear_session(state, chat_id)
        return
    if existing == "pending":
        send_msg(chat_id, MSG["already_pending"].format(pid=pid))
        clear_session(state, chat_id)
        return

    provider = lookup_provider(pid)

    if provider:
        session.update({
            "step": "awaiting_photo",
            "provider_id": pid,
            "provider_name": provider.get("provider_name", "—"),
            "city": str(provider.get("city_id", "—")),
        })
        set_session(state, chat_id, session)
        send_msg(chat_id, MSG["provider_found"].format(
            name=session["provider_name"], city=session["city"],
        ))
    elif DATABRICKS_TOKEN:
        send_msg(chat_id, MSG["provider_not_found"].format(pid=pid))
    else:
        # No Databricks — accept any numeric ID
        session.update({
            "step": "awaiting_photo",
            "provider_id": pid,
            "provider_name": "—",
            "city": "—",
        })
        set_session(state, chat_id, session)
        send_msg(chat_id, MSG["provider_accepted"].format(pid=pid))


def _handle_photo(msg, session, state):
    chat_id = msg["chat"]["id"]
    photo_file_id = msg["photo"][-1]["file_id"]

    username = msg["from"].get("username", "")
    first_name = msg["from"].get("first_name", "")
    display = f"@{username}" if username else first_name

    sub = add_submission(
        state,
        chat_id=chat_id,
        provider_id=session["provider_id"],
        provider_name=session["provider_name"],
        city=session["city"],
        photo_file_id=photo_file_id,
        username=display,
    )

    session["step"] = "submitted"
    set_session(state, chat_id, session)
    send_msg(chat_id, MSG["photo_received"])
    _notify_admin(sub)


def _notify_admin(sub):
    if not ADMIN_CHAT_ID:
        log.warning("ADMIN_CHAT_ID not set — cannot forward to admin")
        return

    caption = MSG["admin_new"].format(
        provider_id=sub["provider_id"],
        provider_name=_esc(sub["provider_name"]),
        city=_esc(sub["city"]),
        username=_esc(sub["username"]),
        time=sub["submitted_at"][:16].replace("T", " "),
    )

    keyboard = {"inline_keyboard": [[
        {"text": "✅ Approve", "callback_data": f"approve:{sub['id']}"},
        {"text": "❌ Reject",  "callback_data": f"reject:{sub['id']}"},
    ]]}

    log.info("Sending admin notification for %s to chat %s", sub["id"], ADMIN_CHAT_ID)
    result = send_photo(
        ADMIN_CHAT_ID,
        sub["photo_file_id"],
        caption=caption,
        reply_markup=keyboard,
    )
    if result.get("ok"):
        sub["admin_message_id"] = result["result"]["message_id"]
        log.info("Admin notified, message_id=%s", sub["admin_message_id"])
    else:
        log.error("Admin notification failed: %s", result)


# ── Admin callback ──────────────────────────────────────────────────

def _handle_callback(cb, state):
    data = cb.get("data", "")
    cb_id = cb["id"]

    if ":" not in data:
        answer_cb(cb_id, "Unknown action")
        return

    action, sub_id = data.split(":", 1)
    sub = find_submission(state, sub_id)

    if not sub:
        answer_cb(cb_id, "Заявку не знайдено")
        return

    if sub["status"] != "pending":
        answer_cb(cb_id, f"Вже оброблено: {sub['status']}")
        return

    admin_chat = cb["message"]["chat"]["id"]

    if action == "approve":
        mark_submission(state, sub_id, "approved")
        answer_cb(cb_id, "Approved ✅")
        send_msg(sub["chat_id"], MSG["approved"])
        send_msg(
            admin_chat,
            f"✅ *Approved*: `{sub['provider_id']}` — {_esc(sub['provider_name'])}\n"
            f"Записано в approved.csv",
        )
        clear_session(state, sub["chat_id"])

    elif action == "reject":
        mark_submission(state, sub_id, "rejected")
        answer_cb(cb_id, "Rejected ❌")
        send_msg(sub["chat_id"], MSG["rejected"])
        send_msg(
            admin_chat,
            f"❌ *Rejected*: `{sub['provider_id']}` — {_esc(sub['provider_name'])}",
        )
        clear_session(state, sub["chat_id"])


# ── /status command ─────────────────────────────────────────────────

def _handle_status(chat_id, state):
    subs = state["submissions"]
    pending  = sum(1 for s in subs if s["status"] == "pending")
    approved = sum(1 for s in subs if s["status"] == "approved")
    rejected = sum(1 for s in subs if s["status"] == "rejected")

    send_msg(chat_id, (
        "📊 *Статус заявок*\n\n"
        f"Очікують перевірки: {pending}\n"
        f"Підтверджено: {approved}\n"
        f"Відхилено: {rejected}\n"
        f"Всього: {len(subs)}"
    ))


# ── Main ────────────────────────────────────────────────────────────

def run_once():
    state = load_state()
    offset = state.get("update_offset", 0)

    updates = get_updates(offset=offset, timeout=1)
    if not updates:
        log.info("No new updates")
        save_state(state)
        return

    log.info("Processing %d update(s)", len(updates))
    for upd in updates:
        try:
            process_update(upd, state)
        except Exception as e:
            log.error("Error on update %s: %s", upd.get("update_id"), e)
        state["update_offset"] = upd["update_id"] + 1

    save_state(state)
    log.info("Done — state saved")


def run_polling():
    log.info("Polling started (Ctrl+C to stop) …")
    state = load_state()

    while True:
        try:
            offset = state.get("update_offset", 0)
            updates = get_updates(offset=offset, timeout=30)

            for upd in updates:
                try:
                    process_update(upd, state)
                except Exception as e:
                    log.error("Error on update %s: %s", upd.get("update_id"), e)
                state["update_offset"] = upd["update_id"] + 1

            save_state(state)

        except KeyboardInterrupt:
            log.info("Shutting down …")
            save_state(state)
            break
        except Exception as e:
            log.error("Polling error: %s — retrying in 5 s", e)
            time.sleep(5)


if __name__ == "__main__":
    if not TELEGRAM_BOT_TOKEN:
        sys.exit("ERROR: TELEGRAM_BOT_TOKEN not set. See .env.example")

    if "--once" in sys.argv:
        run_once()
    else:
        run_polling()
