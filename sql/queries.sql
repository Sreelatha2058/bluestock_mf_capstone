-- Bluestock MF Capstone — 10 Analytical Queries
-- Day 2: SQL Analytics

-- Q1: Top 5 funds by AUM
SELECT scheme_name, fund_house, aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;

-- Q2: Average NAV per month for SBI Bluechip (119551)
SELECT strftime('%Y-%m', nav_date) AS month,
       ROUND(AVG(nav), 2) AS avg_nav
FROM fact_nav
WHERE amfi_code = 119551
GROUP BY month
ORDER BY month;

-- Q3: SIP inflow YoY growth
SELECT month, sip_inflow_crore, yoy_growth_pct
FROM fact_sip_industry
WHERE yoy_growth_pct IS NOT NULL
ORDER BY month;

-- Q4: Total transaction amount by state
SELECT state,
       ROUND(SUM(amount_inr) / 10000000.0, 2) AS total_amount_crore
FROM fact_transactions
GROUP BY state
ORDER BY total_amount_crore DESC;

-- Q5: Funds with expense ratio less than 1%
SELECT scheme_name, fund_house, expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- Q6: Top 5 funds by Sharpe ratio
SELECT scheme_name, fund_house, sharpe_ratio, risk_grade
FROM fact_performance
ORDER BY sharpe_ratio DESC
LIMIT 5;

-- Q7: Average SIP amount by age group
SELECT age_group,
       ROUND(AVG(amount_inr), 2) AS avg_sip_amount,
       COUNT(*) AS total_transactions
FROM fact_transactions
WHERE transaction_type = 'Sip'
GROUP BY age_group
ORDER BY avg_sip_amount DESC;

-- Q8: Fund count per category
SELECT category, sub_category, COUNT(*) AS num_funds
FROM dim_fund
GROUP BY category, sub_category
ORDER BY num_funds DESC;

-- Q9: Top 5 sectors by total portfolio weight
SELECT sector,
       ROUND(SUM(weight_pct), 2) AS total_weight
FROM fact_portfolio
GROUP BY sector
ORDER BY total_weight DESC
LIMIT 5;

-- Q10: Benchmark index performance — latest vs 1 year ago
SELECT index_name,
       ROUND(MAX(close_value), 2) AS latest_value,
       ROUND(MIN(close_value), 2) AS lowest_value,
       ROUND((MAX(close_value) - MIN(close_value)) / MIN(close_value) * 100, 2) AS growth_pct
FROM fact_benchmark
GROUP BY index_name
ORDER BY growth_pct DESC;