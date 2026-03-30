# Bolt Food Delivery Analysis Framework

## Critical: Table Selection Guide

**For aggregate P&L and trend reporting** (GMV, CP, GP, demand incentives, CPO):
→ Use pre-aggregated fact tables with **monthly** granularity for monthly reporting, **weekly** for weekly.
→ Monthly: `fact_delivery_country_monthly`, `fact_delivery_city_monthly`, etc.
→ Weekly: `fact_delivery_country_weekly`, `fact_delivery_city_weekly`, etc.
→ **Do NOT aggregate weekly tables into months** -- week-boundary distortion gives wrong results.
→ These contain invoiced figures and pre-calculated CP/GP.

**For order-level drill-downs** (basket analysis, specific order investigation):
→ Use `etl_delivery_order_monetary_metrics` (raw campaign costs, NOT invoiced figures).

**For user-level analysis** (cohorts, LCS stages):
→ Use `etl_eater_cohorts_lcs_weekly_by_city` + non-additive fact tables.

**NEVER use `etl_delivery_order_monetary_metrics` for aggregate P&L reporting** -- its columns (gmv_eur, net_income_eur, bolt_delivery_campaign_cost_eur) do NOT match the official invoiced P&L figures.

**Metrics are split across two vertical groups:**
- **Financial** (GMV, CP, GP, invoiced costs, bad_order_rate): `delivery_vertical IN ('food', 'store_3p_ent', 'store_3p_mm_smb')` = "Bolt Food" in Looker.
- **Operational** (sessions, conversion, courier util, search, funnel): `delivery_vertical = 'delivery'`. These are NULL under 'food'.
- **Operational metrics are NULL at country level** -- must query **city-level table** (`fact_delivery_city_monthly`) with `delivery_vertical = 'delivery'`, joined to `dim_delivery_city` for country filter.

```sql
-- Financial metrics
FROM ng_delivery_spark.fact_delivery_country_monthly
WHERE delivery_vertical IN ('food', 'store_3p_ent', 'store_3p_mm_smb')

-- Operational metrics (sessions, courier util, conversion)
FROM ng_delivery_spark.fact_delivery_city_monthly f
JOIN ng_delivery_spark.dim_delivery_city c ON f.city_id = c.city_id
WHERE c.country_code = 'cz' AND f.delivery_vertical = 'delivery'
```

## Key Column Mapping (Old → Correct)

| Metric | WRONG (monetary_metrics) | CORRECT (fact_delivery tables) |
|--------|--------------------------|--------------------------------|
| GMV | gmv_eur | total_gmv_before_discounts_eur |
| Contribution Profit | net_income_eur (≠ CP!) | total_contribution_profit_eur |
| Gross Profit | _(not available)_ | total_gross_profit_eur |
| CP excl DI | _(not available)_ | total_contribution_profit_without_demand_incentives_eur |
| Demand Incentives | bolt_delivery_campaign_cost_eur + bolt_menu_campaign_cost_eur | total_invoiced_demand_incentives_eur |
| Courier Costs | courier_earnings_gross_eur | total_invoiced_courier_costs_eur |
| Orders | COUNT(DISTINCT order_id) | courier_delivered_orders_count |
| CPO | earnings / orders | total_invoiced_courier_costs_eur / courier_delivered_orders_count |
| delivery_vertical filter | _(no filter or is_bolt_market=false)_ | delivery_vertical = 'food' |

---

## Agent Instructions for Analysis

When performing data analysis, follow these rules:

1. **Always show three time views for every metric**:
   - **WoW delta** — the urgency signal (what changed this week?)
   - **YoY delta** — the primary trend signal (removes seasonality). Uses ISO week matching.
   - **Trailing 4-week trend** — smoothed direction
2. **Always show both absolute value and % change** for financial metrics.
3. **When identifying a problem city**, show its contribution to the country total (e.g., "Prague accounts for 45% of the country GMV drop").
4. **Follow the drill-down logic**: only go deeper into a branch if a higher level shows something off-track. Don't answer every question -- answer the path that matters.
5. **Cross-reference threshold**: WoW change <2% and within trailing 4-week range → normal, move on. WoW >5% or outside trailing range → drill down. YoY changes >10% always warrant a comment.
6. **If a metric is missing from the data, say so** -- never guess or fabricate values.
7. **Two parallel decompositions of Orders**:
   - `Orders = Active Users × Frequency` — use for user/cohort engagement issues
   - `Orders = Sessions × Conversion` — use for funnel/UX/pricing friction
   - Sessions down + conversion up → traffic problem. Sessions stable + conversion down → funnel problem.
8. **All-Time Best (ATB) benchmark**: For key metrics, compare current value to the best ever observed. Show which week achieved ATB. Direction matters (Orders = highest ↑, CPO = lowest ↓).
9. **City benchmarking**: Show share of country total for absolute metrics and vs country average for rate metrics.

---

## Navigation: Issue Tree Structure

