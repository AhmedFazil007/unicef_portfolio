import sqlite3
import pandas as pd

conn = sqlite3.connect("../data/mortality.db")

queries = {
    "1_latest_ranked": """
        SELECT c.entity, c.year AS latest_year, c.u5mr AS latest_u5mr
        FROM countries c
        INNER JOIN (
            SELECT entity, MAX(year) AS max_year FROM countries GROUP BY entity
        ) latest ON c.entity = latest.entity AND c.year = latest.max_year
        ORDER BY c.u5mr DESC;
    """,
    "2_pct_reduction_since_1990": """
        SELECT y1990.entity, y1990.u5mr AS u5mr_1990, latest.u5mr AS u5mr_latest,
               latest.year AS latest_year,
               ROUND((y1990.u5mr - latest.u5mr) * 100.0 / y1990.u5mr, 1) AS pct_reduction
        FROM countries y1990
        INNER JOIN (
            SELECT c.entity, c.year, c.u5mr
            FROM countries c
            INNER JOIN (
                SELECT entity, MAX(year) AS max_year FROM countries GROUP BY entity
            ) m ON c.entity = m.entity AND c.year = m.max_year
        ) latest ON y1990.entity = latest.entity
        WHERE y1990.year = 1990
        ORDER BY pct_reduction DESC;
    """,
    "3_join_with_meta": """
        SELECT cm.entity, cm.code, c.year, c.u5mr
        FROM country_meta cm
        INNER JOIN countries c ON cm.entity = c.entity
        INNER JOIN (
            SELECT entity, MAX(year) AS max_year FROM countries GROUP BY entity
        ) latest ON c.entity = latest.entity AND c.year = latest.max_year
        ORDER BY c.u5mr ASC;
    """,
    "4_regional_decade_trend": """
        SELECT entity,
               MAX(CASE WHEN year = 1990 THEN u5mr END) AS y1990,
               MAX(CASE WHEN year = 2000 THEN u5mr END) AS y2000,
               MAX(CASE WHEN year = 2010 THEN u5mr END) AS y2010,
               MAX(CASE WHEN year = 2024 THEN u5mr END) AS y2024
        FROM regions
        GROUP BY entity;
    """,
    "5_above_africa_avg": """
        SELECT c.entity, c.year, c.u5mr
        FROM countries c
        WHERE c.year = (SELECT MAX(year) FROM countries)
          AND c.u5mr > (
              SELECT u5mr FROM regions WHERE entity = 'Africa' ORDER BY year DESC LIMIT 1
          );
    """,
}

for name, q in queries.items():
    print(f"\n=== {name} ===")
    df = pd.read_sql_query(q, conn)
    print(df.to_string(index=False))
    df.to_csv(f"../output/query_{name}.csv", index=False)

conn.close()
