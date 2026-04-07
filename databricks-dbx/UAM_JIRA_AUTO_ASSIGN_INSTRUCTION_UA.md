# Автопризначення тікетів UAM у Jira — як це працює

Короткий опис для команди: що робить скрипт, у якому порядку він приймає рішення, які є налаштування та як запропонувати зміни.

---

## Що це

Скрипт **`jira_auto_assign.py`** періодично знаходить **незакриті тікети проєкту UAM без assignee** у Jira (`boltfoodops.atlassian.net`), визначає відповідального й **призначає** його. За потреби **переміщує тікет у колонку** (статус) для маршрутів Tetiana та Anna.

Текст для класифікації береться з **назви (summary)** і **опису (description)**; опис у форматі ADF конвертується в plain text.

---

## Де лежить код і конфіг

| Що | Шлях |
|----|------|
| Скрипт | `databricks-dbx/jira_auto_assign.py` |
| Секрети та налаштування | `databricks-dbx/.env` (не комітити; шаблон — `.env.example`) |

У `.env` мають бути принаймні:

- **`DATABRICKS_TOKEN`** — для запиту AM з Databricks  
- **`JIRA_EMAIL`** та **`JIRA_API_TOKEN`** — для Jira REST API  

---

## Як запускається (типово)

Рекомендований розклад (будні, локальний час машини, де стоїть cron):

```text
0 10,14,16 * * 1-5 cd /шлях/до/databricks-dbx && /usr/bin/python3 jira_auto_assign.py >> /tmp/jira_auto_assign.log 2>&1
```

Ручний запуск з тієї ж папки:

```bash
cd databricks-dbx && python3 jira_auto_assign.py
```

Перевірка без змін у Jira: у `.env` тимчасово **`UAM_DRY_RUN=1`**.

---

## Які тікети потрапляють у вибірку (JQL)

Базовий запит (спрощено):

- проєкт **UAM**
- **assignee is EMPTY**
- статус **не Done**
- за замовчуванням **створені за останні 30 днів** (`UAM_MAX_TICKET_AGE_DAYS`, `0` = без обмеження за датою)
- сортування: **спочатку новіші**

Додатково можна звузити:

- **`UAM_AUTO_ASSIGN_EXTRA_JQL`** — фрагмент JQL (якщо не починається з `AND`, скрипт додасть ` AND ` на початку)
- **`UAM_STATUS_IN`** — список назв колонок через кому (точно як у Jira **Issue → Status**), напр. `All Tickets,AM TICKETS`

---

## Логіка призначення (порядок кроків)

1. **Вже є assignee** у відповіді API → тікет **не чіпаємо** (навіть якщо він якось потрапив у пошук).

2. Якщо увімкнено **`UAM_ROUTE_RULES_ENABLED=1`** (за замовчуванням так), текст **summary + description** проганяється через **`classify_special_route`** у **фіксованому порядку**:
   - спочатку перевірки на **SIMPLY2** (ДУ, legal/FOP тощо);
   - потім **інтеграція / Poster**;
   - потім **MOPS / фінанси**;
   - якщо нічого не зійшлося — маршруту немає, далі AM.

3. Для маршрутів **simply2** і **mops**: призначення відповідній людині + за **`UAM_TRANSITION_ON_ROUTE=1`** спроба **перевести** тікет у колонку `UAM_STATUS_NAME_SIMPLY2` / `UAM_STATUS_NAME_MOPS` (дефолти: `SIMPLY_2PRIORITY`, `MOPS TICKETS`).

4. Для маршруту **integration**: призначення **Khrystyna Berezna**; **перехід у колонку за замовчуванням не заданий** (лише assignee).

5. Якщо спеціального маршруту немає або власник маршруту не знайшовся в Jira (і не увімкнено жорсткий skip):
   - з тікета витягується **`provider_id`** (див. нижче);
   - у **Databricks** (`ng_delivery_spark.dim_provider_v2`, **`country_code = 'ua'`**) шукається **`account_manager_name`**;
   - якщо `provider_id` немає — пробуються **ефемерні запити по назві** з summary (пошук провайдера по імені, потім той самий AM).

6. Ім’я AM з Databricks **зіставляється** з користувачем Jira (`/user/search`, точний збіг display name, потім евристики по імені/прізвищу).

7. Якщо assignee так і не визначено:
   - **`UAM_SKIP_UNKNOWN_ASSIGNEE=1`** → тікет **пропускається** (без fallback);
   - інакше → **fallback** (за замовчуванням display name **Joanna Lizza Ayson**, або `UAM_FALLBACK_ACCOUNT_ID`).

8. Якщо assign не вдався через права, скрипт може **спробувати fallback** (коли не режим skip-unknown).

---

## Спеціальні маршрути (ключові слова)

Усі перевірки робляться по **рядку в нижньому регістрі** (окрім логіки regex, де явно вказано `\b` — межа слова).

### 1. SIMPLY2 → Tetiana Bondar (+ колонка SIMPLY_2 за замовчуванням)