```
0. NORTH STAR: GMV + Orders + CP L2
    │
    ├─ 1. GMV Decomposition
    │     ├─ 1a. Orders vs AOV — which is driving GMV?
    │     │     └─ AOV: Merchant Price vs Eater Fees vs Basket
    │     └─ 1b. City ranking — where is the swing?
    │
    ├─ 2. CP L2 Decomposition (P&L)
    │     ├─ 2a. CP: Revenue (Commission, EF Rev, Ads) vs Costs (CPO, Refunds)
    │     ├─ 2b. Supply Incentives
    │     └─ 2c. Demand Incentives: Type × Payer MECE, efficiency
    │
    ├─ 3. Users & Cohorts
    │     ├─ 3a. Active Users × Frequency — orders bridge
    │     ├─ 3b. Acquisition: Installs → Signups → Activation
    │     ├─ 3c. Bolt+ vs non-Bolt+: frequency, penetration, subs
    │     └─ 3d. Retention: 7d, 30d, core, new user, same-provider
    │
    ├─ 4. Conversion Funnel (Session Lens)
    │     ├─ Sessions → PA → CV → CS → CC → OP
    │     └─ Placed → Delivered drop-off
    │
    ├─ 5. CVP: Selection
    │     ├─ Merchant count, churn, coverage, availability
    │     ├─ Competitive: Bolt vs Wolt vs Foodora
    │     └─ Merchant ops: acceptance, processing time, menu quality
    │
    ├─ 6. CVP: Value (Price Leadership)
    │     ├─ Total user cost, GMV after discounts, eater fees burden
    │     └─ Discount intensity by program, merchant co-investment
    │
    ├─ 7. CVP: Service
    │     ├─ Bad orders, failed/rejected, late delivery
    │     ├─ CS tickets, CSAT, refunds
    │     └─ ETA accuracy, merchant root causes
    │
    ├─ 8. Courier / CPO
    │     ├─ CPO = EpH / DpH
    │     ├─ DpH: CDT, utilization, batching
    │     ├─ EpH: earnings, bonuses, multipliers
    │     └─ Supply health: active couriers, churn, acceptance
    │
    ├─ 9. Geo Investment Lens
    │     └─ City scorecard: CP L2, orders, spend, CVP health
    │
    ├─ 10. User & Merchant Deep Dive
    │     ├─ 10a. Cohort distribution & CP L2 by cohort
    │     ├─ 10b. Value destroyers, DI spend leak
    │     ├─ 10c. Cohort transitions (upgrade/downgrade matrix)
    │     ├─ 10d. Bolt+ before/after analysis
    │     └─ 10h. Merchant-level: movers, quality offenders, churn, ATB gap, AM view
    │
    └─ 11. Campaign Deep Dive
          ├─ 11a. Spend bridge: + New − Expired + Δ Continuing
          ├─ 11b. By objective (MECE): 39 Campaign Spend Objectives
          ├─ 11c. Lifecycle: top expired, top new, replacement quality
          └─ 11d. City drill-down
```

---

## GMV Decomposition Tree

```
GMV (total_gmv_before_discounts_eur) = Orders × AOV
  │
  ├── Orders = Active Users × Frequency
  │     ├── Active Users = Sessions × Session-to-Order Conversion
  │     │     ├── Sessions (sessions_all_users_count): brand awareness, cross-pollination, push/CRM, seasonality, competitors
  │     │     └── Conversion (order_placed_rate): selection, pricing/fees, service quality, courier availability
  │     └── Frequency (delivered_orders_per_user): engagement campaigns, Bolt Plus, merchant diversity, CVP satisfaction
  │
  └── AOV = Merchant Price/Order + Eater Fees/Order
        ├── Merchant Price/Order = Items/Order × Price/Item
        └── Eater Fees/Order = Delivery Fee + Service Fee + Small Order Fee
```

### From GMV to CP L2 (Profitability)

```
  GMV (total_gmv_before_discounts_eur)
- Discounts (menu + delivery)                    = NMV
+ Eater Fees (delivery, SOF, service fee)        = total_eater_fee_revenue_eur
= Eater Payment

Revenue:
  Commission (total_invoiced_provider_commission_eur)
+ Eater Fees (total_eater_fee_revenue_eur)
+ Other Revenue (total_invoiced_other_revenue_eur)

- Variable Costs:
  Courier Costs (total_invoiced_courier_costs_eur)
  Payment Fees
  Refunds (total_invoiced_refunds_eur)

= Gross Profit (total_gross_profit_eur)

- Semi-Variable Costs:
  Customer Service
  Courier Lifecycle: Courier Bags Costs, Other Supply Chain Costs, Transportation Costs
  Merchant Operations: Tablets Costs, Photography Costs, AM Headcount Costs
  Store-specific: Packaging Costs, Paper Bags Costs, Picker Costs, Warehouse Costs, Writeoff/Waste Costs
  Bad Debt
  Supply Incentives (total_invoiced_supply_incentives_eur)

= Contribution Profit (total_contribution_profit_eur)

- Demand Incentives (total_invoiced_demand_incentives_eur)

= CP L2 (total_contribution_profit_without_demand_incentives_eur)
  ≈ Pre-HQ EBITDA proxy
  *** THIS IS THE NORTH STAR, NOT CP OR GMV ***
  Target: CP L2 > 0 by October 2026
```

---

## CPO Decomposition

CPO is the biggest single cost line (~18% of GMV). It has dual decomposition:

### View 1: Operational Efficiency
```
CPO = EpH / DpH
  ├── EpH (Earnings per Hour): total_invoiced_courier_costs_eur / online_hours
  └── DpH (Deliveries per Hour) ≈ (60/CDT) × UT% × Batching uplift
        ├── CDT = Pickup Travel + Wait at Merchant + Picking Up + Dropoff Travel + Dropping Off
        ├── UT% = Utilised Hours / Online Hours (courier_utilisation_rate)
        └── Batching Rate (~24-32%)
```

### View 2: Cost Structure
```
Invoiced Courier Costs = Earnings + Bonus - Deductions + Adjustments + Wait Compensation
  ├── Earnings = Base (Pickup + Distance + Dropoff) + Multiplier (Proactive + Dynamic)
  └── Bonus can be 40-45% of total invoiced costs!
```

#### Courier Earnings Per Order Breakdown (from Looker / fact tables, all weighted averages)
```
Courier Total Earnings/Order
  ├── Courier Effort Based Earnings (total effort-based earnings)
  │     ├── Courier Total Base Earnings = Pickup Base + Distance Base + Dropoff Base
  │     ├── Courier Total Multiplier Earnings
  │     │     ├── Proactive Multiplier Earnings (Pickup + Distance + Dropoff proactive)
  │     │     └── Dynamic Multiplier Earnings (reactive/surge)
  │     └── Courier Minimum Earnings Top Up
  └── Courier Wait Time Compensation (at merchant)
  + Courier Tips (not part of invoiced costs)
```
Effective multiplier rates (pickup/distance/dropoff) show actual multiplier applied vs base.

