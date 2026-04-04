#!/usr/bin/env python3
"""
Sticker verification Telegram bot.

Modes:
  python bot.py              — continuous polling (local dev)
  python bot.py --once       — single poll cycle (GitHub Actions cron)
  python bot.py --webhook    — webhook server (Render / production)
"""

from __future__ import annotations

import json
import logging
import os
import sys
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

import requests

from config import (
    TELEGRAM_BOT_TOKEN, ADMIN_CHAT_ID,
    DATABRICKS_TOKEN, DATABRICKS_HOST, DATABRICKS_HTTP_PATH,
    WEBHOOK_URL, MSG, CITIES,
)
from storage import (
    load_state, save_state,
    get_session, set_session, clear_session,
    add_submission, find_submission, mark_submission,
    provider_submission_status, add_sticker_request,
)
from nova_poshta import list_warehouses, TYPE_POSTOMAT, TYPE_BRANCH, PAGE_SIZE
import math

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
)
log = logging.getLogger("sticker-bot")

API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

_np_cache: dict[int, list[dict]] = {}


# ── Telegram API helpers ────────────────────────────────────────────

def tg(method: str, **kwargs):
    payload = {k: v for k, v in kwargs.items() if v is not None}
    resp = requests.post(f"{API}/{method}", json=payload, timeout=30).json()
    if not resp.get("ok"):
        log.error("Telegram %s failed: %s", method, resp.get("description"))
    return resp


def _esc(text: str) -> str:
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


_poll_backoff = 0

def get_updates(offset=0, timeout=5):
    global _poll_backoff
    try:
        r = requests.get(
            f"{API}/getUpdates",
            params={"offset": offset, "timeout": timeout},
            timeout=timeout + 10,
        )
        r.raise_for_status()
        _poll_backoff = 0
        return r.json().get("result", [])
    except Exception as e:
        _poll_backoff = min(_poll_backoff + 1, 6)
        wait = 2 ** _poll_backoff
        log.error("getUpdates failed (retry in %ds): %s", wait, e)
        time.sleep(wait)
        return []


def set_webhook(url: str):
    if url:
        resp = tg("setWebhook", url=url)
        log.info("setWebhook → %s", resp.get("description", resp))
    else:
        tg("deleteWebhook")
        log.info("Webhook deleted (polling mode)")


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
                    "SELECT provider_id, provider_name, city_name, zone_name "
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
        set_session(state, chat_id, {"step": "ask_has_sticker"})
        keyboard = {"inline_keyboard": [[
            {"text": "Так, є стікер ✅", "callback_data": "has_sticker:yes"},
            {"text": "Ні, потрібен 📦", "callback_data": "has_sticker:no"},
        ]]}
        send_msg(chat_id, MSG["welcome"])
        send_msg(chat_id, MSG["has_sticker_question"], reply_markup=keyboard)
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
    elif step == "need_sticker_pid":
        _handle_need_sticker_pid(chat_id, text, session, state)
    elif step == "need_sticker_city_other":
        _handle_need_sticker_city_text(chat_id, text, session, state)
    elif step == "need_sticker_phone":
        _handle_need_sticker_phone(chat_id, text, session, state)
    elif step == "need_sticker_recipient":
        _handle_need_sticker_recipient(chat_id, text, session, state)
    elif step == "need_sticker_np_search":
        _handle_np_text_search(chat_id, text, session, state)
    elif step == "need_sticker_np_manual":
        _handle_need_sticker_np_manual(chat_id, text, session, state)


# ── Step handlers ───────────────────────────────────────────────────

def _handle_provider_id(chat_id, text, session, state):
    pid = text.strip()
    if not pid.isdigit():
        send_msg(chat_id, "Provider ID має бути числом. Спробуйте ще раз:")
        return

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
            "step": "confirm_provider",
            "flow": "verify",
            "provider_id": pid,
            "provider_name": provider.get("provider_name", "—"),
            "city": provider.get("city_name", "—"),
            "zone": provider.get("zone_name", "—"),
        })
        set_session(state, chat_id, session)
        keyboard = {"inline_keyboard": [[
            {"text": "Так, це мій заклад ✅", "callback_data": "confirm_pid:yes"},
            {"text": "Ні, інший ❌", "callback_data": "confirm_pid:no"},
        ]]}
        send_msg(chat_id, MSG["provider_confirm"].format(
            name=_esc(session["provider_name"]),
            city=_esc(session["city"]),
            zone=_esc(session["zone"]),
        ), reply_markup=keyboard)
    elif DATABRICKS_TOKEN:
        send_msg(chat_id, MSG["provider_not_found"].format(pid=pid))
    else:
        session.update({
            "step": "awaiting_photo",
            "provider_id": pid,
            "provider_name": "—",
            "city": "—",
            "zone": "—",
        })
        set_session(state, chat_id, session)
        send_msg(chat_id, MSG["send_photo"])


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


