"""
Data cleaning script for the Under-Five Mortality dataset
Source: Our World in Data, sourced from UN Inter-agency Group for
Child Mortality Estimation (UN IGME) — a collaboration led by UNICEF
with WHO, the World Bank, and the UN Population Division — and Gapminder.
License: CC BY 4.0

This script:
1. Loads the raw CSV
2. Separates country-level rows from regional/aggregate rows
   (aggregates use an OWID_ prefixed code, e.g. OWID_AFR for Africa)
3. Checks for duplicate (Entity, Year) records
4. Checks for missing values
5. Standardizes column names and types
6. Saves two clean output files: countries.csv and regions.csv
"""

import pandas as pd

RAW_PATH = "../data/raw_child_mortality.csv"
COUNTRIES_OUT = "../data/clean_countries.csv"
REGIONS_OUT = "../data/clean_regions.csv"


def main():
    df = pd.read_csv(RAW_PATH)

    # Standardize column names
    df = df.rename(columns={
        "Entity": "entity",
        "Code": "code",
        "Year": "year",
        "Under-five mortality rate (selected)": "u5mr",
    })

    print(f"Raw rows loaded: {len(df)}")

    # --- Missing value check ---
    missing = df.isnull().sum()
    print("\nMissing values per column:")
    print(missing)

    # --- Duplicate check ---
    dupes = df.duplicated(subset=["entity", "year"]).sum()
    print(f"\nDuplicate (entity, year) rows found: {dupes}")
    if dupes:
        df = df.drop_duplicates(subset=["entity", "year"])
        print(f"Duplicates removed. Rows remaining: {len(df)}")

    # --- Type standardization ---
    df["year"] = df["year"].astype(int)
    df["u5mr"] = df["u5mr"].astype(float)
    df["entity"] = df["entity"].str.strip()

    # --- Separate country-level data from regional aggregates ---
    # OWID uses an "OWID_" prefix in the Code field for continents/regions
    # (e.g. OWID_AFR = Africa, OWID_EU27 = European Union). These are not
    # individual countries, so they need to be excluded from country-level
    # rankings, or they will incorrectly appear alongside real countries.
    is_aggregate = df["code"].astype(str).str.startswith("OWID_")

    regions_df = df[is_aggregate].copy()
    countries_df = df[~is_aggregate].copy()

    print(f"\nCountry-level rows: {len(countries_df)}")
    print(f"Regional aggregate rows: {len(regions_df)}")
    print(f"Countries included: {sorted(countries_df['entity'].unique())}")
    print(f"Regions included: {sorted(regions_df['entity'].unique())}")

    # --- Sanity check: rate should be a plausible percentage-like value ---
    out_of_range = countries_df[(countries_df["u5mr"] < 0) | (countries_df["u5mr"] > 100)]
    if len(out_of_range):
        print(f"\nWARNING: {len(out_of_range)} rows with implausible u5mr values found:")
        print(out_of_range)

    countries_df = countries_df.sort_values(["entity", "year"]).reset_index(drop=True)
    regions_df = regions_df.sort_values(["entity", "year"]).reset_index(drop=True)

    countries_df.to_csv(COUNTRIES_OUT, index=False)
    regions_df.to_csv(REGIONS_OUT, index=False)

    print(f"\nSaved cleaned country data to {COUNTRIES_OUT}")
    print(f"Saved cleaned regional data to {REGIONS_OUT}")


if __name__ == "__main__":
    main()