#### CDT Breakdown (from Looker / fact tables, all weighted averages)
```
Courier Time per Order (accepted → delivered)
  ├── Courier Travelling to Merchant (pickup travel)
  ├── Courier Wait at Merchant
  │     ├── Wait Until Target Arrival (courier early → wait for food)
  │     └── Wait From Target Arrival (food late → courier waits extra)
  ├── Courier Picking Up Order (arrived/ready → picked up)
  ├── Courier Dropping Off Order (picked up → delivered)
  │     ├── Courier Travelling to Eater
  │     └── Courier Dropoff at Door
  └── Courier Redispatch Duration (if applicable)
```
Also tracked: Courier Acceptance Duration, Courier After Order Wait Time (between orders).

### View 3: Batching
```
Batched Order Rate (share of delivered orders in a batch)
  ├── Batched Same Merchant Rate (same provider batch)
  ├── Batched Multi-Merchant Rate (different providers)
  ├── Batched Pre-courier Assignment Rate (batch routing algorithm)
  └── Batched Post-courier Assignment Rate (instant batch algorithm)
```

**CPO denominator**: Always use **Courier Delivered Orders** (`courier_delivered_orders_count`), NOT User Delivered Orders. User Delivered includes own-delivery and takeaway with no courier cost (~5% gap).

### View 4: Courier Lifecycle
```
Courier Supply Pool:
  ├── Active Courier Count / Active Courier Root Count
  ├── New Active Courier Count (first delivery)
  ├── Courier Churn:
  │     ├── Soft Churn (14+ days inactive, can repeat within month)
  │     ├── Hard Churn (31+ days inactive, once per month)
  │     └── Permanent Churn (90+ days inactive)
  └── Resurrected Courier Count (returned after hard churn)
```

Key CPO levers: reducing CDT (esp. pickup travel), improving utilization, batching optimization, multiplier rate management.

---

## Campaign Decomposition (MECE)

### Two verified MECE dimensions for total campaign discount:
1. **By Type**: Menu + Delivery Fee + Service Fee = Total (exact)
2. **By Payer**: Bolt Spend + Merchant Spend = Total (exact)

### Campaign Spend Objectives (39 objectives, MECE — sums to total)

**Bolt ULC**: activation, engagement, reactivation, churn, acquisition, marketing, other
**Smart Promotions**: sp_engagement, sp_reactivation, sp_activation, sp_fully_funded, sp_liquidity
**Other Bolt**: liquidity, bolt_plus_campaign, new_city_launch
**Provider/Co-funded**: provider_campaign_portal, provider_campaign_marketing, provider_campaign_locations, provider_campaign_churn_prevention, provider_campaign_obligations_commitments, provider_campaign_commission_increase, provider_campaign_profit_generator, provider_campaign_sales_benefit, provider_campaign_ELC_merchant, etc.

### Campaign lifecycle bridge
```
ΔTotal Spend = + New Campaigns − Expired Campaigns + Δ Continuing Campaigns
```
- ~46% of campaigns live only 1 week. Portfolio turns over every 2-3 weeks.
- Partial-week detection: if continuing campaign dropped >30% WoW AND doesn't appear next week → partial last week artifact, not genuine decline.

### Critical data rules
- **Campaign orders are NOT additive** — one order triggers ~1.7 campaigns (~75% overcount). Never sum campaign orders across campaigns.
- **Merchant enrollment** only available for ~54% of campaigns (100% Smart Promo, ~50-80% ULC/Marketing, 0% Portal/Locations/Liquidity/Bolt+).
- **Campaign programs** (ULC, Marketplace, Liquidity, Bolt+) overlap and are NOT additive — only Type and Payer dimensions are MECE.
- **Bolt Spend ≈ Demand Incentives** but not identical (small delta from non-campaign demand subsidies).
- **Pure Bolt vs Cost-share**: Bolt spend = Pure Bolt (Bolt-initiated) + Cost-share (Bolt co-funding merchant campaigns). Target cost-share: >40% for Profit countries, >30% others.

---

## User Cohort Framework (Growth Framework 2.0)

### Cohort classification (4-week rolling window)
| Cohort | Definition | Notes |
|--------|-----------|-------|
| New | Activation date within 4-week window | |
| Light | 1 order (not new, not Plus) | |
| Medium | 2-3 orders (not new, not Plus) | |
| Heavy | 4-5 orders (not new, not Plus) | |
| Plus Ready | 6+ orders, no Bolt+ subscription | Best CP L2/order (~€0.31) |
| Plus | Active Bolt+ subscription (any order count) | ~40% frequency lift vs non-Plus |
| Inactive | 0 orders in 4-week window | |

### CP L2 at user level
`CP L2(user) = CP(city-level DE) × orders − DI(user-level)`
- CP per order from city-level (user-level Courier Earnings captures only ~64% of full CPO)
- DI per order reliable at user level (99.0% reconciliation)

### Bolt+ economics
- Revenue: +~€0.45/order commission uplift (23.7% vs 21.4%) + €3.96/month subscription fee (~€0.56/order)
- Cost: ~€1.24/order Bolt+ campaign DI
- Net per-order ≈ -€0.23, but frequency lift generates incremental CP

### Key upgrade rates (benchmarks)
- New → 2-in-4: 14%
- Occasional → Plus Ready: 5.6%/month
- Plus Ready → Plus: 5.3%/month

