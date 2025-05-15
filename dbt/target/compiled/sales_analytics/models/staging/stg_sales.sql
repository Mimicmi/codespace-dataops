

WITH source AS (
    SELECT * FROM "airflow_db"."public"."raw_sales"
),

cleaned AS (
    SELECT
        InvoiceNo,
        StockCode,
        Description,
        Quantity,
        InvoiceDate,
        UnitPrice,
        CustomerID,
        Country,
        Quantity * UnitPrice AS TotalAmount,
        CURRENT_TIMESTAMP AS loaded_at
    FROM source
)

SELECT * FROM cleaned