# ── "Need sticker" flow ─────────────────────────────────────────────
# Steps: provider_id → city → phone → nova poshta branch → done

def _send_city_keyboard(chat_id):
    rows = []
    for i in range(0, len(CITIES), 2):
        row = [{"text": CITIES[i], "callback_data": f"city:{CITIES[i]}"}]
        if i + 1 < len(CITIES):
            row.append({"text": CITIES[i + 1], "callback_data": f"city:{CITIES[i + 1]}"})
        rows.append(row)
    rows.append([{"text": "Інше місто ✏️", "callback_data": "city:__other__"}])
    send_msg(chat_id, MSG["need_sticker_city"],
             reply_markup={"inline_keyboard": rows})


def _handle_need_sticker_pid(chat_id, text, session, state):
    pid = text.strip()
    if not pid.isdigit():
        send_msg(chat_id, "Provider ID має бути числом. Спробуйте ще раз:")
        return

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
            "step": "confirm_provider",
            "flow": "sticker",
            "provider_id": pid,
            "provider_name": provider.get("provider_name", "—"),
            "city": provider.get("city_name", "—"),
            "zone": provider.get("zone_name", "—"),
        })
        set_session(state, chat_id, session)
        keyboard = {"inline_keyboard": [[
            {"text": "Так, це мій заклад ✅", "callback_data": "confirm_pid:yes"},
            {"text": "Ні, інший ❌", "callback_data": "confirm_pid:no"},
        ]]}
        send_msg(chat_id, MSG["provider_confirm"].format(
            name=_esc(session["provider_name"]),
            city=_esc(session["city"]),
            zone=_esc(session["zone"]),
        ), reply_markup=keyboard)
    elif DATABRICKS_TOKEN:
        send_msg(chat_id, MSG["provider_not_found"].format(pid=pid))
    else:
        session.update({
            "provider_id": pid,
            "provider_name": "—",
            "step": "need_sticker_city",
        })
        set_session(state, chat_id, session)
        _send_city_keyboard(chat_id)


def _handle_need_sticker_city_text(chat_id, text, session, state):
    city = text.strip()
    if len(city) < 2:
        send_msg(chat_id, "Будь ласка, введіть назву міста:")
        return
    session["city"] = city
    _send_np_type_keyboard(chat_id, session, state)


def _send_np_type_keyboard(chat_id, session, state):
    session["step"] = "need_sticker_np_type"
    set_session(state, chat_id, session)
    keyboard = {"inline_keyboard": [[
        {"text": "Поштомат 📦", "callback_data": "nptype:postomat"},
        {"text": "Відділення 🏤", "callback_data": "nptype:branch"},
    ]]}
    send_msg(chat_id, MSG["need_sticker_np_type"], reply_markup=keyboard)


def _handle_need_sticker_phone(chat_id, text, session, state):
    phone = text.strip().replace(" ", "").replace("-", "")
    if len(phone) < 10:
        send_msg(chat_id, "Введіть коректний номер телефону (мінімум 10 цифр):")
        return
    session["phone"] = phone
    session["step"] = "need_sticker_recipient"
    set_session(state, chat_id, session)
    send_msg(chat_id, MSG["need_sticker_recipient"])


def _handle_need_sticker_recipient(chat_id, text, session, state):
    name = text.strip()
    if len(name) < 3 or " " not in name:
        send_msg(chat_id, "Введіть *ім'я та прізвище* (наприклад, Іван Петренко):")
        return
    session["recipient"] = name
    _finish_sticker_request(chat_id, session.get("np_selected", "—"), session, state)


# ── NP warehouse list with pagination ──────────────────────────────

