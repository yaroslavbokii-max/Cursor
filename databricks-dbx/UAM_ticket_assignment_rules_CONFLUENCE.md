# UAM Jira — правила автопризначення відповідальних

> **Як опублікувати в Confluence:** Створи нову сторінку в потрібному Space → встав цей текст (Confluence підтримує Markdown у редакторі або через /markdown). Надай права перегляду колегам.

**Власник процесу:** *(вкажи ім’я)*  
**Останнє оновлення:** 2026-03-27  
**Код автоматизації:** `databricks-dbx/jira_auto_assign.py` (локально + cron)

---

## Мета

Єдині правила для того, **кому** призначається тікет проєкту **UAM** (`boltfoodops`) і **в яку колонку** його відправляти, щоб збігатися з SOP і скриптом.

---

## Дошка

- Jira: проєкт **UAM**, дошка (приклад): UAM board / Ukraine menus.
- Колонки (орієнтир): INVISIBLE → SIMPLY_1 / SIMPLY_2 → MOPS → **AM TICKETS** → IN PROGRESS → PENDING → DONE.

---

## Хто за що відповідає (ручний процес + автоматизація)

| Тип запиту | Колонка (статус) | Відповідальний |
|------------|------------------|----------------|
| Юридичні зміни, **ФОП**, припинення / додаткові угоди тощо | **SIMPLY_2PRIORITY** | **Tetiana Bondar** |
| Фінанси, **Vchasno**, інвойси, виплати, акти звірки тощо | **MOPS TICKETS** | **Anna Zaritska** |
| Звичайні AM-кейси (мерчанти, меню, операційні питання) | Зазвичай **AM TICKETS** → далі за процесом | **Account Manager** з даних (Databricks `dim_provider_v2.account_manager_name` для `provider_id`) |

Скрипт використовує **ключові слова** в summary + description; список уточнюється тут при потребі.

---

## Технічні деталі (для підтримки скрипта)

- **Databricks:** `ng_delivery_spark.dim_provider_v2`, `country_code = 'ua'`, поле `account_manager_name`.
- **Jira API:** assign + за потреби **transition** у цільовий статус.
- **Змінні середовища** (`.env` у `databricks-dbx/`): див. коментарі на початку `jira_auto_assign.py` (`UAM_ROUTE_RULES_ENABLED`, `UAM_STATUS_NAME_*`, `UAM_ACCOUNT_ID_*`, тощо).

### Запуск

```bash
cd databricks-dbx
UAM_DRY_RUN=1 python3 jira_auto_assign.py   # тест без змін
python3 jira_auto_assign.py                 # бойовий режим
```

---

## Історія змін

| Дата | Що змінили |
|------|------------|
| 2026-03-27 | Перша версія: правила Tetiana / Anna / AM, посилання на скрипт |

---

## Питання та узгодження

*(додавай рядки: дата — питання — рішення — хто)*

- 
