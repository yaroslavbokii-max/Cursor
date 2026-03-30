# Databricks Table Reference

Known tables by workspace and schema. For live column-level details, check
`/Users/artemfedorov/databricks-setup/schema_notes.md` (updated as tables are explored).

## bolt-incentives

### Pre-Aggregated Fact Tables (PRIMARY for reporting)

These are the **preferred tables** for P&L, performance, and trend analysis. They use invoiced figures
and pre-calculated metrics (GP, CP). Available at four granularity levels, with both weekly and monthly variants:

| Level | Weekly Additive | Monthly Additive | Non-Additive (weekly) | Non-Additive (monthly) |
|-------|----------------|------------------|----------------------|----------------------|
| Global | `ng_delivery_spark.fact_delivery_global_weekly` | `...global_monthly` | `mart_models_spark.fact_delivery_global_non_additive_weekly` | `...monthly` |
| Country | `ng_delivery_spark.fact_delivery_country_weekly` | `...country_monthly` | `mart_models_spark.fact_delivery_country_non_additive_weekly` | `...monthly` |
| City | `ng_delivery_spark.fact_delivery_city_weekly` | `...city_monthly` | `mart_models_spark.fact_delivery_city_non_additive_weekly` | `...monthly` |
| Zone | `ng_delivery_spark.fact_delivery_zone_weekly` | `...zone_monthly` | `mart_models_spark.fact_delivery_zone_non_additive_weekly` | `...monthly` |

**Key rules:**
- **"Bolt Food" = `delivery_vertical IN ('food', 'store_3p_ent', 'store_3p_mm_smb')`** -- NOT just 'food'. Omitting 3P stores undercounts GMV by ~1.8%.
- **Match time grain to reporting need**: use monthly tables for monthly, weekly for weekly. NEVER aggregate weekly table into months (week-boundary distortion gives wrong numbers).
- Additive tables have `country_code` at country/city/zone levels, `city_id` at city/zone levels
- Global table has NO country/city filter -- use country-level table for country analysis
- Non-additive tables use `entity_name`/`entity_id` for the entity dimension
- Partitioned on `metric_timestamp_partition` (date) or `timeframe_date` (date)
- Ratio metrics use weighted-average pattern: `SUM(metric_value * metric_weight) / NULLIF(SUM(metric_weight), 0)`

#### Key Additive Columns (fact_delivery_country_weekly etc.)

| Column | Description |
|--------|-------------|
| `total_gmv_before_discounts_eur` | GMV before discounts (the standard GMV measure) |
| `total_gmv_after_discounts_eur` | GMV after discounts |
| `total_gross_profit_eur` | Gross Profit |
| `total_contribution_profit_eur` | Contribution Profit (the north-star metric) |
| `total_contribution_profit_without_demand_incentives_eur` | CP excluding demand incentives |
| `total_invoiced_demand_incentives_eur` | Invoiced demand incentives (Bolt-funded discounts) |
| `total_invoiced_supply_incentives_eur` | Supply-side incentives |
| `total_invoiced_courier_costs_eur` | Total invoiced courier costs |
| `total_invoiced_courier_earnings_eur` | Courier earnings |
| `total_invoiced_supply_refunds_eur` | Supply refunds |
| `total_invoiced_demand_refunds_eur` | Demand refunds |
| `total_invoiced_refunds_eur` | Total refunds |
| `total_invoiced_provider_commission_eur` | Provider commission revenue |
| `total_eater_fee_revenue_eur` | Eater fee revenue |
| `courier_delivered_orders_count` | Delivered orders count |
| `sessions_all_users_count` | Total sessions |
| `users_delivered_orders_count` | Unique users with delivered orders |

#### Key Non-Additive Columns (fact_delivery_country_non_additive_weekly etc.)

| Column | Description |
|--------|-------------|
| `active_users_delivery_count` | Active delivery users (COUNT DISTINCT) |
| `active_users_delivery_food_count` | Active food users |
| `active_users_delivery_bolt_plus_count` | Active Bolt Plus users |
| `active_courier_count` | Active couriers |
| `active_provider_count` | Active merchants |
| `delivered_orders_per_user` | Orders per user |
| `delivered_orders_per_provider` | Orders per merchant |
| `provider_pop_churn_count` | Merchant churn count |
| `active_top_brands_provider_count` | Active top-brand merchants |

### Other Fact Tables

| Schema | Table | Grain | Notes |
|--------|-------|-------|-------|
| ng_delivery_spark | `fact_provider_weekly` | provider × week | Provider-level weekly metrics |
| ng_delivery_spark | `fact_courier_weekly` | courier × week | Courier-level weekly metrics |
| ng_delivery_spark | `fact_user_delivery_weekly` | user × week | User-level weekly metrics |
| ng_delivery_spark | `fact_campaign_delivery_weekly` | campaign × week | Campaign-level weekly metrics |
| mart_models_spark | `fact_provider_non_additive_weekly` | provider × week | Provider non-additive metrics |
| mart_models_spark | `fact_courier_non_additive_weekly` | courier × week | Courier non-additive metrics |

### Order-Level Tables (for drill-downs)

| Schema | Table | Notes |
|--------|-------|-------|
| ng_public_spark | `etl_delivery_order_monetary_metrics` | Order-grain monetary metrics. `country` (not country_code), `order_created_date` is STRING. Has raw campaign cost columns (bolt_delivery_campaign_cost_eur etc.) but these differ from invoiced figures. Use for order-level drill-downs, NOT for aggregate P&L reporting. |
| ng_public_spark | `etl_delivery_campaign_order_metrics` | Order-grain campaign details: campaign_id, campaign_type, name, spend_objective, cost_share_v2, discount_value, bolt_spend, provider_spend, third_party_spend. Partitioned on order_created_date. |
| ng_delivery_spark | `dim_order_delivery` | Order dimension (from the consolidated queries -- active_users, store_gmv_share). NOT order-level fact; more of a denormalized view. |

