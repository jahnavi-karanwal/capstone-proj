-- 1. Top 5 funds by 5-Year Return

SELECT
    d.scheme_name,
    f.return_5yr_pct
FROM fact_performance f
JOIN dim_fund d
ON f.fund_key = d.fund_key
ORDER BY f.return_5yr_pct DESC
LIMIT 5;


-- 2. Top 5 Funds by 1-Year Return

SELECT
    d.scheme_name,
    f.return_1yr_pct
FROM fact_performance f
JOIN dim_fund d
ON f.fund_key = d.fund_key
ORDER BY f.return_1yr_pct DESC
LIMIT 5;


-- 3. Average NAV Per Month

SELECT
    dd.year,
    dd.month,
    ROUND(AVG(fn.nav),2) AS avg_nav
FROM fact_nav fn
JOIN dim_date dd
ON fn.date_key = dd.date_key
GROUP BY dd.year, dd.month
ORDER BY dd.year, dd.month;


-- 4. Transaction Volume by Type

SELECT
    transaction_type,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_inr),2) AS total_amount
FROM fact_transactions
GROUP BY transaction_type;


-- 5. Transactions by State

-- Monthly Transaction Amount

SELECT
    dd.year,
    dd.month,
    ROUND(SUM(ft.amount_inr),2) AS total_amount
FROM fact_transactions ft
JOIN dim_date dd
ON ft.date_key = dd.date_key
GROUP BY dd.year, dd.month
ORDER BY dd.year, dd.month;


-- 6. Funds with Expense Ratio Below 1%

SELECT
    d.scheme_name,
    fp.expense_ratio_pct
FROM fact_performance fp
JOIN dim_fund d
ON fp.fund_key = d.fund_key
WHERE fp.expense_ratio_pct < 1
ORDER BY fp.expense_ratio_pct;


-- 7. Average Return by Category

SELECT
    d.category,
    ROUND(AVG(fp.return_3yr_pct),2) AS avg_return
FROM fact_performance fp
JOIN dim_fund d
ON fp.fund_key = d.fund_key
GROUP BY d.category
ORDER BY avg_return DESC;


-- 8. Highest Sharpe-Like Funds
-- Using 5Y return as proxy

SELECT
    d.scheme_name,
    fp.return_5yr_pct
FROM fact_performance fp
JOIN dim_fund d
ON fp.fund_key = d.fund_key
ORDER BY fp.return_5yr_pct DESC
LIMIT 10;


-- 9. Fund House Distribution

SELECT
    fund_house,
    COUNT(*) AS total_funds
FROM dim_fund
GROUP BY fund_house
ORDER BY total_funds DESC;


-- 10. Total AUM by Fund House

SELECT
    fund_house,
    ROUND(SUM(aum_crore),2) AS total_aum
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum DESC;