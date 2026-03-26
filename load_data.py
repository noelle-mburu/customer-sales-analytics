import pandas as pd
from sqlalchemy import create_engine
import os

# Database connection settings
DB_USER = "postgres"
DB_PASSWORD = "your_password_here"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "olist"

# SQLAlchemy connection string — connects Python to PostgreSQL
connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(connection_string)

# Path to the folder containing the CSV files
DATA_FOLDER = r"D:\LuxDev\github_projects\customer-sales-analytics\files"

# Maps CSV filenames to their target table names in PostgreSQL
csv_files = {
    "olist_customers_dataset.csv": "customers",
    "olist_orders_dataset.csv": "orders",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "olist_geolocation_dataset.csv": "geolocation",
    "product_category_name_translation.csv": "category_translation"
}

print("Starting data load...\n")

for filename, table_name in csv_files.items():
    file_path = os.path.join(DATA_FOLDER, filename)
    print(f"Loading {filename} → table: '{table_name}'...")

    df = pd.read_csv(file_path)

    df.to_sql(
        name=table_name,
        con=engine,
        schema="olist",
        if_exists="replace",
        index=False
    )

    print(f"  Done! {len(df):,} rows loaded.\n")

print("All tables loaded successfully!")
print(f"\nTables created in the '{DB_NAME}' database:")
for table_name in csv_files.values():
    print(f"  - {table_name}")