### Dimension Tables

| Schema | Table | Key Columns | Notes |
|--------|-------|-------------|-------|
| ng_delivery_spark | `dim_delivery_city` | city_id, city_name, country_code, country_name, business_region_name, marketplace_region_name, food_delivery_launch_date, city_tier, city_segment | City dimension. Join to fact tables on city_id. |
| ng_delivery_spark | `dim_provider_v2` | provider_id, provider_name, business_segment, country_code, city_id, zone_name | Merchant dimension. business_segment: IC, Key Account, Local Hero, Missing Segment Trait. |
| ng_delivery_spark | `dim_courier` | courier_id, city_id | Courier dimension |
| core_models_spark | `dim_country` | country_code, ... | Country dimension |

### User Lifecycle & Cohort Tables

| Schema | Table | Key Columns | Notes |
|--------|-------|-------------|-------|
| ng_public_spark | `etl_eater_cohorts_lcs_weekly_by_city` | user_id, city_id, country_code, stage, conversion_cohort, profitability_abs_cohort, rfm_cohort, cohort_name, week_date, churn_probability_stage | Weekly user LCS classification. Partitioned on week_date. |
| ng_public_spark | `mart_delivery_eater_primary_city_zone_weekly` | user_id, city_id, city_zone_name, city_zone_segment, as_on_week_date | User primary zone assignment. Partitioned on as_on_week_date. |
| core_models_spark | `fact_user_subscriptions` | _(not yet described)_ | Bolt Plus subscription data |

### User Dimension Table

| Schema | Table | Key Columns | Notes |
|--------|-------|-------------|-------|
| ng_delivery_spark | `dim_user_delivery` | user_id, city_id, is_user_activated_in_delivery, delivery_activation_ts, food_activation_ts, market_activation_ts, first_delivery_order_id, first_food_order_id, last_delivery_order_created_ts, is_bolt_plus_subscriber, bolt_plus_first_subscribed_ts, user_sign_up_authorised_ts, created_ts | User dimension: signup, activation, first/last orders, Bolt Plus status. One row per user. No partition -- dimension table. |

### Experiment / A-B Test Tables

| Schema | Table | Key Columns | Notes |
|--------|-------|-------------|-------|
| ng_public_spark | `etl_delivery_campaigns_enrollments` | eater_id, campaign_id, test_id, treatment_id, treatment_type, cohort, lcs_cohort, city_id, country, enrolled_at, enrolled_at_date (partition, STRING) | User enrollment into tests. One row per user × test. treatment_type = 'control' means control group (campaign_id is NULL). Join eater_id → user_id in other tables. |
| ng_public_spark | `etl_delivery_campaigns_ab_scorecard_lcs` | test_id, treatment_id, cohort, spend_objective, city_id, country, test_start_date (partition) | Experiment scorecard results. One row per treatment_id. Contains gmv, orders, uplift, p-values, contribution profit, UC ratios. Use for test result analysis. |

### Campaign & Merchant Tables

| Schema | Table | Key Columns | Notes |
|--------|-------|-------------|-------|
| ng_delivery_spark | `delivery_campaign_provider` | campaign_id, provider_id, enrollment_state, city_id, bundle_id, start, expires_at, weekdays, interval_start/end, enrollment_source | Provider campaign enrollment. Partitioned on created_date (STRING). |
| core_models_spark | `fact_provider_smart_promo_offer_campaign_enrollment` | smart_promo_offer_id, provider_id, campaign_id, campaign_spend_objective, smart_promo_enrollment_state, smart_promo_type, smart_promo_offer_mode, is_valid_promotion, country_code, city_id | Smart promo enrollment data. |
| ng_public_spark | `etl_incentives_provider_targeting_features` | provider_id, date, status, sales_segment, account_management_segment, city_zone_name, is_early_lifecycle, predicted_churn_probability, provider_type, regular_commission, provider_country_code, provider_city_id, can_self_assign_campaign | Provider targeting features with churn prediction. |

### Basket & Item Tables

| Schema | Table | Key Columns | Notes |
|--------|-------|-------------|-------|
| ng_delivery_spark | `dim_basket_item_delivery` | basket_item_id, order_id, provider_id, item_id, product_id, sku, basket_item_name, basket_item_type, menu_item_type, campaign_id, campaign_spend_objective, item_price_before_discount_with_vat_eur, order_created_date_local | Item-level dimension with pricing. Partitioned on order_created_date_local. |
| ng_delivery_spark | `etl_delivery_order_user_basket_item_v2` | order_id, user_basket_item_id, item_id, name, unit_price, total_price, order_id, product_id, sku, basket_item_state, menu_item_type | Raw basket item data. Partitioned on created_date (STRING). |
| ng_delivery_store_spark | `etl_delivery_store_order_item_cogs` | order_id, provider_id, store_id, sku, item_id, quantity, total_purchasing_price_gross_eur, total_selling_price_gross_eur, campaign_spend_objective | Store COGS at item level. |

### Business Review Tables

| Schema | Table | Notes |
|--------|-------|-------|
| ng_delivery_spark | `delivery_business_review_metrics_weekly` | Pre-built business review metrics |
| ng_delivery_spark | `food_business_review_metrics_weekly_v2` | Food-specific business review (v2) |

## bolt-common

Not yet catalogued. Run `SHOW SCHEMAS` and `SHOW TABLES IN <schema>` to discover.

## bolt-data

Not yet configured.