def _send_np_page(chat_id, session, state, page: int = 1, query: str = ""):
    city = session.get("city", "")
    wh_type = session.get("np_type_ref")
    warehouses, total = list_warehouses(city, wh_type, page=page, query=query)

    if not warehouses:
        rows = [
            [{"text": "🔍 Пошук за номером/адресою", "callback_data": "np:__search__"}],
            [{"text": "✏️ Ввести вручну", "callback_data": "np:__manual__"}],
        ]
        send_msg(chat_id, MSG["need_sticker_np_empty"],
                 reply_markup={"inline_keyboard": rows})
        return

    total_pages = max(1, math.ceil(total / PAGE_SIZE))
    _np_cache[chat_id] = warehouses
    session["np_page"] = page
    session["np_query"] = query
    set_session(state, chat_id, session)

    rows = []
    for i, w in enumerate(warehouses):
        label = w["short"]
        if len(label) > 45:
            label = label[:42] + "…"
        rows.append([{"text": label, "callback_data": f"np:{i}"}])

    nav_row = []
    if page > 1:
        nav_row.append({"text": "⬅️ Назад", "callback_data": f"nppage:{page - 1}"})
    if page < total_pages:
        nav_row.append({"text": "Далі ➡️", "callback_data": f"nppage:{page + 1}"})
    if nav_row:
        rows.append(nav_row)

    rows.append([
        {"text": "🔍 Пошук", "callback_data": "np:__search__"},
        {"text": "✏️ Вручну", "callback_data": "np:__manual__"},
    ])

    header = MSG["need_sticker_np_list"].format(
        page=page, pages=total_pages, total=total)
    send_msg(chat_id, header, reply_markup={"inline_keyboard": rows})


def _handle_np_text_search(chat_id, text, session, state):
    query = text.strip()
    if not query:
        send_msg(chat_id, "Введіть номер або частину адреси:")
        return
    _send_np_page(chat_id, session, state, page=1, query=query)


def _handle_need_sticker_np_manual(chat_id, text, session, state):
    np_branch = text.strip()
    if len(np_branch) < 3:
        send_msg(chat_id, "Будь ласка, вкажіть відділення Нової Пошти:")
        return
    session["np_selected"] = np_branch
    session["step"] = "need_sticker_phone"
    set_session(state, chat_id, session)
    send_msg(chat_id, MSG["need_sticker_phone"])


def _finish_sticker_request(chat_id, nova_poshta, session, state):
    _np_cache.pop(chat_id, None)
    username = session.get("username", "—")
    req = add_sticker_request(
        state,
        chat_id=chat_id,
        provider_id=session["provider_id"],
        provider_name=session.get("provider_name", "—"),
        city=session.get("city", "—"),
        phone=session.get("phone", "—"),
        recipient=session.get("recipient", "—"),
        nova_poshta=nova_poshta,
        username=username,
    )

    clear_session(state, chat_id)
    send_msg(chat_id, MSG["sticker_request_sent"])
    _notify_admin_sticker_request(req)


def _notify_admin_sticker_request(req):
    if not ADMIN_CHAT_ID:
        return

    text = MSG["admin_sticker_request"].format(
        provider_id=req["provider_id"],
        provider_name=_esc(req["provider_name"]),
        city=_esc(req["city"]),
        recipient=_esc(req.get("recipient", "—")),
        phone=_esc(req["phone"]),
        nova_poshta=_esc(req["nova_poshta"]),
        username=_esc(req["username"]),
        time=req["created_at"][:16].replace("T", " "),
    )
    send_msg(ADMIN_CHAT_ID, text)


# ── Admin callback ──────────────────────────────────────────────────

