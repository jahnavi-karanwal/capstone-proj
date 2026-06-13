# Data Dictionary – Mutual Fund Analytics

## Project Overview

This document describes the datasets, database schema, data types, business definitions, and source references used in the Mutual Fund Analytics Capstone Project.

---

# Dimension Tables

## dim_fund

**Description:** Stores master information about mutual fund schemes.

| Column Name   | Data Type | Description                              | Source             |
| ------------- | --------- | ---------------------------------------- | ------------------ |
| fund_key      | INTEGER   | Surrogate primary key for fund dimension | Generated          |
| amfi_code     | INTEGER   | Unique AMFI scheme identifier            | 01_fund_master.csv |
| fund_house    | TEXT      | Asset Management Company (AMC) name      | 01_fund_master.csv |
| scheme_name   | TEXT      | Name of mutual fund scheme               | 01_fund_master.csv |
| category      | TEXT      | Broad mutual fund category               | 01_fund_master.csv |
| sub_category  | TEXT      | Detailed mutual fund category            | 01_fund_master.csv |
| risk_category | TEXT      | Risk classification of scheme            | 01_fund_master.csv |

---

## dim_date

**Description:** Stores date-related attributes used for time-series analysis.

| Column Name | Data Type | Description                              | Source            |
| ----------- | --------- | ---------------------------------------- | ----------------- |
| date_key    | INTEGER   | Surrogate primary key for date dimension | Generated         |
| date        | DATE      | Calendar date                            | Multiple datasets |
| year        | INTEGER   | Calendar year                            | Derived           |
| month       | INTEGER   | Calendar month                           | Derived           |
| quarter     | INTEGER   | Calendar quarter                         | Derived           |

---

# Fact Tables

## fact_nav

**Description:** Stores historical Net Asset Value (NAV) information for mutual funds.

| Column Name | Data Type | Description                      | Source             |
| ----------- | --------- | -------------------------------- | ------------------ |
| nav_id      | INTEGER   | Primary key                      | Generated          |
| fund_key    | INTEGER   | Foreign key referencing dim_fund | Derived            |
| date_key    | INTEGER   | Foreign key referencing dim_date | Derived            |
| nav         | REAL      | Net Asset Value of scheme        | 02_nav_history.csv |

---

## fact_transactions

**Description:** Stores investor transaction records.

| Column Name      | Data Type | Description                                    | Source                       |
| ---------------- | --------- | ---------------------------------------------- | ---------------------------- |
| transaction_id   | INTEGER   | Primary key                                    | Generated                    |
| fund_key         | INTEGER   | Foreign key referencing dim_fund               | Derived                      |
| date_key         | INTEGER   | Foreign key referencing dim_date               | Derived                      |
| amount_inr       | REAL      | Transaction amount in Indian Rupees            | 08_investor_transactions.csv |
| transaction_type | TEXT      | Type of transaction (SIP, Lumpsum, Redemption) | 08_investor_transactions.csv |

---

## fact_performance

**Description:** Stores mutual fund performance and risk metrics.

| Column Name       | Data Type | Description                       | Source                    |
| ----------------- | --------- | --------------------------------- | ------------------------- |
| performance_id    | INTEGER   | Primary key                       | Generated                 |
| fund_key          | INTEGER   | Foreign key referencing dim_fund  | Derived                   |
| return_1yr_pct    | REAL      | One-year annualized return (%)    | 07_scheme_performance.csv |
| return_3yr_pct    | REAL      | Three-year annualized return (%)  | 07_scheme_performance.csv |
| return_5yr_pct    | REAL      | Five-year annualized return (%)   | 07_scheme_performance.csv |
| expense_ratio_pct | REAL      | Expense ratio charged by fund (%) | 07_scheme_performance.csv |

---

## fact_aum

**Description:** Stores Assets Under Management (AUM) data.

| Column Name | Data Type | Description                       | Source                   |
| ----------- | --------- | --------------------------------- | ------------------------ |
| aum_id      | INTEGER   | Primary key                       | Generated                |
| date_key    | INTEGER   | Foreign key referencing dim_date  | Derived                  |
| fund_house  | TEXT      | Name of AMC                       | 03_aum_by_fund_house.csv |
| aum_crore   | REAL      | Assets Under Management in Crores | 03_aum_by_fund_house.csv |

---

# Source Dataset Summary

## 01_fund_master.csv

Contains mutual fund master data including AMFI codes, fund houses, categories, expense ratios, fund managers, and risk classifications.

---

## 02_nav_history.csv

Contains historical NAV values for mutual fund schemes across multiple dates.

---

## 03_aum_by_fund_house.csv

Contains AUM statistics for different fund houses over time.

---

## 04_monthly_sip_inflows.csv

Contains SIP inflow metrics, active SIP accounts, and SIP AUM trends.

---

## 05_category_inflows.csv

Contains category-wise net inflow and outflow data.

---

## 06_industry_folio_count.csv

Contains folio counts segmented by mutual fund categories.

---

## 07_scheme_performance.csv

Contains fund performance metrics including returns, alpha, beta, Sharpe ratio, Sortino ratio, volatility, drawdown, ratings, and expense ratios.

---

## 08_investor_transactions.csv

Contains investor transaction details including transaction type, amount, location, demographic information, and KYC status.

---

## 09_portfolio_holdings.csv

Contains scheme portfolio holdings including stock names, sectors, portfolio weights, market value, and prices.

---

## 10_benchmark_indices.csv

Contains benchmark index closing values used for comparative performance analysis.

---

# Data Quality Rules Applied

1. Date fields converted to datetime format.
2. NAV values validated to be greater than zero.
3. Missing NAV values forward-filled within each scheme.
4. Duplicate records removed where applicable.
5. Transaction amounts validated to be positive.
6. Transaction types standardized to SIP, Lumpsum, and Redemption.
7. Return metrics converted to numeric data types.
8. Expense ratios validated within acceptable range (0.1%–2.5%).
9. Cleaned datasets stored in the data/processed directory.
10. Data loaded into SQLite star-schema database for analytics.

---

# Database Name

**bluestock_mf.db**

# Database Design

Star Schema consisting of:


* dim_fund
* dim_date
* fact_nav
* fact_transactions
* fact_performance
* fact_aum

This schema supports fund performance analysis, NAV trend analysis, investor transaction analytics, and AUM reporting.