### LCS stages (from Eater Churn Model)
| Stage | Churn Probability | ULC Channel |
|-------|-------------------|-------------|
| Signup | <= 14d from signup | Activation |
| Never Activated | >14d, 0 orders | Activation |
| Engagement | Churn prob <= 80% | Engagement |
| Churning | 80% < prob <= 92% | Reactivation |
| Not Active | prob > 92% | Reactivation |
Further split by Conversion rank (1-3) and Profitability rank (1-3).
Source: `etl_eater_cohorts_lcs_weekly_by_city`

### Retention Metrics (from Looker / fact tables)
```
Order Retention:
  ├── 7d Retention Rate (% orders with repeat order within 7 days)
  ├── 30d Retention Rate (% orders with repeat order within 30 days)
  ├── 7d Loyalty Rate (% orders that had a previous order in prior 7 days)
  ├── 30d Loyalty Rate (% orders that had a previous order in prior 30 days)
  ├── 7d Loyalty Retention Rate (% core orders with repeat in prior 7 days)
  └── 30d Loyalty Retention Rate (% core orders with repeat in prior 30 days)

Same-entity Retention (brand/provider/business segment):
  ├── Same Brand 30d Retention/Loyalty Rate
  ├── Same Provider 30d Retention/Loyalty Rate
  └── Same Business Segment 30d Retention/Loyalty Rate

User Retention:
  ├── Core User 30d City Retention (activated 90+ days ago, reordered in same city within 30d)
  ├── Core User 30d Zonal Retention (same but zone-level)
  └── New User 5wk Retention (activated <90d ago, ordered in 5th week after activation)
```

### User Growth & Engagement Metrics (from Looker / fact tables)
```
Acquisition Funnel:
  App Installs → Signups → Activations
  Signup-to-Activation Rate

Active Users:
  ├── Active Users Count (delivery)
  ├── Active Users Food / Store / Store 1P / Store 3P ENT / Store 3P MM&SMB
  └── Active Users Bolt Plus Count

User Engagement:
  ├── Cross-vertical Users (ordered from food AND store)
  ├── Food Exclusive Users / Store Exclusive Users
  ├── User Deliveries Unique Merchant Count (merchant diversity)
  └── User Order Frequency (orders / active users)

Bolt Plus Subscription:
  ├── First Subscriptions Count (new subscribers)
  ├── Renewed Subscriptions Count (resubscribers after gap)
  └── Churned Count (90+ day gap between sub end and next sub start or today)
```

---

## Service Quality (CVP: Service)

Bad orders cost ~1% of GMV. Users with bad orders have **~8.5pp lower 30-day reorder rate**.

### Bad order rate decomposition (by actor at fault)
- **Provider at fault**: failed (did not respond, rejected after accept), missing/wrong items, late preparation
- **Courier at fault**: failed during delivery, late delivery, quality/handling
- **Platform/Other**: no courier found, system issues
- **Eater**: cancelled by customer

### Order quality metrics (from Looker / fact tables)
```
Bad Order Rate (share of orders labelled as bad)
  ├── Failed Order Rate
  │     ├── Failed (Merchant) — provider didn't respond or rejected
  │     ├── Failed (Bolt & Courier) — courier/platform failure
  │     └── Failed (Eater) — cancelled by customer
  ├── Late Delivery Order Rate (delivered after initial ETA upper bound)
  │     ├── Late Delivery -5 Min Rate (up to 5 min late)
  │     ├── Late Delivery 5-10 Min Rate
  │     └── Late Delivery 10min+ Rate ← key target: <5%
  ├── Late Pickup Order Rate (picked up 5+ min after food ready)
  │     ├── Late Pickup Courier Late Rate (courier was late)
  │     └── Late Pickup Merchant Early Rate (merchant prepared faster than estimated)
  │     ├── Late Pickup 5-10 Min Rate
  │     ├── Late Pickup 10-15 Min Rate
  │     └── Late Pickup 15min+ Rate
  ├── Bad Rating Order Rate (1-3 star courier OR merchant rating)
  │     ├── Bad Courier Rating Rate
  │     └── Bad Merchant Rating Rate
  ├── CS Ticket Order Rate (any eater CS ticket)
  │     ├── Missing Items Ticket Rate
  │     ├── Order Quality Ticket Rate
  │     ├── Delivery Quality Ticket Rate (courier actions)
  │     └── Timing Quality Ticket Rate (delays)
  └── Item Adjustment Order Rate (at least one item adjusted)
        └── Item Replacement Order Rate

Honey Order Rate = share of orders labelled as good (opposite of Bad Order Rate)
Bad Order Provider Rate = bad merchant rating OR missing/wrong item ticket OR refund > 0
```

### Order drop-off: Placed → Delivered
```
Placed Orders
  ├── Failed Orders (merchant/courier/eater fault)
  ├── Rejected Orders (provider rejected)
  └── Delivered Orders
```

### ETA Accuracy Metrics (from Looker / fact tables, all weighted averages)
```
Eater ETA Accuracy Rate (1 - share of inaccurate ETAs)
  ├── Checkout ETA: Avg Error, Avg Absolute Error, Range, In-Range %, Missing Rate
  ├── Initial ETA (at assignment): Avg Error, Avg Absolute Error, Range, In-Range %, Missing Rate
  ├── Accepted ETA: Avg Error, Avg Absolute Error, Missing Rate
  ├── Matched ETA: Avg Error, Avg Absolute Error, Missing Rate
  └── Search ETA: Avg Error, Avg Absolute Error, Missing Rate

Merchant ETA: Avg Duration, Avg Error, Avg Absolute Error
  ├── Late Preparation 5-10 Rate
  └── Late Preparation 10min+ Rate

Courier ETA:
  ├── Pickup ETA: Avg Error, Avg Absolute Error, Missing Rate
  ├── Dropoff ETA: Avg Error, Avg Absolute Error, Missing Rate
  └── Courier Arrival Time vs Merchant ETA (gap in minutes)
```

