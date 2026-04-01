"""Bot configuration — loads secrets from env vars or .env file."""

import os
from pathlib import Path


def _load_env():
    env_path = Path(__file__).parent / ".env"
    if not env_path.is_file():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env()

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
ADMIN_CHAT_ID = os.environ.get("TELEGRAM_ADMIN_CHAT_ID", "")
DATABRICKS_TOKEN = os.environ.get("DATABRICKS_TOKEN", "")

DATABRICKS_HOST = "bolt-incentives.cloud.databricks.com"
DATABRICKS_HTTP_PATH = "sql/protocolv1/o/2472566184436351/0221-081903-9ag4bh69"

DATA_DIR = Path(__file__).parent / "data"
STATE_FILE = DATA_DIR / "state.json"
APPROVED_CSV = DATA_DIR / "approved.csv"

# ── Ukrainian messages ──────────────────────────────────────────────

MSG = {
    "welcome": (
        "Привіт! 👋\n\n"
        "Цей бот допоможе підтвердити розміщення стікера Bolt Food "
        "на вітрині вашого закладу.\n\n"
        "Після підтвердження ми запустимо промо-кампанію для вас.\n\n"
        "Будь ласка, введіть ваш *Provider ID*:"
    ),
    "provider_found": (
        "✅ Знайдено: *{name}*\n"
        "Місто: {city}\n\n"
        "Якщо це ваш заклад — надішліть фото стікера Bolt на вітрині."
    ),
    "provider_not_found": (
        "❌ Provider ID `{pid}` не знайдено серед партнерів UA.\n"
        "Перевірте і спробуйте ще раз."
    ),
    "provider_accepted": (
        "Прийнято Provider ID: `{pid}`.\n\n"
        "Надішліть фото стікера Bolt на вітрині вашого закладу."
    ),
    "photo_received": (
        "📸 Дякуємо! Ваше фото надіслано на перевірку.\n"
        "Ми повідомимо вас про результат."
    ),
    "already_submitted": (
        "Ви вже надіслали фото на перевірку.\n"
        "Щоб почати заново — натисніть /start"
    ),
    "already_approved": (
        "🔒 Заклад з Provider ID `{pid}` вже підтверджено раніше.\n"
        "Повторна подача неможлива."
    ),
    "already_pending": (
        "⏳ Заклад з Provider ID `{pid}` вже подано на перевірку.\n"
        "Очікуйте результат."
    ),
    "send_photo": "Будь ласка, надішліть саме *фото* (не файл).",
    "approved": (
        "🎉 Ваше фото підтверджено!\n"
        "Промо-кампанію буде запущено найближчим часом."
    ),
    "rejected": (
        "На жаль, фото не пройшло перевірку.\n"
        "Переконайтеся, що стікер добре видно, і спробуйте знову через /start"
    ),
    "myid": "Ваш Chat ID: `{chat_id}`",
    "admin_new": (
        "📋 *Нова заявка на стікер*\n\n"
        "Provider: `{provider_id}`\n"
        "Назва: {provider_name}\n"
        "Місто: {city}\n"
        "Від: {username}\n"
        "Час: {time}"
    ),
}
