# Правила авто-призначення UAM (Jira)

Живий документ: тут зафіксовано **усі бізнес-правила**, за якими працює скрипт [`jira_auto_assign.py`](jira_auto_assign.py).  
Колеги **дописують або змінюють** правила тут → далі зміни **впроваджуються в код** (людиною або через Cursor / AI з посиланням на цей файл).

---

## Як запропонувати нове правило

1. Відредагуй **цей файл** у гілці / PR (або опиши в issue з копією блоку нижче).
2. Додай рядок у [таблицю маршрутів](#таблиця-спецмаршрутів-ключові-слова--відповідальний) або окремий підрозділ з прикладами summary/description.
3. Вкажи обов’язково:
   - **Умова** (ключові слова / regex / бренд / винятки).
   - **Відповідальний** у Jira (Display name як у профілі + бажано `accountId`).
   - **Колонка після призначення** — так / ні; якщо так — **точна назва Status** у Jira.
   - **Пріоритет** відносно інших маршрутів (що важливіше, якщо збігаються кілька правил).
4. У PR опиши: *«Оновити `UAM_AUTO_ASSIGN_RULES.md` + синхронізувати `jira_auto_assign.py`»*.

### Шаблон для нового рядка (копіюй у таблицю)

| Порядок | Ключові слова / умова | Assignee (Jira) | Перехід у колонку | Примітки |
|--------:|------------------------|-----------------|-------------------|----------|
| (число) | … | … | Ні / так (назва) | … |

### Для AI / імплементації в коді

Після змін у цьому документі потрібно оновити (за потреби):

- `classify_special_route()` — порядок перевірок і ключові слова.
- `resolve_route_assignee()` — новий тип маршруту + env `UAM_ACCOUNT_ID_*` / `UAM_DISPLAY_NAME_*`.
- `run()` — гілка маршруту, `target_transition`, логи skip/warning.
- `prefetch_targets` — display name для кешу Jira.
- Докстрінг на початку `jira_auto_assign.py`, [`.env.example`](.env.example), **цей файл** (щоб залишався джерелом правди).

Увімкнення всіх keyword-маршрутів: `UAM_ROUTE_RULES_ENABLED=1` (за замовчуванням увімкнено).

---

## Загальна логіка (не keyword-маршрути)

| Крок | Що відбувається |
|------|------------------|
| Вибірка | JQL: проєкт **UAM**, **assignee is EMPTY**, статус **≠ Done**; опційно вік тікета (`UAM_MAX_TICKET_AGE_DAYS`), додатковий JQL, фільтр статусів (`UAM_STATUS_IN`). |
| Порядок обробки | За статусом: `UAM_STATUS_SORT_ORDER` або алфавіт статусу; у межах статусу — **новіші** перші. |
| Текст для правил | `summary` + plain text з `description` (ADF розгортається). |
| Якщо keyword-маршрут не спрацював | `provider_id` з кастомного поля або з тексту → **Databricks** `dim_provider_v2`, `country_code = 'ua'` → `account_manager_name` → пошук користувача в Jira. |
| Якщо AM не знайдено | Fallback (за замовчуванням **Joanna Lizza Ayson**), якщо не `UAM_SKIP_UNKNOWN_ASSIGNEE=1`. |

Якщо в API вже є assignee — тікет **не змінюється**.

---

## Порядок пріоритету спецмаршрутів

Перевірка йде **зверху вниз**: перше співпадіння виграє.

1. **simply2** — ДУ + legal / FOP  
2. **integration** — інтеграція, Poster  
3. **mcdonalds** — McDonald’s  
4. **mops** — фінанси / Vchasno / інвойси тощо  
5. Далі — **AM з Databricks** (див. вище)

---

## Таблиця спецмаршрутів (ключові слова → відповідальний)

| ID маршруту | Умова (у тексті тікета, зазвичай `lower()`) | Assignee | Колонка після assign* | Env (accountId / ім’я) |
|-------------|---------------------------------------------|----------|------------------------|-------------------------|
| **simply2** | Фрази: `ду припинення`, `ду на зміну` **або** legal/FOP: слово `фоп`/`fop`, `legal entity`, `юридичн`, `зміна юридичної`, `зміна фоп`, `legal change`, `termination agreement`, `угода припинення`, `припинення співпраці`, `припинення договору`, `додаткова угода`, `additional agreement`, `simply_2`, `simply 2` | **Tetiana Bondar** | Так → `SIMPLY_2PRIORITY` (або `UAM_STATUS_NAME_SIMPLY2`) | `UAM_ACCOUNT_ID_TETIANA`, `UAM_DISPLAY_NAME_TETIANA` |
| **integration** | Підрядок `інтегр`; опечатки `нтеграція`, `нтеграцію`; цілі слова `poster`, `integration` | **Khrystyna Berezna** | Ні (лише assignee) | `UAM_ACCOUNT_ID_KHRYSTYNA_INTEGRATION`, `UAM_DISPLAY_NAME_INTEGRATION` |
| **mcdonalds** | Підрядок `макдональд` або `mcdonald`; цілі слова `mcd`, `mcds` | **Hanna Ruda** | Ні | `UAM_ACCOUNT_ID_MCDONALDS_AM`, `UAM_DISPLAY_NAME_MCDONALDS_AM` |
| **mops** | `vchasno`, `вчасно`, `invoice`, `інвойс`, `invoices`, `рахунок-фактура`, слово `mops`, `фінансов`, `payout`, `виплата`, `deduction`, `компенсація`, `акт звірки`, `iban`, `ібан`, `рахунок від` | **Anna Zaritska** | Так → `MOPS TICKETS` (або `UAM_STATUS_NAME_MOPS`) | `UAM_ACCOUNT_ID_ANNA`, `UAM_DISPLAY_NAME_ANNA` |

\*Перехід у колонку виконується лише якщо `UAM_TRANSITION_ON_ROUTE=1` і з поточного статусу є дозволений transition.

---

## Довідник змінних `.env` (коротко)

| Змінна | Призначення |
|--------|-------------|
| `JIRA_EMAIL`, `JIRA_API_TOKEN` | Доступ до Jira API |
| `DATABRICKS_TOKEN` | Запит AM у `dim_provider_v2` |
| `JIRA_CUSTOM_FIELD_PROVIDER` | Поле з numeric `provider_id` (опційно) |
| `UAM_MAX_TICKET_AGE_DAYS` | `0` = усі дати; інакше обмеження `created` |
| `UAM_MAX_ISSUES` | Максимум тікетів за один прогін (дефолт 200) |
| `UAM_STATUS_IN` | Дозволені статуси (через кому) |
| `UAM_STATUS_SORT_ORDER` | Порядок колонок для обробки |
| `UAM_AUTO_ASSIGN_EXTRA_JQL` | Додатковий фрагмент JQL |
| `UAM_ROUTE_RULES_ENABLED` | `0` вимикає всі keyword-маршрути з таблиці |
| `UAM_TRANSITION_ON_ROUTE` | Переміщення в колонку для simply2 / mops |
| `UAM_DRY_RUN` | `1` — лише лог, без assign |
| `UAM_SKIP_UNKNOWN_ASSIGNEE` | `1` — без fallback, skip якщо не вдалося знайти людину |
| `UAM_FALLBACK_DISPLAY_NAME`, `UAM_FALLBACK_ACCOUNT_ID` | Fallback assignee |

Повний список і коментарі — у [`.env.example`](.env.example) та docstring у `jira_auto_assign.py`.

---

## Версія документа

- **Останнє узгодження з кодом:** зміни в коді мають відображатися тут; при зміні правил у коді без оновлення цього файлу — виправити PR.

Якщо щось у таблиці не збігається з поведінкою скрипта — **джерело істини для логіки** залишається код; цей файл треба оновити в тому ж PR.