def _handle_callback(cb, state):
    data = cb.get("data", "")
    cb_id = cb["id"]
    chat_id = cb["message"]["chat"]["id"]

    # "Has sticker?" buttons
    if data.startswith("has_sticker:"):
        answer = data.split(":", 1)[1]
        answer_cb(cb_id)
        session = get_session(state, chat_id)
        if not session:
            return

        username_raw = cb["from"].get("username", "")
        first_name = cb["from"].get("first_name", "")
        session["username"] = f"@{username_raw}" if username_raw else first_name

        if answer == "yes":
            session["step"] = "awaiting_provider_id"
            set_session(state, chat_id, session)
            send_msg(chat_id, MSG["enter_provider_id"])
        else:
            session["step"] = "need_sticker_pid"
            set_session(state, chat_id, session)
            send_msg(chat_id, MSG["need_sticker"])
        return

    # Provider confirmation buttons
    if data.startswith("confirm_pid:"):
        answer = data.split(":", 1)[1]
        answer_cb(cb_id)
        session = get_session(state, chat_id)
        if not session:
            return

        if answer == "yes":
            flow = session.get("flow", "verify")
            if flow == "sticker":
                session["step"] = "need_sticker_city"
                set_session(state, chat_id, session)
                _send_city_keyboard(chat_id)
            else:
                session["step"] = "awaiting_photo"
                set_session(state, chat_id, session)
                send_msg(chat_id, MSG["send_photo"])
        else:
            flow = session.get("flow", "verify")
            if flow == "sticker":
                session["step"] = "need_sticker_pid"
            else:
                session["step"] = "awaiting_provider_id"
            set_session(state, chat_id, session)
            send_msg(chat_id, MSG["provider_wrong"])
        return

    # City selection buttons
    if data.startswith("city:"):
        city = data.split(":", 1)[1]
        answer_cb(cb_id)
        session = get_session(state, chat_id)
        if not session:
            return

        if city == "__other__":
            session["step"] = "need_sticker_city_other"
            set_session(state, chat_id, session)
            send_msg(chat_id, MSG["need_sticker_city_other"])
        else:
            session["city"] = city
            _send_np_type_keyboard(chat_id, session, state)
        return

    # NP type selection (postomat / branch)
    if data.startswith("nptype:"):
        choice = data.split(":", 1)[1]
        answer_cb(cb_id)
        session = get_session(state, chat_id)
        if not session:
            return

        session["np_type_ref"] = TYPE_POSTOMAT if choice == "postomat" else TYPE_BRANCH
        set_session(state, chat_id, session)
        _send_np_page(chat_id, session, state, page=1)
        return

    # NP pagination
    if data.startswith("nppage:"):
        page = int(data.split(":", 1)[1])
        answer_cb(cb_id)
        session = get_session(state, chat_id)
        if not session:
            return
        query = session.get("np_query", "")
        _send_np_page(chat_id, session, state, page=page, query=query)
        return

    # Nova Poshta warehouse selection buttons
    if data.startswith("np:"):
        choice = data.split(":", 1)[1]
        answer_cb(cb_id)
        session = get_session(state, chat_id)
        if not session:
            return

        if choice == "__search__":
            session["step"] = "need_sticker_np_search"
            set_session(state, chat_id, session)
            send_msg(chat_id,
                     "🔍 Введіть *номер* або *частину адреси* відділення:")
        elif choice == "__manual__":
            session["step"] = "need_sticker_np_manual"
            set_session(state, chat_id, session)
            send_msg(chat_id, MSG["need_sticker_np_fallback"])
        else:
            idx = int(choice)
            results = _np_cache.get(chat_id, [])
            if idx < len(results):
                session["np_selected"] = results[idx]["description"]
                session["step"] = "need_sticker_phone"
                set_session(state, chat_id, session)
                _np_cache.pop(chat_id, None)
                send_msg(chat_id, MSG["need_sticker_phone"])
            else:
                send_msg(chat_id, "Помилка вибору. Спробуйте /start")
        return

    # Approve / Reject buttons
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
    sticker_reqs = len(state.get("sticker_requests", []))

    send_msg(chat_id, (
        "📊 *Статус заявок*\n\n"
        f"Очікують перевірки: {pending}\n"
        f"Підтверджено: {approved}\n"
        f"Відхилено: {rejected}\n"
        f"Запити на стікер: {sticker_reqs}\n"
        f"Всього заявок: {len(subs)}"
    ))


# ── Webhook server ──────────────────────────────────────────────────

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        self.send_response(200)
        self.end_headers()

        try:
            update = json.loads(body)
            state = load_state()
            process_update(update, state)
            save_state(state)
        except Exception as e:
            log.error("Webhook error: %s", e)

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, fmt, *args):
        pass


def run_webhook():
    port = int(os.environ.get("PORT", 10000))
    if WEBHOOK_URL:
        set_webhook(f"{WEBHOOK_URL}/webhook")
    log.info("Webhook server on port %d", port)
    HTTPServer(("0.0.0.0", port), WebhookHandler).serve_forever()


# ── Polling modes ───────────────────────────────────────────────────

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
    set_webhook("")
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
    elif "--webhook" in sys.argv:
        run_webhook()
    else:
        run_polling()
