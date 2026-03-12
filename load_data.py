# Importing necessary libraries
import pandas as pd   # a Python library for working with data sets. It has functions for analyzing, cleaning, exploring, and manipulating data.
from sqlalchemy import create_engine
import os     # a built-in python module that lets you interact with your operating system; files, folders, and paths etc.

# ── Why SQLAlchemy? ───────────────────────────────────────────────────────────
# SQLAlchemy is a Python library that lets us talk to databases.
# Instead of writing raw database commands, we can use Python to:
# 1. Connect to our PostgreSQL database
# 2. Load pandas DataFrames directly into database tables
# It's like a translator between Python and PostgreSQL.

# ── Database connection settings ──────────────────────────────────────────────
DB_USER = "postgres"       # your PostgreSQL username (usually "postgres")
DB_PASSWORD = "9876"  # your PostgreSQL password
DB_HOST = "localhost"      # the server where PostgreSQL is running (your own machine)
DB_PORT = "5432"           # the default PostgreSQL port
DB_NAME = "olist"          # the name of the database we'll create the tables in

# ── Connection string ─────────────────────────────────────────────────────────
# This is the address SQLAlchemy uses to find and connect to your database.
# Format: "postgresql://username:password@host:port/database_name"
# Think of it like a URL for your database.
connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the engine; this is the actual connection object we'll use to send data
# to PostgreSQL. We haven't connected yet, we've just set up the instructions.
engine = create_engine(connection_string)

# ── Folder path ───────────────────────────────────────────────────────────────
DATA_FOLDER = r"D:\LuxDev\github_projects\customer-sales-analytics\files"  # raw string (r"") allows backslashes without needing to escape them

# ── CSV files to load ─────────────────────────────────────────────────────────
# This is a dictionary that maps:
# - the CSV filename (file names on your computer)
# - to the table name (what it will be called in PostgreSQL)
# Using short, clean table names makes SQL queries easier to write
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

# ── Load each CSV into PostgreSQL ─────────────────────────────────────────────
print("Starting data load...\n")

for filename, table_name in csv_files.items():

    # Build the full path to the CSV file
    # os.path.join() safely combines folder path + filename
    # regardless of whether you're on Windows or Mac
    file_path = os.path.join(DATA_FOLDER, filename)

    print(f"Loading {filename} → table: '{table_name}'...")

    # Read the CSV file into a pandas DataFrame
    # A DataFrame is like an Excel table in Python; rows and columns
    df = pd.read_csv(file_path)

    # Load the DataFrame into PostgreSQL
    # to_sql() does this:
    # - Creates the table if it doesn't exist
    # - Inserts all rows from the DataFrame
    # if_exists="replace" means: if the table already exists, drop it and recreate it
    # This is useful when re-running the script so you always get fresh data
    # index=False means: don't add an extra "index" column from pandas
    df.to_sql(
        name=table_name,        # name of the table in PostgreSQL
        con=engine,             # the connection we created above
        schema="olist",         # the olist schema in the database
        if_exists="replace",    # replace table if it already exists
        index=False             # don't write the pandas row numbers as a column
    )

    print(f"  Done! {len(df):,} rows loaded.\n")

print("All tables loaded successfully!")
print(f"\nTables created in the '{DB_NAME}' database:")
for table_name in csv_files.values():
    print(f"  - {table_name}")