- Фрази: **`ду припинення`**, **`ду на зміну`**
- Далі блок **legal / FOP** (приклади): `фоп`, `fop`, `legal entity`, `юридичн`, `зміна юридичної`, `зміна фоп`, `legal change`, `termination agreement`, `угода припинення`, `припинення співпраці`, `припинення договору`, `додаткова угода`, `additional agreement`, `simply_2`, `simply 2`

### 2. Integration → Khrystyna Berezna (без дефолтного переходу колонки)

- Підрядок **`інтегр`** (покриває інтеграція, інтеграцію, інтеграції тощо)
- Опечатки: **`нтеграція`**, **`нтеграцію`**
- Цілі слова: **`poster`**, **`integration`**

**Важливо:** цей блок перевіряється **раніше** за MOPS. Якщо в одному тексті є і «integration», і фінансові маркери, спрацює **integration** (Khrystyna), а не Anna.

### 3. MOPS → Anna Zaritska (+ колонка MOPS за замовчуванням)

Приклади маркерів: `vchasno`, `вчасно`, `invoice`, `інвойс`, `invoices`, `рахунок-фактура`, слово `mops`, `фінансов`, `payout`, `виплата`, `deduction`, `компенсація`, `акт звірки`, `iban`, `ібан`, `рахунок від`

---

## Звідки береться `provider_id`

1. Опційне кастомне поле Jira: **`JIRA_CUSTOM_FIELD_PROVIDER`** (наприклад `customfield_12345`).
2. Інакше — парсинг **summary** і **description**:
   - спочатку явні шаблони на кшталт `provider id: 12345`;
   - інакше перше «правдоподібне» число 4–8 цифр (роки на кшталт 2024 відфільтровуються евристикою).

---

## Змінні середовища (коротко)

Повний перелік з поясненнями — у **docstring** на початку `jira_auto_assign.py` і в коментарях **`databricks-dbx/.env.example`**.

Ключові групи:

| Група | Приклад змінних |
|--------|------------------|
| Jira / Databricks | `JIRA_EMAIL`, `JIRA_API_TOKEN`, `DATABRICKS_TOKEN` |
| Обсяг і фільтри | `UAM_MAX_ISSUES`, `UAM_MAX_TICKET_AGE_DAYS`, `UAM_STATUS_IN`, `UAM_AUTO_ASSIGN_EXTRA_JQL` |
| Маршрути | `UAM_ROUTE_RULES_ENABLED`, `UAM_TRANSITION_ON_ROUTE`, `UAM_STATUS_NAME_SIMPLY2`, `UAM_STATUS_NAME_MOPS` |
| Account ID (надійніше за пошук по імені) | `UAM_ACCOUNT_ID_TETIANA`, `UAM_ACCOUNT_ID_ANNA`, `UAM_ACCOUNT_ID_KHRYSTYNA_INTEGRATION` |
| Імена для пошуку | `UAM_DISPLAY_NAME_TETIANA`, `UAM_DISPLAY_NAME_ANNA`, `UAM_DISPLAY_NAME_INTEGRATION` |
| Fallback | `UAM_FALLBACK_DISPLAY_NAME`, `UAM_FALLBACK_ACCOUNT_ID` |
| Поведінка | `UAM_DRY_RUN`, `UAM_SKIP_UNKNOWN_ASSIGNEE`, `JIRA_CUSTOM_FIELD_PROVIDER` |

---

## Як колегам запропонувати правки

1. **Нові ключові слова або новий маршрут** — правити функцію **`classify_special_route`** у `jira_auto_assign.py` (зберегти порядок перевірок або явно узгодити з командою новий пріоритет).
2. **Інший assignee для маршруту** — **`resolve_route_assignee`** + за потреби нові змінні `UAM_ACCOUNT_ID_*` / `UAM_DISPLAY_NAME_*`.
3. **Колонка після призначення** — для Tetiana/Anna: **`target_transition`** у циклі `run()` і відповідна змінна `UAM_STATUS_NAME_*`. Для integration зараз transition не задається; додати — окремий невеликий патч у `run()`.
4. **Звузити/розширити вибірку тікетів** — JQL-частина **`fetch_unassigned_tickets`** або змінні `UAM_*` без зміни коду, де це достатньо.
5. Перед продакшеном: **`UAM_DRY_RUN=1`**, переглянути лог; за потреби тимчасово **`UAM_MAX_ISSUES`** зменшити.

Після змін варто прогнати скрипт у dry-run і переконатися, що в Jira **display name** користувачів збігаються з очікуваннями (або задати **`UAM_ACCOUNT_ID_*`**).

---

## Обмеження та нюанси

- Дані AM — **Україна**: `dim_provider_v2` з **`country_code = 'ua'`**. Інші країни цим шляхом не покриті.
- Класифікація **проста по підрядках/regex** — можливі хибні спрацьовування; нові правила краще узгоджувати з прикладами реальних summary/description.
- Перехід у статус залежить від **доступних transitions** у workflow Jira; якщо колонка недоступна з поточного статусу, у логу буде попередження.

---

*Документ відповідає стану коду в репозиторії (файл `jira_auto_assign.py`). Якщо логіка зміниться — оновіть цю інструкцію разом із PR.*