### Customer Support Metrics
```
Delivery CCPO (contacts per order)
  ├── Food CCPO
  └── Store CCPO
Delivery CCPO Manual Resolution (manual-only contacts per order)
Average Handling Time (minutes per ticket)
CSAT Positive Response Rate
CSAT Response Rate
FRT Live Orders P75 (first response time, 75th percentile)
```

### Key targets (GM Summit)
- Bad order rate: <10% (current: ~14.9%)
- Late delivery 10min+: <5%
- CSAT: >60

---

## Standard Query Templates

### Monthly Country P&L (matches Looker exactly)
```sql
SELECT
    metric_timestamp_partition AS month,
    ROUND(SUM(total_gmv_before_discounts_eur), 0) AS gmv_eur,
    ROUND(SUM(total_contribution_profit_eur) / NULLIF(SUM(total_gmv_before_discounts_eur), 0) * 100, 2) AS cp_margin_pct,
    ROUND(SUM(total_contribution_profit_without_demand_incentives_eur), 0) AS cp_l2_eur,
    ROUND(SUM(total_contribution_profit_without_demand_incentives_eur) / NULLIF(SUM(total_gmv_before_discounts_eur), 0) * 100, 2) AS cp_l2_margin_pct,
    ROUND(SUM(total_invoiced_demand_incentives_eur) / NULLIF(SUM(total_gmv_before_discounts_eur), 0) * 100, 2) AS di_pct_gmv,
    ROUND(SUM(total_invoiced_courier_costs_eur) / NULLIF(SUM(courier_delivered_orders_count), 0), 2) AS cpo_eur
FROM ng_delivery_spark.fact_delivery_country_monthly     -- USE MONTHLY TABLE for monthly reporting
WHERE country_code = '<COUNTRY>'
  AND delivery_vertical IN ('food', 'store_3p_ent', 'store_3p_mm_smb')  -- "Bolt Food" = food + 3P stores
  AND metric_timestamp_partition >= '<START>'
  AND metric_timestamp_partition < '<END>'
GROUP BY metric_timestamp_partition
ORDER BY month
```

### Weekly Country Trend
```sql
SELECT
    metric_timestamp_partition AS week_start,
    ROUND(SUM(total_gmv_before_discounts_eur), 0) AS gmv_eur,
    ROUND(SUM(total_contribution_profit_eur) / NULLIF(SUM(total_gmv_before_discounts_eur), 0) * 100, 2) AS cp_margin_pct,
    ROUND(SUM(total_contribution_profit_without_demand_incentives_eur), 0) AS cp_l2_eur
FROM ng_delivery_spark.fact_delivery_country_weekly      -- USE WEEKLY TABLE for weekly reporting
WHERE country_code = '<COUNTRY>'
  AND delivery_vertical IN ('food', 'store_3p_ent', 'store_3p_mm_smb')
  AND metric_timestamp_partition >= '<START>'
  AND metric_timestamp_partition < '<END>'
GROUP BY metric_timestamp_partition
ORDER BY week_start
```

### Country Operational Metrics (sessions, courier, funnel)
```sql
SELECT
    f.metric_timestamp_partition AS month,
    ROUND(SUM(f.sessions_all_users_count), 0) AS sessions,
    ROUND(SUM(f.order_placed_rate_value * f.order_placed_rate_weight)
          / NULLIF(SUM(f.order_placed_rate_weight), 0) * 100, 2) AS session_to_order_pct,
    ROUND(SUM(f.courier_utilisation_rate_value * f.courier_utilisation_rate_weight)
          / NULLIF(SUM(f.courier_utilisation_rate_weight), 0) * 100, 2) AS courier_util_pct,
    ROUND(SUM(f.session_search_usage_rate_value * f.session_search_usage_rate_weight)
          / NULLIF(SUM(f.session_search_usage_rate_weight), 0) * 100, 2) AS search_usage_pct,
    ROUND(SUM(f.session_provider_rs_closure_rate_value * f.session_provider_rs_closure_rate_weight)
          / NULLIF(SUM(f.session_provider_rs_closure_rate_weight), 0) * 100, 2) AS rs_closure_pct
FROM ng_delivery_spark.fact_delivery_city_monthly f           -- CITY level, not country
JOIN ng_delivery_spark.dim_delivery_city c ON f.city_id = c.city_id
WHERE c.country_code = '<COUNTRY>'
  AND f.delivery_vertical = 'delivery'                        -- NOT 'food'
  AND f.metric_timestamp_partition >= '<START>'
  AND f.metric_timestamp_partition < '<END>'
GROUP BY f.metric_timestamp_partition
ORDER BY month
```

Available funnel steps (all at city level, delivery vertical, weighted averages):
- `session_search_usage_rate` -- % sessions using search
- `provider_viewed_rate` -- % sessions viewing a provider
- `product_added_rate` -- % sessions adding to cart
- `cart_viewed_rate` -- % sessions viewing cart
- `checkout_started_rate` / `checkout_completed_rate` -- checkout funnel
- `order_placed_rate` -- overall session-to-order conversion
- Step-to-step: `order_placed_from_provider_viewed_rate`, `order_placed_from_checkout_completed_rate`, etc.
- Food-specific: `food_order_placed_from_provider_viewed_rate`

### Session Selection & Supply Constraint Metrics (city level, delivery vertical)
```
Selection / Availability:
  ├── Median Merchant Count Shown per Session (food / store / total)
  ├── Median Merchant Within 4km Count Shown per Session
  ├── Unique Merchants Viewed per Session (converted vs unconverted)
  ├── Unique Merchants Viewed Before Product Added per Session
  ├── Zero Available Providers Instance Search Rate (search returned 0 results)
  └── Time to 1st Merchant Viewed per Session (minutes)

Supply Constraints / Estimated Lost Orders:
  ├── Estimated Orders Lost From Eater Surge (surge pricing on delivery fee)
  ├── Estimated Orders Lost From Pause Demand Incentives (DI campaigns paused)
  └── Estimated Orders Lost From Radius Shrinkage (temporary radius reduction)

Session Weighted Metrics:
  ├── Busy Ratio (active orders / online couriers per session)
  ├── Delivery Fee Dynamic Multiplier (surge multiplier on DF)
  ├── Courier Earnings Dynamic Multiplier (surge multiplier on earnings)
  ├── Per-Merchant Closure Rate (PPC-closed merchants / total merchants)
  └── Radius Shrinkage Rate (radius-shrunk merchants / total merchants)
```

