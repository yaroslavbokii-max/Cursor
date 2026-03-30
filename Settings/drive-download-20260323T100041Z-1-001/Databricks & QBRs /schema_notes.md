# Databricks Schema Notes

Auto-updated as tables are explored. This file is referenced by the Cursor skill
so the agent remembers what it has learned across sessions.

---

## Key Metric Definitions

- **AOV (standard)** = merchant price before discount per order = `SUM(menu_price_full_eur) / COUNT(orders)` from `etl_delivery_order_monetary_metrics`. This matches Looker's AOV. ~10% lower than GMV/order because GMV includes eater fees (delivery fee, service fee, small order fee).
- **GMV/Order** = `total_gmv_before_discounts_eur / courier_delivered_orders_count` from fact tables. Includes eater fees. NOT the same as AOV in Looker.

---

## bolt-common

_No tables explored yet. Run `SHOW SCHEMAS` to start._

## bolt-incentives

### Pre-Aggregated Fact Tables (PRIMARY for reporting)

#### ng_delivery_spark.fact_delivery_country_weekly

| Column | Type | Notes |
|--------|------|-------|
| metric_timestamp_local | timestamp | Week start timestamp (local) |
| metric_timestamp_partition | date | **Partition column.** Week start date. |
| delivery_vertical | string | 'food', 'store_1p', 'store_3p_ent', 'store_3p_mm_smb', 'store_unclassified', 'business', 'delivery' (empty for food!) |
| country_code | string | Lowercase ISO 2-letter (e.g. 'cz') |
| total_gmv_before_discounts_eur | float | **GMV (the standard measure)** |
| total_gmv_after_discounts_eur | float | GMV after discounts |
| total_gross_profit_eur | float | Gross Profit |
| total_contribution_profit_eur | float | **Contribution Profit (north star)** |
| total_contribution_profit_without_demand_incentives_eur | float | CP excluding demand incentives |
| total_invoiced_demand_incentives_eur | float | **Invoiced demand incentives** |
| total_invoiced_supply_incentives_eur | float | Supply-side incentives |
| total_invoiced_courier_costs_eur | float | **Total invoiced courier costs** |
| total_invoiced_courier_earnings_eur | float | Courier earnings |
| total_invoiced_provider_commission_eur | float | Provider commission revenue |
| total_eater_fee_revenue_eur | float | Eater fee revenue |
| total_invoiced_refunds_eur | float | Total refunds |
| total_invoiced_demand_refunds_eur | float | Demand refunds |
| total_invoiced_supply_refunds_eur | float | Supply refunds |
| courier_delivered_orders_count | float | **Delivered orders count** |
| sessions_all_users_count | float | Total sessions |
| users_delivered_orders_count | float | Unique users with delivered orders |
| order_placed_rate_value / _weight | float | Session-to-order conversion (weighted avg) |
| gmv_before_discounts_per_order_eur_value / _weight | float | AOV before discounts (weighted avg) |
| eater_fee_revenue_gmv_share_value / _weight | float | Eater fee as % of GMV (weighted avg) |
| provider_commission_gmv_share_value / _weight | float | Commission as % of GMV (weighted avg) |
| campaign_discount_gmv_share_value / _weight | float | Total campaign discount as % of GMV |
| campaign_spend_bolt_gmv_share_value / _weight | float | Bolt campaign spend as % of GMV |
| campaign_spend_provider_gmv_share_value / _weight | float | Provider campaign spend as % of GMV |
| session_provider_rs_closure_rate_value / _weight | float | Restaurant supply closure rate |

