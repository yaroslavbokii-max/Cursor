# Looker Explores Datasources Guide

This guide provides an overview of all available Looker explores (datasources) in Bolt Food, organized by type and use case. This knowledge base helps you:

1. **Identify the Right Datasource**: Find which explore to use for your specific business question
2. **Understand Use Cases**: Learn what each datasource is designed for
3. **Navigate Looker**: Know where to find each explore and who to contact for questions

---

## Overview

This manual provides guidance for users to effectively use the curated explores in Looker. The curated explores have names starting with a "⭐" to distinguish them from legacy explores. The curated explores are organized into two categories:

- **⭐ Information Explores** - Dimensional data for detailed analysis and filtering
- **📊 Metrics Explores** - Pre-calculated metrics with time-based aggregations

---

## When to Use Each Type

### Use Information Explores When:

- ✓ Performing detailed data exploration
- ✓ Creating complex filters or segments
- ✓ Investigating specific cases or outliers

### Use Metrics Explores When:

- ✓ You need aggregated performance data
- ✓ Building dashboards or reports with KPIs
- ✓ Analysing trends over time

---

## 📊 Metrics Explores

Metrics Explores contain **pre-aggregated metrics** at various time granularities from hourly to monthly. These are optimized for:

- Building dashboards and reports with KPIs
- Analyzing trends over time
- Quick performance monitoring

### Key Features of Metrics Explores:

1. **Pre-aggregated data** - Faster queries, optimized for reporting
2. **Time granularity options** - Hourly, daily, weekly, monthly (with historical archive option)
3. **Additive & Non-additive metrics** - Understand which metrics can be aggregated
4. **Information views integration** - Additional dimensions for grouping
5. **Entity granularity** - Switch between zone, city, country, and global metrics (in The Delivery Explore)
6. **Slicer functionality** - Access regional metrics for sub-verticals (Food, Store 1P, etc.)

### Available Metrics Explores:

#### ⭐ The Delivery Explore

