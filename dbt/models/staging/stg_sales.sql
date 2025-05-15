{{
  config(
    materialized='view',
    schema='staging'
  )
}}

WITH source AS (
    SELECT * FROM {{ source('raw', 'sales') }}
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