### Merchant Performance Metrics (from Looker / fact tables)
```
Merchant Acceptance:
  ├── Merchant Acceptance Rate
  ├── Merchant Acceptance Time (minutes to accept)
  ├── Merchant Late Acceptance 5min+ Rate
  ├── Merchant Did-Not-Respond Orders Count
  └── Merchant Rejected Orders Count

Merchant Processing:
  └── Merchant Processing Time (proposed → preparation finished, minutes)

Merchant Availability:
  ├── Merchant Availability Rate (% of working hours active)
  ├── Merchant Active Duration / Inactive Duration (minutes)
  ├── Per Merchant Closure Rate (PPC closures)
  ├── Merchant PPC Closed Count
  └── Merchant SKU Sessions Availability Rate (session-weighted item availability)

Merchant Lifecycle:
  ├── Active Merchant Count / Active Top Brand Count
  ├── New Active Merchant Count (first-time active)
  ├── Active Merchants with <10 Orders Count / Rate
  ├── ELC Active Merchant Count (early lifecycle merchants)
  ├── ELC Merchants Orders Delivered
  ├── Delivered Orders per Merchant
  ├── PoP Merchant Churn Count / Rate (active → inactive period-over-period)
  ├── PoP Merchant Resurrected Count
  ├── Merchant Churn Count / Resurrected Count (absolute)
  └── Merchant Deliveries Unique User Count
```

### Bolt Plus GMV Share
```sql
ROUND(SUM(bolt_plus_delivery_gmv_share_value * bolt_plus_delivery_gmv_share_weight)
      / NULLIF(SUM(bolt_plus_delivery_gmv_share_weight), 0) * 100, 2) AS bolt_plus_gmv_share_pct
```

### Campaign Spend by Objective
```sql
SELECT
    DATE_TRUNC('MONTH', order_created_date) AS month,
    spend_objective,
    ROUND(SUM(CAST(bolt_spend AS DOUBLE)), 0) AS bolt_spend_eur,
    ROUND(SUM(CAST(discount_value AS DOUBLE)), 0) AS total_discount_eur,
    COUNT(DISTINCT order_id) AS orders
FROM ng_public_spark.etl_delivery_campaign_order_metrics
WHERE country = '<COUNTRY>'
  AND order_created_date >= '<START>' AND order_created_date < '<END>'
GROUP BY 1, 2
ORDER BY 1, bolt_spend_eur DESC
```

### Weighted Average Metric Pattern
```sql
SUM(metric_value * metric_weight) / NULLIF(SUM(metric_weight), 0) AS metric
```

---

## Root-Cause Investigation Levels

### Level 0: North Star — Are We On Track?
First 3 questions every week. Everything else is a drill-down.

| Metric | Source | Column(s) |
|--------|--------|-----------|
| GMV | fact_delivery_country_weekly | total_gmv_before_discounts_eur |
| Orders | same | courier_delivered_orders_count |
| CP L2 | same | total_contribution_profit_without_demand_incentives_eur |
| CP L2 margin % | same | CP L2 / GMV |
| Food vs Store split | same | delivery_vertical filter |

### Level 1: GMV Decomposition
Is it an orders problem or an AOV problem?

| Check | Table | SQL Logic |
|-------|-------|-----------|
| Orders trend | fact_delivery_country_weekly | SUM(courier_delivered_orders_count) by period |
| AOV trend | same | SUM(total_gmv_before_discounts_eur) / SUM(courier_delivered_orders_count) |
| GMV bridge | same | ΔOrders × AOV_prev + Orders_curr × ΔAOV |
| City ranking | fact_delivery_city_weekly | Rank by absolute GMV delta; show % contribution to country change |
| Eater fee yield | same | eater_fee_revenue_gmv_share (weighted avg) |
| Discount rate | same | campaign_discount_gmv_share (weighted avg) |

### Level 2: Order Drivers
Why did orders change?

| Check | Table | Logic | Interpretation |
|-------|-------|-------|----------------|
| Active users | non_additive table | active_users_delivery_food_count | Fewer users = acquisition/retention issue |
| Frequency | non_additive table | delivered_orders_per_user | Lower freq = engagement issue |
| Sessions | city-level, delivery vertical | sessions_all_users_count | Fewer sessions = demand issue |
| Conversion | city-level, delivery vertical | order_placed_rate (weighted avg) | Lower conv = UX/pricing/supply issue |
| User cohort mix | etl_eater_cohorts_lcs_weekly_by_city | GROUP BY stage | Shift in LCS composition |
| Merchant closures | city-level, delivery vertical | session_provider_rs_closure_rate (weighted avg) | Higher = supply constraint |

### Level 3: Revenue & Cost Waterfall (CP L2)
Why did profitability change?

| Check | Table | SQL Logic |
|-------|-------|-----------|
| CP L2 bridge | fact_delivery_country_weekly | ΔCP vs −ΔDemand Incentives |
| Commission yield | same | provider_commission_gmv_share (weighted avg) |
| CPO | same | SUM(total_invoiced_courier_costs_eur) / SUM(courier_delivered_orders_count) |
| Demand incentive rate | same | SUM(total_invoiced_demand_incentives_eur) / SUM(total_gmv_before_discounts_eur) |
| Supply incentive rate | same | SUM(total_invoiced_supply_incentives_eur) / SUM(total_gmv_before_discounts_eur) |
| Refund rate | same | SUM(total_invoiced_refunds_eur) / SUM(total_gmv_before_discounts_eur) |
| Eater fee share | same | eater_fee_revenue_gmv_share (weighted avg) |
| GP margin | same | SUM(total_gross_profit_eur) / SUM(total_gmv_before_discounts_eur) |