**Looker Link**: [fact_delivery](https://bolt.cloud.looker.com/explore/curated_delivery/fact_delivery)

**Purpose**: Zone, city, country and global metrics

**Owner**: Zhanna Azizova & Bram Verhoef

**Use Cases**:
- High-level performance monitoring across all delivery operations
- Zone-level, city-level, country-level, or global metrics analysis
- Cross-vertical analysis (Food, Store 1P, etc.) using slicers
- Business-critical dashboards requiring pre-aggregated data

---

#### ⭐ Metrics - Campaigns

**Looker Link**: [fact_campaign](https://bolt.cloud.looker.com/explore/curated_delivery/fact_campaign)

**Purpose**: Metrics on campaign level

**Owner**: James Davies & Bram Verhoef

**Use Cases**:
- Campaign performance analysis and ROI
- Campaign spend tracking (Bolt-funded vs Merchant-funded)
- Campaign discount analysis
- Campaign enrollment metrics

---

#### ⭐ Metrics - Couriers

**Looker Link**: [fact_courier](https://bolt.cloud.looker.com/explore/curated_delivery/fact_courier)

**Purpose**: Metrics on courier or fleet level

**Owner**: Mohammadhasan Farazmand & Bram Verhoef

**Use Cases**:
- Courier utilization and efficiency metrics
- Courier earnings analysis
- Fleet-level performance tracking
- Courier acceptance and completion rates
- Courier online hours and utilized hours

---

#### ⭐ Metrics - Merchants

**Looker Link**: [fact_provider](https://bolt.cloud.looker.com/explore/curated_delivery/fact_provider)

**Purpose**: Metrics on merchant or brand level

**Owner**: Wahaj Baig & Amruth Anand

**Use Cases**:
- Merchant-level KPIs and performance metrics
- Brand-level aggregations
- Merchant GMV and commission analysis
- Merchant acceptance rates and order volumes
- Menu quality metrics (photo coverage, description coverage)

---

#### ⭐ Metrics - Users

**Looker Link**: [fact_user](https://bolt.cloud.looker.com/explore/curated_delivery/fact_user)

**Purpose**: Metrics on user level

**Owner**: Ansh Jain & Bram Verhoef

**Use Cases**:
- User behavior and retention metrics
- User activation and growth tracking
- User lifecycle analysis
- User order frequency and AOV
- Session-to-order conversion metrics

---

## ⭐ Information Explores

Information Explores contain **detailed dimensional information** about entities (e.g., orders, couriers, merchants). These are optimized for:

- Performing detailed data exploration
- Creating complex filters or segments
- Investigating specific cases or outliers

### Key Features of Information Explores:

1. **Detailed dimensional data** - Access to granular entity-level information
2. **Flexible filtering** - Complex segmentation capabilities
3. **500+ dimensions** - Rich context for deep-dive analysis
4. **Time basis selection** - Choose the timestamp that fits your analysis
5. **Report date filter** - Mandatory filter that enhances query efficiency
6. **Primary and secondary views** - Main view plus integrated secondary views for additional analysis

### Available Information Explores:

#### ⭐ Info - Basket Items

**Looker Link**: [dim_courier](https://bolt.cloud.looker.com/explore/curated_delivery/dim_courier)

**Owner**: Giacomo Leo

**Use Cases**:
- Item-level basket analysis
- Dish composition and modifiers analysis
- Item pricing before/after discounts
- Basket size and item count analysis
- Item-level campaign discount tracking

---

#### ⭐ Info - Couriers

**Looker Link**: [dim_courier](https://bolt.cloud.looker.com/explore/curated_delivery/dim_courier)

**Owner**: Mohammadhasan Farazmand & Bram Verhoef

**Use Cases**:
- Individual courier performance analysis
- Courier-level deep dives and outlier investigation
- Detailed courier acceptance and delivery patterns
- Courier earnings breakdown
- Courier vehicle type analysis

---

#### ⭐ Info - Courier Fleets

**Looker Link**: [dim_courier_fleet](https://bolt.cloud.looker.com/explore/curated_delivery/dim_courier_fleet)

**Owner**: Mohammadhasan Farazmand & Bram Verhoef

**Use Cases**:
- Fleet-level courier management
- Fleet performance analysis
- Fleet operations and coordination

---

#### ⭐ Info - Courier Leads

**Looker Link**: [dim_courier_lead](https://bolt.cloud.looker.com/explore/curated_delivery/dim_courier_lead)

**Owner**: Kamilya Kosset & Bram Verhoef

**Use Cases**:
- Courier recruitment and lead tracking
- Courier lead conversion analysis
- Courier onboarding metrics

---

#### ⭐ Info - Menu Items

**Looker Link**: [dim_provider_active_menu_item](https://bolt.cloud.looker.com/explore/curated_delivery/dim_provider_active_menu_item)

**Owner**: Wahaj Baig & Amruth Anand

**Use Cases**:
- Menu item details and pricing
- Menu item availability analysis
- Menu item performance tracking
- Menu quality metrics

---

#### ⭐ Info - Merchants

**Looker Link**: [dim_provider](https://bolt.cloud.looker.com/explore/curated_delivery/dim_provider)

**Owner**: Wahaj Baig & Amruth Anand

**Use Cases**:
- Merchant attributes and details
- Merchant-level deep-dive analysis
- Merchant lifecycle tracking (ELC, etc.)
- Merchant availability and operations
- Brand-level analysis

---

#### ⭐ Info - Merchant Leads

**Looker Link**: [dim_provider_lead_onboarding_case](https://bolt.cloud.looker.com/explore/curated_delivery/dim_provider_lead_onboarding_case)

**Owner**: Wahaj Baig & Amruth Anand

**Use Cases**:
- Merchant lead conversion tracking
- Onboarding SLA analysis (24hr qualification, 72hr asset delivery, etc.)
- Merchant ops escalation tracking
- Lead-to-onboard funnel analysis

---

#### ⭐ Info - Orders

**Looker Link**: [dim_order_delivery](https://bolt.cloud.looker.com/explore/explore/curated_delivery/dim_order_delivery)

**Owner**: Mohammadhasan Farazmand & Bram Verhoef

**Use Cases**:
- Order-level deep-dive analysis
- Detailed order investigation (500+ dimensions available)
- Order quality and timing analysis
- Order-level campaign and discount tracking
- Order status and lifecycle tracking
- Courier-order relationships

---

#### ⭐ Info - Orders x Campaigns

**Looker Link**: [dim_order_campaign_delivery](https://bolt.cloud.looker.com/explore/curated_delivery/dim_order_campaign_delivery)

**Owner**: James Davies & Bram Verhoef

**Use Cases**:
- Order-campaign relationship analysis
- Campaign effectiveness at order level
- Campaign discount and spend tracking per order
- Campaign enrollment and merchant participation

---

#### ⭐ Info - PIM Catalog SKUs

**Looker Link**: [dim_order_delivery](https://bolt.cloud.looker.com/explore/curated_delivery/dim_order_delivery)

**Owner**: Giacomo Leo

**Use Cases**:
- Product Information Management catalog data
- SKU-level product details
- Catalog item tracking

---

#### ⭐ Info - Sessions

**Looker Link**: [dim_session_user_delivery_mixpanel](https://bolt.cloud.looker.com/explore/curated_delivery/dim_session_user_delivery_mixpanel)

**Owner**: Ansh Jain & Bram Verhoef

**Use Cases**:
- User session-level behavior analysis
- Session flow and conversion funnel
- Merchant selection and browsing patterns
- Session-to-order conversion analysis
- User journey tracking

---

#### ⭐ Info - Store documents

**Looker Link**: [dim_store_document_item](https://bolt.cloud.looker.com/explore/curated_delivery/dim_store_document_item)

**Owner**: Alexander Stolnikov & Giacomo Leo

**Use Cases**:
- Store document item-level data
- Store document analysis
- Store inventory and document tracking

---

#### ⭐ Info - Users

**Looker Link**: [dim_user_delivery](https://bolt.cloud.looker.com/explore/curated_delivery/dim_user_delivery)

**Owner**: Ansh Jain & Bram Verhoef

**Use Cases**:
- User-level detailed analysis
- User attributes and segmentation
- User lifecycle tracking
- User activation and retention analysis
- User order history and behavior

---

## Use Case Guide

### Common Business Questions and Recommended Explores

#### "I need to analyze order performance trends"
- **Use**: ⭐ The Delivery Explore (Metrics)
- **Why**: Pre-aggregated order metrics with time-based analysis, supports zone/city/country/global views
- **Alternative**: ⭐ Info - Orders (for detailed order-level analysis with 500+ dimensions)

#### "I want to understand courier utilization and performance"
- **Use**: 📊 Metrics - Couriers
- **Why**: Pre-calculated courier performance metrics at courier or fleet level
- **Alternative**: ⭐ Info - Couriers (for individual courier details and deep-dive analysis)

#### "I need merchant-level performance data"
- **Use**: 📊 Metrics - Merchants
- **Why**: Aggregated merchant metrics ready for analysis at merchant or brand level
- **Alternative**: ⭐ Info - Merchants (for merchant attributes and detailed analysis)

#### "I want to analyze campaign effectiveness"
- **Use**: 📊 Metrics - Campaigns or ⭐ Info - Orders x Campaigns
- **Why**: Campaign-level metrics and order-campaign relationships
- **Alternative**: ⭐ Info - Orders (for order-level campaign data)

#### "I need user behavior and retention metrics"
- **Use**: 📊 Metrics - Users
- **Why**: Pre-aggregated user metrics at user level
- **Alternative**: ⭐ Info - Users or ⭐ Info - Sessions (for detailed user journey)

#### "I want to analyze basket composition and items"
- **Use**: ⭐ Info - Basket Items
- **Why**: Detailed item-level data for basket analysis

#### "I need session-level user behavior"
- **Use**: ⭐ Info - Sessions
- **Why**: Detailed session data with user journey information

#### "I want merchant onboarding metrics and SLA tracking"
- **Use**: ⭐ Info - Merchant Leads
- **Why**: Lead-to-onboard conversion tracking and onboarding SLA metrics

#### "I need menu item analysis"
- **Use**: ⭐ Info - Menu Items
- **Why**: Detailed menu item data and pricing information

#### "I want courier fleet analysis"
- **Use**: ⭐ Info - Courier Fleets
- **Why**: Fleet-level courier data and management

#### "I need courier lead tracking"
- **Use**: ⭐ Info - Courier Leads
- **Why**: Courier lead conversion and onboarding metrics

#### "I want store document analysis"
- **Use**: ⭐ Info - Store documents
- **Why**: Store document item-level data

#### "I need PIM catalog SKU data"
- **Use**: ⭐ Info - PIM Catalog SKUs
- **Why**: Product information management catalog data

---

## Important Notes

### Access Requirements

All users must request explore access to the `curated_delivery` model in Looker. To check your access status, visit any explore link above. If you lack access, submit a ticket to the IT service desk under 'Additional access / new account'.

### Best Practices

1. **Use Metrics Explores for dashboards** - They're optimized for reporting and KPIs
2. **Use Information Explores for deep dives** - When you need detailed analysis or specific filters
3. **Check metric documentation** - Each metric in Metrics Explores links to the underlying Information Explore for detailed analysis
4. **Contact explore owners** - Reach out via #food-analytics for questions about specific explores
5. **Understand additive vs non-additive metrics** - Non-additive metrics require the metric key dimension to be selected

### Getting Help

- **General questions**: Contact explore owners listed above via #food-analytics
- **Access issues**: IT service desk
- **Complex questions**: Reach out to Bram Verhoef or Zhanna Azizova

---

## Quick Reference Table

| Business Need | Recommended Explore | Type | Use Case |
|--------------|-------------------|------|----------|
| Order trends & KPIs | ⭐ The Delivery Explore | Metrics | High-level performance monitoring |
| Courier performance | 📊 Metrics - Couriers | Metrics | Courier utilization and efficiency |
| Merchant performance | 📊 Metrics - Merchants | Metrics | Merchant-level KPIs |
| Campaign analysis | 📊 Metrics - Campaigns | Metrics | Campaign ROI and effectiveness |
| User metrics | 📊 Metrics - Users | Metrics | User behavior and retention |
| Detailed order analysis | ⭐ Info - Orders | Information | Order-level deep dive |
| User journey analysis | ⭐ Info - Sessions | Information | Session flow and conversion |
| Basket analysis | ⭐ Info - Basket Items | Information | Item-level basket composition |
| Merchant details | ⭐ Info - Merchants | Information | Merchant attributes and details |
| Courier details | ⭐ Info - Couriers | Information | Individual courier analysis |
| Campaign-order relationships | ⭐ Info - Orders x Campaigns | Information | Order-campaign mapping |
| Merchant onboarding | ⭐ Info - Merchant Leads | Information | Lead conversion tracking |
| Menu analysis | ⭐ Info - Menu Items | Information | Menu item details and pricing |
| Courier fleet management | ⭐ Info - Courier Fleets | Information | Fleet-level operations |
| Courier lead tracking | ⭐ Info - Courier Leads | Information | Courier recruitment |
| Store documents | ⭐ Info - Store documents | Information | Store document items |
| PIM catalog | ⭐ Info - PIM Catalog SKUs | Information | Product catalog data |

---

*Last updated: Based on Looker Explores Manual*
