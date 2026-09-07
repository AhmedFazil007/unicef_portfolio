# Under-Five Mortality: Data Cleaning, SQL Analysis & Dashboard

**Status: portfolio / practice project — not employer work product.**

This project was built to demonstrate a real, inspectable data-analyst workflow:
cleaning a public dataset with Python, analyzing it with SQL, and visualizing the
results — using the same subject-matter family (UNICEF / UN child-welfare data)
referenced in my CV, but built entirely on public data rather than any employer's
internal data.

## Data source

Our World in Data (`ourworldindata.org/grapher/child-mortality`), which combines:
- **UN Inter-agency Group for Child Mortality Estimation (UN IGME)** — a collaboration
  led by **UNICEF** together with WHO, the World Bank, and the UN Population Division
- **Gapminder** (for historical estimates pre-1990)

Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Downloaded September 2026.

The extract used here covers 10 countries (Afghanistan, Albania, Algeria, Angola,
Bangladesh, Brazil, Chad, China, Egypt, Ethiopia) plus 4 regional aggregates
(Africa, Asia, Europe, European Union), spanning 1950–2024 — 400 raw rows.

## What's in this repo

```
unicef_portfolio/
├── data/
│   ├── raw_child_mortality.csv     # as downloaded, unmodified
│   ├── clean_countries.csv         # cleaned, country-level only
│   ├── clean_regions.csv           # cleaned, regional aggregates only
│   └── mortality.db                # SQLite database used for SQL analysis
├── scripts/
│   ├── 01_clean_data.py            # pandas cleaning: dedup, missing values, type fixes, split
│   ├── 02_load_to_sqlite.py        # loads cleaned CSVs into SQLite
│   ├── 03_run_queries.py           # runs the SQL queries, saves results
│   └── 04_visualize.py             # generates all charts with matplotlib
├── sql/
│   └── queries.sql                 # 5 real SQL queries: ranking, self-join, join, pivot, cross-table
├── output/
│   ├── chart_*.png                 # generated charts
│   ├── query_*.csv                 # query result exports
│   └── dashboard.html              # standalone dashboard (open directly in a browser)
└── README.md
```

## How to reproduce

```bash
cd scripts
python3 01_clean_data.py
python3 02_load_to_sqlite.py
python3 03_run_queries.py
python3 04_visualize.py
```

## Cleaning steps taken

1. Checked for missing values (none found in this extract).
2. Checked for duplicate `(entity, year)` records (none found).
3. Separated country-level rows from regional/continental aggregates — OWID marks
   aggregates with an `OWID_`-prefixed code (e.g. `OWID_AFR` for Africa), which must
   be excluded from country-level rankings or they distort the comparison.
4. Standardized types (year → int, rate → float) and stripped whitespace from names.
5. Range-checked all rate values against a plausible 0–100 band.

## SQL techniques demonstrated

- Subquery + join to find each country's most recent reported year
- Self-join to compute percentage change between two time points (1990 vs. latest)
- Join against a separate lookup table (`country_meta`)
- Conditional aggregation (`CASE WHEN`) to pivot years into columns
- Cross-table comparison (countries vs. regional average)

## Key findings

- China shows the largest relative improvement since 1990 (-89.4%).
- Chad has both the highest current rate (9.73 per 100 live births, 2024) and the
  smallest relative improvement since 1990 (-54.0%) in this dataset.
- The EU's 2024 average (0.39) is roughly 17x lower than Africa's (6.63), though
  Africa has still cut its rate by more than half since 1990.

## Author

Ahmed Fazil — built as a self-directed practice project.
