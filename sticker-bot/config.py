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
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")

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
        "Після підтвердження ми запустимо для вас промо-кампанію "
        "на *безкоштовну доставку* з вашого закладу за рахунок "
        "компанії Bolt. Кампанія стартує з *наступного понеділка* "
        "після підтвердження."
    ),
    "has_sticker_question": "Чи є у вас вже стікер Bolt Food?",
    "enter_provider_id": "Введіть ваш *Provider ID*:",
    "need_sticker": (
        "📦 Щоб отримати стікер, нам потрібна інформація.\n\n"
        "Введіть ваш *Provider ID*:"
    ),
    "need_sticker_city": "Оберіть ваше місто:",
    "need_sticker_city_other": "Введіть назву вашого міста:",
    "need_sticker_phone": "Введіть *номер телефону* отримувача (наприклад, 0671234567):",
    "need_sticker_recipient": "Введіть *ім'я та прізвище* отримувача:",
    "need_sticker_np_type": "Куди надіслати стікер?",
    "need_sticker_np_list": "Оберіть зі списку ({page}/{pages}, всього: {total}):",
    "need_sticker_np_empty": "За вашим запитом нічого не знайдено. Спробуйте інше:",
    "need_sticker_np_fallback": (
        "Введіть *номер або адресу відділення Нової Пошти* вручну.\n\n"
        "Наприклад: `Відділення №5, вул. Хрещатик, 22`"
    ),
    "sticker_request_sent": (
        "✅ Дякуємо! Ваш запит на стікер прийнято.\n"
        "Ми надішлемо стікер найближчим часом.\n\n"
        "Коли наклеїте його — поверніться через /start "
        "і надішліть фото підтвердження."
    ),
    "provider_confirm": (
        "Знайдено заклад:\n\n"
        "📍 *{name}*\n"
        "Місто: {city}\n"
        "Район: {zone}\n\n"
        "Це ваш заклад?"
    ),
    "provider_not_found": (
        "❌ Provider ID `{pid}` не знайдено серед партнерів UA.\n"
        "Перевірте і спробуйте ще раз."
    ),
    "provider_wrong": (
        "Перевірте Provider ID і спробуйте ще раз.\n"
        "Введіть ваш *Provider ID*:"
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
        "🎉 Ваше фото підтверджено!\n\n"
        "Промо-кампанія на *безкоштовну доставку* з вашого закладу "
        "за рахунок компанії Bolt буде запущена автоматично "
        "з *наступного понеділка*."
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
    "admin_sticker_request": (
        "📦 *Запит на стікер*\n\n"
        "Provider: `{provider_id}`\n"
        "Назва: {provider_name}\n"
        "Місто: {city}\n"
        "Отримувач: {recipient}\n"
        "Телефон: {phone}\n"
        "Нова Пошта: {nova_poshta}\n"
        "Від: {username}\n"
        "Час: {time}"
    ),
}

CITIES = [
    "Київ", "Львів", "Одеса", "Харків", "Дніпро",
    "Запоріжжя", "Вінниця", "Івано-Франківськ",
    "Тернопіль", "Хмельницький", "Чернівці", "Рівне",
]