**CRITICAL: Metrics are split across two vertical groups:**
- **Financial metrics** (GMV, CP, GP, invoiced costs, bad_order_rate): `delivery_vertical IN ('food', 'store_3p_ent', 'store_3p_mm_smb')` = "Bolt Food" in Looker. Using only 'food' undercounts GMV by ~1.8%.
- **Operational metrics** (sessions, conversion rates, courier utilization, search usage, funnel steps): `delivery_vertical = 'delivery'`. These are NULL for 'food' vertical.
- **Operational metrics are NULL at country level** -- must query at **city level** (`fact_delivery_city_monthly/weekly`) with `delivery_vertical = 'delivery'` and join `dim_delivery_city` to filter by country.

#### mart_models_spark.fact_delivery_country_non_additive_weekly

| Column | Type | Notes |
|--------|------|-------|
| entity_name | string | Entity type identifier |
| entity_id | string | Entity value (e.g. country code) |
| delivery_vertical | string | Same as additive table |
| timeframe_value | timestamp | Week start timestamp |
| timeframe_date | date | **Partition column.** Week start date. |
| active_users_delivery_count | float | Active delivery users (COUNT DISTINCT) |
| active_users_delivery_food_count | float | Active food users |
| active_users_delivery_bolt_plus_count | float | Active Bolt Plus users |
| active_courier_count | float | Active couriers |
| active_provider_count | float | Active merchants |
| delivered_orders_per_user | float | Orders per user |
| delivered_orders_per_provider | float | Orders per provider |
| provider_pop_churn_count / rate | float | Merchant churn |
| active_top_brands_provider_count | float | Active top-brand merchants |

#### Table hierarchy (same column structure at each level, available in both weekly and monthly)

Weekly:
- `fact_delivery_global_weekly` / `fact_delivery_global_non_additive_weekly` -- no country/city filter
- `fact_delivery_country_weekly` / `fact_delivery_country_non_additive_weekly` -- has country_code
- `fact_delivery_city_weekly` / `fact_delivery_city_non_additive_weekly` -- has city_id
- `fact_delivery_zone_weekly` / `fact_delivery_zone_non_additive_weekly` -- has city_id + zone_name

Monthly (use for monthly reporting -- NEVER aggregate weekly into months):
- `fact_delivery_global_monthly` / `fact_delivery_global_non_additive_monthly`
- `fact_delivery_country_monthly` / `fact_delivery_country_non_additive_monthly`
- `fact_delivery_city_monthly` / `fact_delivery_city_non_additive_monthly`
- `fact_delivery_zone_monthly` / `fact_delivery_zone_non_additive_monthly`

### ng_public_spark

| Table | Key Columns | Notes |
|-------|------------|-------|
| etl_delivery_order_monetary_metrics | order_id, user_id, provider_id, courier_id, city_id, country (str, e.g. 'cz'), currency, currency_rate, order_created (timestamp), order_created_date (STRING, partition), gmv_eur, nmv_eur, net_income_eur, total_discount_eur, delivery_full_price_eur, delivery_discount_eur, delivery_price_after_discount_eur, menu_price_full_eur, menu_discount_eur, menu_price_after_discount_eur, courier_earnings_gross_eur, courier_earnings_net_eur, provider_commission_gross_eur, provider_commission_net_eur, bolt_delivery_campaign_cost_eur, bolt_menu_campaign_cost_eur, provider_delivery_campaign_cost_eur, provider_menu_campaign_cost_eur, small_order_fee_eur, service_fee_eur, is_bolt_market, is_bolt_market_1p | order_created_date is STRING (partition). Country is lowercase ISO 2-letter. **Use for order-level drill-downs only, NOT for aggregate P&L** (values differ from invoiced figures). |
| etl_delivery_campaign_order_metrics | campaign_id, campaign_type, name, spend_objective, cost_share_v2, city_id, country, target, campaign_start/end, discount_level, commission_increase, order_id, discount_value, cost_share, bolt_spend, provider_spend, third_party_spend, bolt_spend_without_vat, provider_id, order_created_date (partition) | Order-grain campaign details with spend breakdown. |
| etl_eater_cohorts_lcs_weekly_by_city | user_id, city_id, city_name, country_code, stage, conversion_cohort (int), profitability_abs_cohort (int), rfm_cohort, cohort_name, week_date (partition), churn_probability_stage, churn_probability_conversion_cohort, churn_probability_profitability_abs_cohort, churn_probability_cohort | Weekly user LCS classification. |
| mart_delivery_eater_primary_city_zone_weekly | user_id, city_id, city_zone_name, city_zone_segment, city_zone_polygon_id, as_on_week_date (partition) | User primary zone assignment. |
| etl_incentives_provider_targeting_features | provider_id, date (partition), status, sales_segment, account_management_segment, city_zone_name, is_early_lifecycle, predicted_churn_probability, provider_type, regular_commission, provider_country_code, provider_city_id, can_self_assign_campaign, merchant_campaign_spend_from_gmv_1d/7d/14d/30d | Provider targeting features with churn scores and commission data. |