### Level 4: Investment Deep-Dive
Why did spend/efficiency change?

| Check | Source |
|-------|--------|
| Campaign spend by objective | etl_delivery_campaign_order_metrics (spend_objective column, MECE) |
| Campaign lifecycle bridge | +New − Expired + ΔContinuing (from campaign-level data) |
| Campaign discount MECE | By Type: Menu/DF/SF. By Payer: Bolt/Merchant. |
| Bolt vs provider spend split | campaign_spend_bolt_gmv_share vs campaign_spend_provider_gmv_share |
| Pure Bolt vs Cost-share | Cost-share portion of Bolt menu/DF campaigns |
| Smart promo enrollment | fact_provider_smart_promo_offer_campaign_enrollment |
| Provider targeting features | etl_incentives_provider_targeting_features |

---

## Standard Cross-Cuts

### By Geography
```sql
-- Country-level: use fact_delivery_country_weekly with country_code filter
-- City-level: use fact_delivery_city_weekly, JOIN dim_delivery_city for names
-- Zone-level: use fact_delivery_zone_weekly
```

### By Provider / Brand
For brand-level analysis, use `etl_delivery_order_monetary_metrics` (order-grain) joined to `dim_provider_v2`:
```sql
SELECT
    CASE WHEN LOWER(p.provider_name) LIKE 'mcdon%' THEN 'McDonald''s'
         WHEN LOWER(p.provider_name) LIKE 'kfc%' THEN 'KFC'
    END AS brand,
    ...
FROM ng_public_spark.etl_delivery_order_monetary_metrics m
JOIN ng_delivery_spark.dim_provider_v2 p ON m.provider_id = p.provider_id
WHERE brand IS NOT NULL
GROUP BY brand
```

### By User Cohort (LCS)
Source: `etl_eater_cohorts_lcs_weekly_by_city` — GROUP BY stage for lifecycle distribution.

### By User Type (Bolt Plus)
| Segment | Source |
|---------|--------|
| Bolt Plus users | non_additive: active_users_delivery_bolt_plus_count |
| Bolt Plus GMV share | additive: bolt_plus_delivery_gmv_share (weighted avg) |
| Subscriptions | fact_user_subscriptions (core_models_spark) |

---

## Key Benchmarks (from GM Summit)

| Metric | Target / Benchmark | Source |
|--------|-------------------|--------|
| YoY GMV Growth | ~25% | Strategy goal |
| Profitability (CP L2 > 0) | By Oct 2026 | Strategy goal |
| Bad Order Rate | <10% | Ops target (currently ~14.9%) |
| Late Delivery 10min+ | <5% | Ops target |
| Bad Order Retention Impact | ~8.5pp reorder gap | 2026 Vision |
| Restaurant Commission | 22.0% of AOV | Merchant target (currently ~21.5%) |
| Bolt+ GMV Share | ~22% | Global benchmark |
| Bolt+ Frequency Lift | ~40-50% vs non-B+ | Observed |
| Merchant Churn | ~3% | 2025 average |
| New User 2-in-4 Rate | Improve from 14% | Growth Framework 2.0 |
| Store GMV Share | 9% of Delivery GMV | 2026 target (currently ~7%) |
| Cost-share (Profit countries) | >40% | Growth Framework |
| Cost-share (Others) | >30% | Growth Framework |
| ICP ROI targets | 0.5-0.7 | Depends on country segment |
| CSAT | >60 | Summit (currently ~60) |
| Merchant churn signal | <10 orders/week = high churn probability | |
| Bad order cost | ~EUR 4.00/order (CS + refunds + lost retention) | |
| CPO lever | Reducing CDT by 2 min saves ~EUR 0.30/order | |

---

## Cross-Reference Map

