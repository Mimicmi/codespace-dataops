import pandas as pd

# Charger l'Excel
df = pd.read_excel('Online Retail.xlsx')

# Garder uniquement les colonnes nécessaires
columns = [
    'InvoiceNo',
    'StockCode',
    'Description',
    'Quantity',
    'InvoiceDate',
    'UnitPrice',
    'CustomerID',
    'Country'
]

df = df[columns]

# Nettoyage de base : supprimer les lignes vides
df = df.dropna(subset=['CustomerID', 'UnitPrice'])

# Sauvegarder en CSV
df.to_csv('sales.csv', index=False)
