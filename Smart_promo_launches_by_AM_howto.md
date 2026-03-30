# Smart promos launched — by Account Manager (this week)

**What we checked in your workspace:** `Settings` (Databricks & QBRs), `MBR`, `Agents`, `context files` (Looker guide + Bolt Food Metrics Glossary), `WBR with GM` (commission CSV), `assets`.  
**Result:** None of these files contain a pre-built export or weekly counts per AM. They only document **where** the data lives (Looker explores + Databricks tables).

---

## Option A — Looker (fastest if you have `curated_delivery` access)

1. Open **[⭐ Metrics - Campaigns](https://bolt.cloud.looker.com/explore/curated_delivery/fact_campaign)**  
   *Owner: James Davies & Bram Verhoef — questions in #food-analytics.*

2. Add dimensions:
   - Time: **week** (or **day**) matching *this calendar week*.
   - **Country / city** if you only need one market.
   - In **Merchants / Provider** dimensions, look for anything like **Account Manager**, **Owner**, **Salesforce owner** (exact label varies by explore).  
   *Glossary references “Provider activity - Account Management” under **⭐ The Delivery Explore** and **⭐ Metrics - Merchants** — AM-related fields often sit next to merchant dimensions.*

3. Under **Campaigns → Smart Promotion Campaigns**, pick a metric that matches your definition of “launched”, e.g.:
   - **Smart Promotion Campaigns Merchants Enrolled, #** (merchants with SP discount on orders — *not* the same as “promo launched” unless that’s your KPI), or  
   - Any explore-specific **enrollment / new campaign / launch** metric your team uses for SP.

4. If **Metrics - Campaigns** does not expose AM as a dimension, try **[⭐ Metrics - Merchants](https://bolt.cloud.looker.com/explore/curated_delivery/fact_provider)** with the same **Smart Promotion Campaigns** measures and merchant-level AM dimensions.

5. **Download** → CSV / Excel.

> **Important:** Your docs list `fact_provider_smart_promo_offer_campaign_enrollment` for enrollment, but do **not** list an AM column on that fact. The AM dimension almost always comes from a **provider/merchant dimension** joined in Looker — confirm the field name in the UI.

---

## Option B — Databricks SQL (when you need “launched this week” literally)

1. Inspect columns (names may differ in prod):

```sql
DESCRIBE TABLE core_models_spark.fact_provider_smart_promo_offer_campaign_enrollment;
```

2. Identify:
   - Column for **event time** (e.g. enrollment created, state change to live, `start_ts`, etc.).
   - How you define **one launch** (`COUNT(DISTINCT smart_promo_offer_id)` vs `campaign_id` vs `provider_id` × `offer`).

3. Join merchant dimension for AM (confirm column name — `dim_provider_v2` in notes has `account_management_segment`, not necessarily **AM name**):

```sql
-- TEMPLATE: adjust column names after DESCRIBE + confirm AM field exists
SELECT
  p.<account_manager_field> AS account_manager,  -- replace with real column
  COUNT(DISTINCT sp.smart_promo_offer_id) AS smart_promo_launches
FROM core_models_spark.fact_provider_smart_promo_offer_campaign_enrollment sp
JOIN ng_delivery_spark.dim_provider_v2 p
  ON sp.provider_id = p.provider_id
WHERE sp.country_code = 'ua'   -- if needed
  AND <sp.launch_or_enrollment_ts> >= date_trunc('week', current_date())
  AND <sp.launch_or_enrollment_ts> <  date_trunc('week', current_date()) + interval 7 days
  AND sp.is_valid_promotion = true   -- if applicable
GROUP BY 1
ORDER BY 2 DESC;
```

If **AM name** is not on `dim_provider_v2`, ask analytics for the table that maps `provider_id` → AM (often Salesforce / internal mart).

---

## What does *not* work from your files

| Source | Why |
|--------|-----|
| `WBR with GM/Commision .csv` | Brands + commission KPIs; no smart promo, no AM person |
| `MBR/*.csv` | High-level MBR metrics (e.g. Smart Promos MM %), not per-AM launches |
| Glossary | Points to explores + metric groups; no weekly AM extract |

---

## Next step

If you paste a **screenshot or list of dimension names** from Looker (Campaigns or Merchants explore) that contain “Account Manager”, I can rewrite the exact click-path and suggest the right measure for “launched”.