### ng_delivery_spark

| Table | Key Columns | Notes |
|-------|------------|-------|
| dim_provider_v2 | provider_id, vendor_id, provider_name, vendor_name, brand_name, group_name, business_segment, business_segment_v2, business_subsegment_v2, brand_tier, account_management_segment, country_code (lowercase ISO 2-letter), city_id, city_name, zone_name, zone_segment, delivery_vertical, provider_type, provider_status, lifecycle_status, is_virtual_brand_provider, is_top_brand, provider_rating, regular_commission_rate, takeaway_commission_rate, rod_commission_rate, is_bolt_plus_enrolled_provider, is_bolt_market_provider, is_store_provider, is_store_3p_ent, is_store_3p_mm_smb, supported_delivery_type, active_delivery_type, is_batchable, is_early_lifecycle_provider, first_active_ts, first_delivered_order_ts, last_delivered_order_ts, provider_price_level, min_order_value, small_order_fee_cap, service_fee_percentage, is_integrated_provider, pos_integrator_name | Merchant dimension. Use LOWER(provider_name) LIKE patterns to match brands. business_segment values: 'IC (Segment)', 'Key Account (Segment)', 'Local Hero (Segment)', 'Missing Segment Trait'. Has commission rates, Bolt Plus enrollment, store flags, ELC status. No partition. |
| dim_delivery_city | city_id, city_name, city_timezone, is_city_active, city_polygon, country_code, country_name, is_country_active, country_currency, business_region_name, marketplace_region_name, food_delivery_launch_date, is_primary_city, is_new_city, is_expansion_city, city_tier | City dimension. Join to fact tables on city_id. Use to map country_code → country_name when needed. |
| dim_user_delivery | user_id, city_id, is_user_activated_in_delivery, is_user_first_activated_in_food, is_user_first_activated_in_market, delivery_activation_ts, food_activation_ts, market_activation_ts, first_delivery_order_id, first_food_order_id, first_market_order_id, last_delivery_order_created_ts, last_food_order_created_ts, is_bolt_plus_subscriber, bolt_plus_first_subscribed_ts, bolt_plus_last_subscribed_ts, bolt_plus_last_unsubscribed_ts, user_sign_up_authorised_ts, created_ts, created_date, original_media_source, user_acquisition_source, appsflyer_campaign_name, first_session_started_ts, first_provider_search_event_ts, first_provider_viewed_event_ts, first_product_added_event_ts, first_cart_viewed_event_ts, city_timezone | User dimension. One row per user_id. Has activation timestamps per vertical, first/last order IDs, Bolt Plus subscription status, attribution data. No partition -- dimension table. Join on user_id. |
| dim_basket_item_delivery | basket_item_id, order_id, provider_id, item_id, product_id, sku, basket_item_name, basket_item_type, menu_item_type, campaign_id, campaign_spend_objective, item_price_before_discount_with_vat_eur, order_created_date_local (partition) | Item-level dimension with pricing. |
| etl_delivery_order_user_basket_item_v2 | order_id, user_basket_item_id, item_id, name, unit_price, total_price, product_id, sku, basket_item_state, menu_item_type, created_date (STRING partition) | Raw basket item data. |
| delivery_campaign_provider | id, campaign_id, provider_id, enrollment_state, city_id, bundle_id, start, expires_at, weekdays, interval_start/end, enrollment_source, created_date (STRING partition) | Provider campaign enrollment. |
| dim_order_delivery | ORDER_CREATED_TS_LOCAL, ORDER_CREATED_DATE_LOCAL, delivery_vertical, user_id, city_id, order_gmv_eur, order_delivered_ts | Order dimension (not order-level fact). Used in consolidated queries for active users and store GMV share. |