| If you're in... | And find... | Jump to... |
|-----------------|-------------|------------|
| GMV Decomposition | Orders drove the change | Users & Cohorts (user lens) or Conversion Funnel (session lens) |
| CP L2 | Courier costs drove CP change | CPO decomposition |
| CP L2 | Refunds growing | Service Quality (what's causing bad orders?) |
| CP L2 | Demand Incentives changed | Campaign Deep Dive |
| Conversion Funnel | Discovery dropped (MV→PA) | CVP: Selection |
| Conversion Funnel | Checkout dropped (CV→CS) | CVP: Value (prices/fees) |
| Conversion Funnel | Placed→Delivered dropped | CVP: Service (failed/rejected) |
| CVP: Value | Discount depth changing | Campaign Deep Dive |
| CVP: Service | Provider at fault dominates | Selection: Merchant ops health |
| CVP: Service | Courier at fault dominates | CPO: Courier supply & operations |
| CPO | Utilization dropping | Courier supply health |
| CPO | Merchant wait growing in CDT | Selection: Merchant processing time |
| Geo Investment | City underperforming | Run full issue tree for that city |
| Users & Cohorts | Need user-level profitability | User cohort CP L2 analysis |
| CP L2 | DI is growing — who is it going to? | DI spend leak analysis |

---

## Campaign Spend Objectives Reference

| Objective | Owner | Purpose |
|-----------|-------|---------|
| activation | Growth | New user first order |
| reactivation | Growth | Bring back inactive users |
| engagement | Growth | Keep active users ordering |
| churn | Growth | User churn prevention |
| liquidity | Growth | City/zone-wide marketplace push |
| marketing | Marketing/Growth | Promo codes, influencers |
| provider_campaign_ELC_merchant | Growth | Merchant early lifecycle (first 30 days) |
| provider_campaign_churn_prevention | Growth | Merchant churn prevention |
| provider_campaign_commission_increase | Growth | Support commission increase negotiations |
| provider_campaign_portal | Growth | Merchant self-service campaigns |
| provider_campaign_profit_generator | Growth | Shift orders to high-commission merchants |
| provider_campaign_sales_benefit | Growth | Contractual sales benefits |
| bolt_market_* | Growth | Bolt Market specific campaigns |

---

## Brand / Provider Investment Analysis

To analyze demand incentive spend into specific brands or merchants:

1. **Find providers**: Match brand by name in `dim_provider_v2` using `LOWER(provider_name) LIKE 'pattern%'`
   - McDonald's → `'mcdon%'`, KFC → `'kfc%'`, Bageterie Boulevard → `'bageterie boulevard%'`
   - IC chains have many locations; always aggregate at brand level using CASE
2. **Join to order-level metrics**: `JOIN dim_provider_v2 p ON m.provider_id = p.provider_id`
   (use `etl_delivery_order_monetary_metrics` for brand-level drill-downs since fact tables don't have provider grain)
3. **Key columns for spend analysis** (order-level table):
   - Bolt-funded: `bolt_delivery_campaign_cost_eur + bolt_menu_campaign_cost_eur`
   - Merchant-funded: `provider_delivery_campaign_cost_eur + provider_menu_campaign_cost_eur`
   - Total: `total_discount_eur`
   - Express as % of GMV for comparability
4. **Cost-share assessment**: merchant_spend / (bolt_spend + merchant_spend)
   - Target: >40% for Profit countries, >30% for others
   - Zero merchant spend = red flag for cost-share negotiation

Saved query template: `saved_queries/brand_demand_incentive_spend.sql`

---

## Experiment / A-B Test Analysis

### Tables
- **Enrollments**: `etl_delivery_campaigns_enrollments` — who was enrolled in which test/treatment
- **Scorecard**: `etl_delivery_campaigns_ab_scorecard_lcs` — pre-calculated results per treatment

### Key scorecard metrics
- GMV, NMV, finished_orders (treatment vs control)
- Uplift (absolute): gmv_uplift, finished_orders_uplift, active_eaters_uplift
- P-values: gmv_p_value, finished_orders_p_value, active_eater_p_value (also _hp variants for holdout period)
- UC ratio: uc_ratio_bolt (Bolt spend GMV U/C), uc_ratio_total (total spend GMV U/C)
- Contribution profit: contribution_profit_percentage, incremental_contribution_profit_eur
- Conversion: conversion_rate, conversion_rate_control

### Combining multiple treatments
When aggregating across multiple treatments/tests:
```sql
-- Combined GMV U/C (Bolt)
SUM(gmv_uplift) / NULLIF(SUM(bolt_cost_uplift), 0) AS combined_uc_ratio_bolt

-- Combined net activation rate
SUM(users_enrolled * conversion_rate) / NULLIF(SUM(users_enrolled), 0)
- SUM(users_enrolled_control * conversion_rate_control) / NULLIF(SUM(users_enrolled_control), 0)
  AS combined_net_activation_rate

-- Combined activation rate
SUM(users_enrolled * conversion_rate) / NULLIF(SUM(users_enrolled), 0) AS combined_activation_rate
```

### Holdout period metrics
Columns with `_hp` suffix = holdout period (after campaign ends). Use to assess lasting impact vs during-campaign only.

---

## Known Gaps & Calibration Notes

1. **ULC campaign discount % of GMV**: The `campaign_discount_gmv_share` weighted average from fact tables gives ~19-21%, but Looker's "ULC campaign discount" shows slightly different values (~20.5%, 19.0%, 22.2% for CZ Nov-Jan). The exact Looker definition likely includes additional discount sources (cashback coupons, etc.) or uses a different aggregation. Treat fact-table campaign_discount as a close proxy (~0.5-1.5pp deviation).
2. **A/B test scorecard**: Available via `etl_delivery_campaigns_ab_scorecard_lcs` (pre-calculated uplift, p-values, UC ratios). For raw enrollment data, use `etl_delivery_campaigns_enrollments`. ICP ROI may differ from scorecard U/C.
3. **Session/courier metrics at country level**: Always NULL. Must query at city level with `delivery_vertical = 'delivery'` and join dim_delivery_city for country filter.
4. **Campaign orders overlap**: One order triggers ~1.7 campaigns. Campaign order counts are NOT additive across campaigns (~75% overcount).
5. **Merchant enrollment**: Only available for ~54% of campaigns. Full coverage for Smart Promo; partial for ULC/Marketing; zero for Portal/Locations/Liquidity/Bolt+.
6. **CP L2 at user level**: User-level Courier Earnings captures only ~64% of full CPO. Always use city-level CP for user profitability calculations.
7. **CPO denominator**: Courier Delivered Orders ≠ User Delivered Orders (~5% gap). Always use Courier Delivered Orders.
8. **Demand Incentives ≈ Bolt Spend**: Small delta from non-campaign demand subsidies. Not exactly identical.

---

## Investigation Workflow

When asked to analyze a metric movement:

1. **Quantify the change** -- WoW, MoM, YoY, trailing 4-week. Show absolute and %. Compare to ATB.
2. **Decompose top-down** -- GMV → orders vs AOV → users vs frequency. CP L2 → CP vs DI.
3. **Cut by dimensions** -- city (show % contribution), provider/brand, user cohort to isolate where the change concentrates
4. **Check campaigns** -- did spend change? New campaigns launched? Campaigns ended? Lifecycle bridge.
5. **Check supply side** -- merchant count changes, closures, new launches, churn
6. **Check external factors** -- holidays, weather, competitor moves, seasonality
7. **Quantify impact** -- attribute EUR impact to each driver
8. **Connect to CP L2** -- what's the profitability implication? CP L2 is the north star.
