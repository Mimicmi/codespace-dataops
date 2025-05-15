

WITH daily_revenue AS (
    SELECT
        DATE(InvoiceDate) AS transaction_date,
        Country,
        CustomerID,
        SUM(TotalAmount) AS daily_revenue,
        COUNT(DISTINCT InvoiceNo) AS nb_transactions
    FROM "airflow_db"."public_staging"."stg_sales"
    GROUP BY 1, 2, 3
)

SELECT 
    transaction_date,
    Country,
    CustomerID,
    daily_revenue,
    nb_transactions,
    daily_revenue/nb_transactions AS avg_transaction_value
FROM daily_revenue