### Experiment / A-B Test Tables (ng_public_spark)

| Table | Key Columns | Notes |
|-------|------------|-------|
| etl_delivery_campaigns_enrollments | eater_id (= user_id), campaign_id, test_id, treatment_id, enrolled_at, enrolled_at_date (STRING, partition), treatment_type ('control' = control group, campaign_id NULL), cohort, lcs_cohort, city_id, country, holdout_id, test_start, test_end, campaign_start, campaign_end, enrollment_expires_at, enrollment_valid_end_at, bonus_type, treatment_bonus_type | One row per user × test enrollment. Use to find users in a specific test/campaign. Join eater_id → user_id. |
| etl_delivery_campaigns_ab_scorecard_lcs | test_id, treatment_id, cohort, spend_objective, bonus_type, bonus_value, max_code_usage, cost_share_percentage, city_id, country, test_start (timestamp), test_start_date (DATE, partition), users_enrolled, users_enrolled_control, gmv, nmv, finished_orders, finished_orders_control, bolt_campaign_cost, provider_campaign_cost, total_discount, gmv_uplift, finished_orders_uplift, bolt_cost_uplift, conversion_rate, conversion_rate_control, campaign_roi, gmv_p_value, finished_orders_p_value, uc_ratio_bolt, uc_ratio_total, contribution_profit_percentage, incremental_contribution_profit_eur, active_eaters, active_eaters_control, active_eaters_uplift, active_eater_p_value | One row per treatment_id. Scorecard for experiment results. combined GMV U/C = SUM(bolt gmv uplift) / SUM(bolt cost uplift). combined net activation rate = SUM(enrolled*act_rate)/SUM(enrolled) - SUM(control_enrolled*control_act_rate)/SUM(control_enrolled). |

### ng_delivery_store_spark

| Table | Key Columns | Notes |
|-------|------------|-------|
| etl_delivery_store_order_item_cogs | order_id, provider_id, store_id, sku, item_id, quantity, total_purchasing_price_gross_eur, total_selling_price_gross_eur, campaign_spend_objective | Store COGS at item level. |

### core_models_spark

| Table | Key Columns | Notes |
|-------|------------|-------|
| fact_user_subscriptions | _Not yet described_ | Bolt Plus subscription data |
| fact_provider_smart_promo_offer_campaign_enrollment | smart_promo_offer_id, provider_id, campaign_id, campaign_spend_objective, smart_promo_enrollment_state, smart_promo_type, smart_promo_offer_mode, is_valid_promotion, country_code, city_id | Smart promo enrollment data. |

### mart_models_spark

| Table | Key Columns | Notes |
|-------|------------|-------|
| fact_delivery_global_non_additive_weekly | entity_name, entity_id, delivery_vertical, timeframe_value, timeframe_date (partition) | Global non-additive metrics (no country filter) |
| fact_delivery_country_non_additive_weekly | (same structure + country entity) | Country-level non-additive metrics |
| fact_delivery_city_non_additive_weekly | (same structure + city entity) | City-level non-additive metrics |
| fact_delivery_zone_non_additive_weekly | (same structure + zone entity) | Zone-level non-additive metrics |

## bolt-data

_Not yet configured._
