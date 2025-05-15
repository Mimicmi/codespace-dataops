DROP TABLE IF EXISTS raw_sales CASCADE;

CREATE TABLE raw_sales (
    InvoiceNo TEXT,
    StockCode TEXT,
    Description TEXT,
    Quantity INTEGER,
    InvoiceDate TIMESTAMP,
    UnitPrice NUMERIC,
    CustomerID TEXT,
    Country TEXT
);

COPY raw_sales(InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country)
FROM '/tmp/sales.csv'
DELIMITER ','
CSV HEADER;
