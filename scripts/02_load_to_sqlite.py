"""
Loads the cleaned country + region CSVs into a local SQLite database
so we can run real SQL against them.

Two tables are created:
- countries(entity, code, year, u5mr)
- regions(entity, code, year, u5mr)

A separate lookup table `country_meta` is also built to demonstrate
a genuine JOIN (entity -> code lookup), rather than querying a single
flat table.
"""

import sqlite3
import pandas as pd

DB_PATH = "../data/mortality.db"

countries = pd.read_csv("../data/clean_countries.csv")
regions = pd.read_csv("../data/clean_regions.csv")

conn = sqlite3.connect(DB_PATH)

countries.to_sql("countries", conn, if_exists="replace", index=False)
regions.to_sql("regions", conn, if_exists="replace", index=False)

# Build a small lookup table of entity -> code (deduplicated) to allow
# a genuine join example, rather than just querying one flat table.
country_meta = countries[["entity", "code"]].drop_duplicates().reset_index(drop=True)
country_meta.to_sql("country_meta", conn, if_exists="replace", index=False)

conn.commit()

cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM countries")
print("countries table rows:", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM regions")
print("regions table rows:", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM country_meta")
print("country_meta table rows:", cur.fetchone()[0])

conn.close()
print(f"\nSQLite database written to {DB_PATH}")
